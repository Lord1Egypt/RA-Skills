#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_lib.py — 通用批量检索引擎（ct-* 技能族通用）

设计要点（详见各技能 references/batch_spec.md）：
- 自包含：仅依赖 Python 标准库；仅在提供 YAML spec 时按需 import yaml。
  运行时**不依赖 ct-base**，符合 ct 家族"复制 → 注入 → 自包含"模型。
- 每个 entry = 一次子进程 CLI 调用（家族事实契约；ct-registry 自身即如此）。
- --pack 模式（2026-10-20）：多个 entry 打包成一次 Coze 调用（mode=batch_search），
  Coze 端拆解逐条执行后批量返回；翻译预处理一次完成；结果按 entry id 拆回并写
  pack_payloads.json，再以 --from-pack 子进程复用 ct_literature.py 全管线。
  端点不支持该契约时自动回退逐 entry 模式。契约见 references/batch_search_contract.md。
- --concurrency N（默认 1）：entry 级并发执行（子进程层，不改写各技能 CLI）。
- 严格继承 SAFE PREVIEW：默认只打印计划（dry-run），必须显式 --run 才联网执行。
- 每个 entry 写入独立 out_dir/<id>/ 子目录，避免固定文件名互相覆盖。
- 增量写 manifest + --resume 续跑，单 entry 失败不拖垮整批。
- 配额闸门：OpenAlex 免 key 仅 100/天，run 前预估并警告。

引擎完全通用；差异仅在各技能的 ADAPTER 字典（字段→CLI flag 映射）。
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import re
import shlex
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

ENGINE_VERSION = "1.1.0"

# ── §16.9 出站调用收口：transport 实现移入 adapters/ ──────────────────
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SKILL_ROOT not in sys.path:
    sys.path.insert(0, _SKILL_ROOT)
from adapters.batch_pack_send import pack_send as _pack_send_impl  # noqa: E402


# --------------------------------------------------------------------------
# 工具函数
# --------------------------------------------------------------------------

def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _slugify(text, max_len=48):
    text = (text or "").strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "_", text).strip("_-")
    return text[:max_len].strip("_-") or "entry"


def _parse_scalar(v):
    """把字符串标量解析为 bool/int/float/str（YAML 已自带类型，这里主要服务行列表）。"""
    if isinstance(v, (bool, int, float)):
        return v
    s = str(v).strip()
    low = s.lower()
    if low in ("true", "yes", "1"):
        return True
    if low in ("false", "no", "0"):
        return False
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def _is_truthy(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    if v is None:
        return False
    return str(v).strip().lower() not in ("", "false", "no", "0")


def _str(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


# --------------------------------------------------------------------------
# spec 解析
# --------------------------------------------------------------------------

META_KEYS = {"_primary", "_skill", "_lineno", "_id_hint",
             "_label_hint", "_enabled", "_out_dir_override"}


def _load_yaml(path):
    try:
        import yaml  # type: ignore
    except ImportError:
        sys.stderr.write(
            "[batch] ERROR: YAML spec 需要 PyYAML。请安装：pip install pyyaml\n")
        raise
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _parse_kv_tokens(tok_str):
    """shlex 切分 key=value 对；双引号内的空格被保留。
    畸形引号（如用户粘贴带半个引号的文本）时退化为空白切分——
    单行参数异常不应以 traceback 拖垮整批。"""
    if not tok_str.strip():
        return {}
    try:
        toks = shlex.split(tok_str)
    except ValueError:
        toks = tok_str.split()
    out = {}
    for tok in toks:
        if "=" not in tok:
            continue
        k, v = tok.split("=", 1)
        out[k.strip()] = v
    return out


def _normalize_concepts(value):
    """把 concepts 规范化为 [TYPE=VALUE, ...] 字符串列表，统一三种来源：
    - 行列表字符串 "intervention:pembro;outcome:OS" → 拆 ';'、':'→'='
    - YAML 列表的 dict（{intervention: pembro}）→ 取首个 k=v
    - YAML 列表的字符串（"intervention=pembro"）→ 保留（':'→'='）"""
    if value is None:
        return None
    if isinstance(value, list):
        out = []
        for item in value:
            if isinstance(item, dict):
                if item:
                    k = next(iter(item))
                    out.append("%s=%s" % (k, item[k]))
            elif isinstance(item, str):
                out.append(item.replace(":", "=", 1))
            else:
                out.append(str(item))
        return out
    if isinstance(value, str):
        items = []
        for part in value.split(";"):
            part = part.strip()
            if part:
                items.append(re.sub(r":", "=", part, 1))
        return items
    return [str(value)]


def _detect_format(path, raw):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".yaml", ".yml"):
        return "yaml"
    head = raw.lstrip()[:200].lower()
    if head.startswith("version:") or "entries:" in head:
        return "yaml"
    return "linelist"


def parse_linelist(text, default_skill):
    entries = []
    cur_skill = default_skill
    for lineno, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("@"):
            cur_skill = s[1:].strip()
            continue
        if "|" in raw:
            primary, _, kv = raw.partition("|")
        else:
            primary, kv = raw, ""
        primary = primary.strip()
        fields = {}
        for k, v in _parse_kv_tokens(kv).items():
            fields[k] = _parse_scalar(v)
        if "concepts" in fields:
            fields["concepts"] = _normalize_concepts(fields["concepts"])
        fields["_primary"] = primary
        fields["_skill"] = cur_skill
        fields["_lineno"] = lineno
        entries.append(fields)
    return entries


def parse_yaml(doc, default_skill):
    if not isinstance(doc, dict):
        raise ValueError("YAML spec 顶层必须是 mapping（含 version/entries）")
    doc_skill = doc.get("skill", default_skill)
    defaults = doc.get("defaults") or {}
    raw_entries = doc.get("entries") or []
    if not isinstance(raw_entries, list):
        raise ValueError("YAML spec 的 entries 必须是列表")
    out = []
    for i, e in enumerate(raw_entries):
        if not isinstance(e, dict):
            raise ValueError("entries[%d] 必须是 mapping" % i)
        merged = dict(defaults)          # defaults 为基
        merged.update(e)                  # entry 覆盖
        if "concepts" in merged:
            merged["concepts"] = _normalize_concepts(merged["concepts"])
        skill = merged.get("skill", doc_skill)
        fields = {k: v for k, v in merged.items()
                  if k not in ("id", "label", "skill", "enabled", "out_dir")}
        fields["_skill"] = skill
        fields["_id_hint"] = e.get("id")
        fields["_label_hint"] = e.get("label")
        fields["_enabled"] = e.get("enabled", True)
        fields["_out_dir_override"] = e.get("out_dir")
        fields["_lineno"] = i + 1
        out.append(fields)
    return out


# --------------------------------------------------------------------------
# entry 构建 + 校验
# --------------------------------------------------------------------------

def _build_entry_dict(fields, adapter, idx):
    primary_field = adapter.get("primary_field", "topic")
    default_skill = adapter.get("default_skill", "ct-literature")
    supported = adapter.get("supported_skills", [default_skill])

    if "_primary" in fields:
        fields[primary_field] = fields.pop("_primary")

    skill = fields.get("_skill", default_skill)
    entry = {
        "index": idx,
        "skill": skill,
        "lineno": fields.get("_lineno"),
        "enabled": bool(fields.get("_enabled", True)),
        "id": None,
        "label": None,
        "out_dir_override": fields.get("_out_dir_override"),
        "fields": {},
        "status": "pending",
        "reason": "",
        "cmd": None,
        "returncode": None,
        "elapsed_sec": None,
        "n_results": None,
        "out_dir": None,
    }

    base = (fields.get(primary_field) or fields.get("_label_hint")
            or ("entry_%d" % (idx + 1)))
    entry["id"] = str(fields.get("_id_hint") or _slugify(str(base)))
    entry["label"] = fields.get("_label_hint") or fields.get(primary_field) or entry["id"]

    if skill not in supported:
        entry["status"] = "skipped"
        entry["reason"] = "skill '%s' 不被本 adapter 支持（v1 仅: %s）" % (
            skill, ", ".join(supported))
        return entry
    if not entry["enabled"]:
        entry["status"] = "skipped"
        entry["reason"] = "已禁用 (enabled=false)"
        return entry

    fmap = adapter["fields"]
    cleaned = {}
    errors = []
    for k, v in fields.items():
        if k in META_KEYS:
            continue
        if k not in fmap:
            errors.append("未知字段 '%s'" % k)
            continue
        cleaned[k] = v
    for req in adapter.get("required", []):
        if req not in cleaned or cleaned.get(req) in (None, "", False):
            errors.append("缺少必填字段 '%s'" % req)
    if errors:
        entry["status"] = "error"
        entry["reason"] = "; ".join(errors)
        return entry

    entry["fields"] = cleaned
    return entry


# --------------------------------------------------------------------------
# 命令构建
# --------------------------------------------------------------------------

def _build_cmd(entry, adapter, engine_script_dir, entry_out_dir):
    script_path = os.path.join(engine_script_dir, adapter["script"])
    argv = [sys.executable, script_path]
    fmap = adapter["fields"]
    for k, v in entry["fields"].items():
        spec = fmap[k]
        flag = spec["flag"]
        kind = spec.get("kind", "value")
        if kind == "value":
            if v in (None, "", False):
                continue
            argv += ["--" + flag, _str(v)]
        elif kind == "flag_true":
            if _is_truthy(v):
                argv += ["--" + flag]
        elif kind == "flag_booloptional":
            if v is True or (isinstance(v, str) and v.lower() == "true"):
                argv += ["--" + flag]
            elif v is False or (isinstance(v, str) and v.lower() == "false"):
                argv += ["--no-" + flag]
            # 否则沿用脚本默认，不传
        elif kind == "append":
            items = v if isinstance(v, list) else [v]
            for item in items:
                argv += ["--" + flag, _str(item)]
    # 计划命令始终带 --run，便于复制执行（dry-run 只打印不执行）
    argv += ["--run", "--out-dir", entry_out_dir]
    return argv


# --------------------------------------------------------------------------
# 聚合产物
# --------------------------------------------------------------------------

def _count_results(entry_out_dir):
    for fn in (".merged.json", "openalex.json"):
        p = os.path.join(entry_out_dir, fn)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            continue
        if isinstance(d, dict):
            for k in ("works", "results", "records"):
                if isinstance(d.get(k), list):
                    return len(d[k])
            if isinstance(d.get("data"), list):
                return len(d["data"])
        elif isinstance(d, list):
            return len(d)
    return None


def _summarize(entries):
    s = {"total": len(entries), "ok": 0, "error": 0,
         "skipped": 0, "resumed": 0, "pending": 0}
    for e in entries:
        st = e["status"]
        s[st] = s.get(st, 0) + 1
    return s


def _write_manifest(batch_out, spec_file, fmt, run_mode, entries, adapter):
    path = os.path.join(batch_out, "batch_manifest.json")
    data = {
        "engine": "ct-batch-lib",
        "engine_version": ENGINE_VERSION,
        "generated_at": _now_iso(),
        "spec_file": spec_file,
        "format": fmt,
        "run_mode": run_mode,
        "adapter_skill": adapter.get("default_skill"),
        "summary": _summarize(entries),
        "entries": [
            {
                "id": e["id"], "label": e["label"], "skill": e["skill"],
                "status": e["status"], "reason": e["reason"],
                "out_dir": e.get("out_dir"), "cmd": e.get("cmd"),
                "returncode": e.get("returncode"),
                "elapsed_sec": e.get("elapsed_sec"),
                "n_results": e.get("n_results"),
                "lineno": e.get("lineno"),
                "pack_keyword": e.get("pack_keyword"),
            } for e in entries
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _write_errors(batch_out, errors_log):
    path = os.path.join(batch_out, "batch_errors.log")
    if not errors_log:
        if os.path.isfile(path):
            os.remove(path)
        return
    with open(path, "w", encoding="utf-8") as f:
        for eid, rc, msg in errors_log:
            f.write("==== %s (exit %s) ====\n%s\n\n" % (eid, rc, msg))


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _write_index_html(batch_out, entries, adapter):
    path = os.path.join(batch_out, "batch_index.html")
    rows = []
    for e in entries:
        link = ""
        if e.get("out_dir"):
            rep = os.path.join(e["out_dir"], "lit_report.html")
            if os.path.isfile(rep):
                link = '<a href="%s/lit_report.html">report</a>' % e["id"]
        n = e.get("n_results")
        nstr = str(n) if n is not None else "-"
        rows.append(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (_esc(e["id"]), _esc(e["label"]), _esc(e["status"]), nstr,
               _esc(str(e.get("elapsed_sec") or "-")), link))
    sm = _summarize(entries)
    html = (
        "<html><head><meta charset='utf-8'><title>Batch Index</title>"
        "<style>body{font-family:system-ui,sans-serif;margin:2rem}"
        "table{border-collapse:collapse;width:100%%}"
        "th,td{border:1px solid #ddd;padding:.5rem;text-align:left}"
        "h1{font-size:1.3rem}p.caption{margin:1rem 0}</style></head><body>"
        "<h1>ct-literature 批量检索汇总</h1>"
        "<p class='caption'>总计 %d · 成功 %d · 失败 %d · 跳过 %d · 续跑 %d</p>"
        "<table><thead><tr><th>ID</th><th>Label</th><th>状态</th>"
        "<th>结果数</th><th>耗时(s)</th><th>报告</th></tr></thead>"
        "<tbody>%s</tbody></table></body></html>"
        % (sm["total"], sm["ok"], sm["error"], sm["skipped"],
           sm["resumed"], "\n".join(rows))
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def _write_summary_md(batch_out, entries, adapter, spec_file, fmt):
    path = os.path.join(batch_out, "batch_summary.md")
    sm = _summarize(entries)
    lines = [
        "# 批量检索摘要", "",
        "- 规格文件: `%s`" % spec_file,
        "- 格式: %s" % fmt,
        "- 总计: %d · 成功: %d · 失败: %d · 跳过: %d · 续跑: %d" % (
            sm["total"], sm["ok"], sm["error"], sm["skipped"], sm["resumed"]),
        "",
        "| ID | Label | 状态 | 结果数 | 耗时(s) |",
        "|---|---|---|---|---|",
    ]
    for e in entries:
        n = e.get("n_results")
        lines.append("| %s | %s | %s | %s | %s |" % (
            e["id"], e["label"], e["status"],
            n if n is not None else "-", e.get("elapsed_sec") or "-"))
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _print_summary(entries, progress):
    sm = _summarize(entries)
    if progress == "json":
        print(json.dumps({"event": "summary", **sm}, ensure_ascii=False))
    else:
        print("\n[batch] 汇总：总计 %d · 成功 %d · 失败 %d · 跳过 %d · 续跑 %d"
              % (sm["total"], sm["ok"], sm["error"], sm["skipped"], sm["resumed"]))


# --------------------------------------------------------------------------
# Pack 模式（--pack，2026-10-20）：多个 entry 打包成一次 Coze 调用
# --------------------------------------------------------------------------
# 流程：翻译预处理（一次）→ 按包大小拆包 → 每包一次 POST（mode=batch_search，
# queries 数组）→ Coze 端拆解逐条执行、批量返回 → 按 entry id 拆回写
# pack_payloads.json → --from-pack 子进程复用 ct_literature.py 全管线。
# 传输复用 fetch_coze_unified：异步协议（{accepted, run_id} + 轮询）与 S3
# 外置回参；端点不支持 batch_search 契约时自动回退逐 entry 模式。
# Coze 端契约见 references/batch_search_contract.md。

PACK_MODE_NAME = "batch_search"


def _pack_import_skill(engine_script_dir):
    """import 技能侧复用件（fetch_coze_unified / topic_translator）。
    batch_lib 位于 scripts/，adapters/ 与 scripts/ 同级（技能根下）。"""
    skill_root = os.path.dirname(engine_script_dir)
    for _p in (engine_script_dir, skill_root):
        if _p and _p not in sys.path:
            sys.path.insert(0, _p)
    fcu = importlib.import_module("adapters.fetch_coze_unified")
    tt = importlib.import_module("topic_translator")
    return fcu, tt


def _pack_prepare_keywords(entries, adapter, tt, online=True):
    """一次预处理：全部 entry 的检索式翻英。

    复刻 ct_literature._build_search_topic 的概念 AND 拼接与去重规则；
    翻译按唯一字符串缓存——联网兜底（MyMemory）对相同片段只发一次。
    online=False 不走联网兜底（dry-run 预览用，保持零联网）。
    """
    primary = adapter.get("primary_field", "topic")
    cache = {}

    def _tr(text):
        key = str(text or "").strip()
        if not key:
            return {"translated": False, "topic_en": key, "untranslated": []}
        if key not in cache:
            try:
                cache[key] = tt.translate_topic(key, online_fallback=online)
            except Exception:
                cache[key] = {"translated": False, "topic_en": key,
                              "untranslated": []}
        return cache[key]

    stats = {"translated": 0, "already_en": 0, "partial": 0}
    for e in entries:
        if e["status"] != "pending":
            continue
        f = e["fields"]
        topic = f.get(primary) or ""
        tp = _tr(topic)
        kw = tp.get("topic_en") if tp.get("translated") else str(topic)
        seen, terms = set(), []
        kw_l = kw.lower()
        for c in (f.get("concepts") or []):
            if isinstance(c, str) and "=" in c:
                v = c.split("=", 1)[1].strip()
            else:
                v = str(c).strip()
            if not v:
                continue
            ctp = _tr(v)
            cv = ctp.get("topic_en") if ctp.get("translated") else v
            ck = cv.lower()
            if ck in seen or ck in kw_l:
                continue
            seen.add(ck)
            terms.append(cv)
        e["pack_keyword"] = (kw + " " + " ".join(terms)).strip() if terms else kw
        if tp.get("translated"):
            if tp.get("untranslated"):
                stats["partial"] += 1
            else:
                stats["translated"] += 1
        else:
            stats["already_en"] += 1
    return stats


def _pack_sources_for(entry, adapter, fcu):
    """本 entry 应打包给 Coze 的 source 列表（复刻 dispatch 的 Coze 路由）：
    - semantic_scholar 恒本地（2026-09-06 决策：私人 key 零传递），不进包；
    - openalex 仅本机无 key 时进包（有 key 走本地 keyed pool，由 --from-pack
      子进程按原路由执行）；
    - 其余源按 entry 开关与 --sources 限制过滤。
    """
    f = entry["fields"]
    srcs = []
    if not fcu._has_openalex_key():
        srcs.append("openalex")
    # europepmc / biorxiv / medrxiv 默认开（显式 false 才关，含字符串 "false"）；
    # arxiv 默认关（仅显式 true 才开）——与 ct_literature.py 的开关语义一致。
    if f.get("with_europepmc") is not False:
        srcs.append("europepmc")
    if f.get("with_biorxiv") is not False:
        srcs.append("biorxiv")
    if f.get("with_medrxiv") is not False:
        srcs.append("medrxiv")
    if _is_truthy(f.get("with_arxiv")):
        srcs.append("arxiv")
    raw = f.get("sources")
    if raw:
        want = {x.strip().lower() for x in str(raw).split(",") if x.strip()}
        srcs = [x for x in srcs if x in want]
    return srcs


def _pack_queries(entry, adapter, fcu):
    f = entry["fields"]
    # max_results 显式落地：entry 未指定时用 adapter 的 pack.default_max
    # （与 ct_literature.py --max 默认 50 对齐）——不依赖 Coze 端默认值，
    # 保证 pack 与非 pack 路径每源上限一致。
    try:
        dmax = int((adapter.get("pack") or {}).get("default_max") or 50)
    except (TypeError, ValueError):
        dmax = 50
    out = []
    for src in _pack_sources_for(entry, adapter, fcu):
        q = {"id": entry["id"], "source": src,
             "keyword": entry.get("pack_keyword") or "",
             "max_results": f.get("max") or dmax}
        for fkey, qkey in (("year_from", "year_from"), ("year_to", "year_to"),
                           ("date_from", "lit_date_from"),
                           ("date_to", "lit_date_to")):
            v = f.get(fkey)
            if v not in (None, "", False):
                q[qkey] = v
        out.append(q)
    return out


def _pack_payload(pkg, adapter, fcu, batch_id, pi, pkg_total, spec_file):
    queries = []
    for e in pkg:
        queries.extend(_pack_queries(e, adapter, fcu))
    querystr = json.dumps({
        "batch_id": batch_id,
        "package": "%d/%d" % (pi, pkg_total),
        "entries": [e["id"] for e in pkg],
        "n_queries": len(queries),
        "mode": PACK_MODE_NAME,
        "spec": os.path.basename(spec_file),
    }, ensure_ascii=False)
    return {
        "mode": PACK_MODE_NAME,
        "queries": queries,
        "log_feishu": True,   # 每包一条汇总留痕（取代逐 entry N 条）
        "query_origin": fcu._query_origin(),
        "skill_version": fcu._skill_version(),
        "entry_point": fcu.entry_point(),
        "locale": fcu._resolve_locale(),
        "params": {"user_language": fcu._resolve_locale()},
        "querystr": querystr,
    }


def _pack_send(payload, fcu, timeout):
    """一次 POST（主路径 /run + 异步轮询）。
    返回 (ok, data, unsupported, err)。出站实现已按 §16.9 收口到
    adapters/batch_pack_send.py，本处仅保留同签名薄封装（调用点零改动）。"""
    return _pack_send_impl(payload, fcu, timeout)
def _pack_classify(data):
    """响应分类：supported / unsupported / failed。
    supported：含 results 列表（新契约）；unsupported：端点按普通 search
    响应了（works/projects，无 results）——即忽略 batch_search 契约；
    failed：其余（error 等）。"""
    if not isinstance(data, dict):
        return "failed"
    if data.get("error"):
        return "failed"
    if isinstance(data.get("results"), list):
        return "supported"
    if any(k in data for k in ("works", "projects", "project_list")):
        return "unsupported"
    return "failed"


def _pack_results(data, fcu):
    """取出 results 列表；过大外置时回拉 S3（同 dispatch 口径）。"""
    if isinstance(data, dict) and data.get("s3_url") and not data.get("results"):
        pl = fcu._fetch_s3_projects(
            data["s3_url"], log_fn=lambda m: print(m, file=sys.stderr))
        if isinstance(pl, dict):
            for k in ("results", "projects"):
                if isinstance(pl.get(k), list):
                    return pl[k]
            return []
        return pl if isinstance(pl, list) else []
    res = data.get("results") if isinstance(data, dict) else None
    return res if isinstance(res, list) else []


def _pack_split(pkg, results, adapter, fcu):
    """按 entry id 拆回，写各 entry 的 pack_payloads.json（dispatch 同构的
    source payload 列表）。返回 (written_ids, missing_entries)。"""
    by_id = {}
    for item in results:
        if isinstance(item, dict):
            by_id.setdefault(str(item.get("id")), []).append(item)
    written, missing = [], []
    for e in pkg:
        items = by_id.get(e["id"]) or []
        payloads, errs = [], []
        df = e["fields"].get("date_from")
        dt = e["fields"].get("date_to")
        for it in items:
            if it.get("status") == "error" or it.get("error"):
                errs.append("%s: %s" % (it.get("source"), it.get("error")))
                continue
            works = it.get("works") or []
            src = it.get("source")
            if works:
                works = fcu._sanitize_works(works)
                if df or dt:
                    works, _dw = fcu.clip_by_date_window(works, df, dt, src)
            payloads.append({
                "source": fcu._display_source(src),
                "count": len(works),
                "works": works,
                "total_count": it.get("total_count", len(works)),
            })
        if not payloads:
            missing.append(e)
            if errs:
                e["reason"] = "; ".join(errs)[:300]
            continue
        pack_file = os.path.join(e["out_dir"], "pack_payloads.json")
        os.makedirs(e["out_dir"], exist_ok=True)
        with open(pack_file, "w", encoding="utf-8") as f:
            json.dump(payloads, f, ensure_ascii=False, indent=2)
        e["pack_payloads_file"] = pack_file
        written.append(e["id"])
    return written, missing


def _pack_cmd(entry):
    """在原 entry 命令中插入 --from-pack（其余 flag 原样保留，供 meta/审计）。"""
    cmd = list(entry.get("cmd") or [])
    pf = entry.get("pack_payloads_file")
    if not pf:
        return cmd
    try:
        i = cmd.index("--run")
    except ValueError:
        i = len(cmd)
    return cmd[:i] + ["--from-pack", pf] + cmd[i:]


def _print_pack_plan(entries, adapter, engine_script_dir, args):
    """dry-run 的打包计划预览（零联网；翻译只走本地词典）。"""
    try:
        fcu, tt = _pack_import_skill(engine_script_dir)
    except Exception as e:
        sys.stderr.write("[batch] pack 计划预览：技能模块加载失败 %s\n" % e)
        return
    kstats = _pack_prepare_keywords(entries, adapter, tt, online=False)
    pend = [e for e in entries if e["status"] == "pending"]
    if not pend:
        return
    size = max(1, args.pack_size)
    pkgs = [pend[i:i + size] for i in range(0, len(pend), size)]
    print("\n[batch] PACK 计划（dry-run 预览，未联网）：%d 条 entry → %d 包"
          "（≤%d 条/包，mode=%s）" % (len(pend), len(pkgs), size,
                                     PACK_MODE_NAME))
    print("[batch] 翻译预处理（本地词典；--run 时才走联网兜底）：新译 %d · "
          "原英文 %d · 部分未译 %d" % (kstats["translated"],
                                      kstats["already_en"],
                                      kstats["partial"]))
    for pi, pkg in enumerate(pkgs, 1):
        qs = []
        for e in pkg:
            qs.extend(_pack_queries(e, adapter, fcu))
        print("  包 %d/%d：%s" % (pi, len(pkgs),
                                  ", ".join(e["id"] for e in pkg)))
        print("      queries=%d  sources=%s"
              % (len(qs), sorted({q["source"] for q in qs})))
        for e in pkg[:2]:
            print("      · %s → keyword=%r" % (e["id"], e.get("pack_keyword")))


def _execute_pack(entries, adapter, engine_script_dir, args, batch_out,
                  spec_file, fmt, run_mode, _log, _manifest,
                  _execute_from_pack, _execute_normal, _run_all):
    """--pack 执行流。返回 None = 正常走完（回退 entry 已交常规执行）；
    返回 int = 提前中止的退出码。"""
    try:
        fcu, tt = _pack_import_skill(engine_script_dir)
    except Exception as e:
        sys.stderr.write("[batch] pack 模式加载技能模块失败：%s\n" % e)
        return 2
    kstats = _pack_prepare_keywords(entries, adapter, tt, online=True)
    print("[batch] pack 翻译预处理（一次完成）：新译 %d · 原英文 %d · 部分未译 %d"
          % (kstats["translated"], kstats["already_en"], kstats["partial"]))
    still = []
    for e in entries:
        if e["status"] != "pending":
            continue
        done_marker = os.path.join(e["out_dir"], ".done")
        if args.resume and os.path.isfile(done_marker):
            e["status"] = "resumed"
            e["reason"] = "跳过（--resume 且已完成）"
            e["n_results"] = _count_results(e["out_dir"])
            _log("  ↷ 跳过(已完成): %s" % e["id"])
            _manifest()
        else:
            still.append(e)
    if not still:
        return None
    batch_id = "%s_%s" % (os.path.splitext(os.path.basename(spec_file))[0],
                          _now_iso().replace(":", "").replace("-", ""))
    size = max(1, args.pack_size)
    pkgs = [still[i:i + size] for i in range(0, len(still), size)]
    print("[batch] PACK：%d 条 entry 分 %d 包（≤%d 条/包），逐包一次 Coze "
          "调用（mode=%s）" % (len(still), len(pkgs), size, PACK_MODE_NAME))
    fallback = []
    unsupported_seen = False
    retries = max(0, args.pack_retries)
    for pi, pkg in enumerate(pkgs, 1):
        payload = _pack_payload(pkg, adapter, fcu, batch_id, pi, len(pkgs),
                                spec_file)
        ok, data, unsup, last_err = False, None, False, None
        for attempt in range(1, retries + 2):
            ok, data, unsup, err = _pack_send(payload, fcu, args.timeout)
            last_err = err
            if ok or unsup:
                break
            _log("  ⚠ 包 %d/%d 第 %d 次发送失败：%s"
                 % (pi, len(pkgs), attempt, err))
            if attempt <= retries:
                time.sleep(min(30, 5 * attempt))
        if not ok and last_err and "AUTH-BLOCK" in str(last_err):
            sys.stderr.write("[batch] %s\n" % last_err)
            return 3
        kind = _pack_classify(data) if ok else \
            ("unsupported" if unsup else "failed")
        if kind != "supported":
            unsupported_seen = unsupported_seen or (kind == "unsupported")
            _log("  ⚠ 包 %d/%d 不可用（%s）：%s"
                 % (pi, len(pkgs), kind, last_err or "响应不符合契约"))
            if args.pack_fallback == "strict":
                sys.stderr.write(
                    "[batch] --pack-fallback strict：包 %d 失败，已中止。\n" % pi)
                return 3
            fallback.extend(pkg)
            continue
        results = _pack_results(data, fcu)
        written, missing = _pack_split(pkg, results, adapter, fcu)
        for e in pkg:
            if e["id"] in written:
                e["status"] = "packed"
                e["reason"] = "包 %d/%d 已取回" % (pi, len(pkgs))
            else:
                e["status"] = "error"
                e["reason"] = ((e.get("reason") or "").strip()
                               or "包内无该 entry 结果") + "（回退常规检索）"
                fallback.append(e)
        _log("  📦 包 %d/%d 完成：%d/%d 条 entry 取回（%d 个 source 查询）"
             % (pi, len(pkgs), len(written), len(pkg), len(payload["queries"])))
        _manifest()
        if pi < len(pkgs) and args.delay:
            time.sleep(args.delay)
    packed = [e for e in entries if e["status"] == "packed"]
    if packed:
        _log("[batch] %d 条 entry 进入 --from-pack 子进程管线（合并/去重/报告）..."
             % len(packed))
        _run_all(packed, _execute_from_pack)
    if fallback:
        for e in fallback:
            if e["status"] in ("error", "packed"):
                e["status"] = "pending"
                e["reason"] = "pack 回退：逐 entry 常规检索"
        _log("[batch] %d 条 entry 回退逐 entry 常规检索" % len(fallback))
        _run_all([e for e in fallback if e["status"] == "pending"],
                 _execute_normal)
    if unsupported_seen:
        _log("[batch] 提示：Coze 端暂不支持 %s 契约"
             "（见 references/batch_search_contract.md），本次已自动回退。"
             % PACK_MODE_NAME)
    return None


# --------------------------------------------------------------------------
# 主入口
# --------------------------------------------------------------------------

def run_batch(spec_file, adapter, engine_script_dir, args):
    spec_file = os.path.abspath(spec_file)
    if not os.path.isfile(spec_file):
        sys.stderr.write("[batch] ERROR: spec 文件不存在: %s\n" % spec_file)
        return 2

    with open(spec_file, "r", encoding="utf-8") as f:
        raw = f.read()
    fmt = _detect_format(spec_file, raw)
    if fmt == "yaml":
        doc = _load_yaml(spec_file)
        raw_entries = parse_yaml(doc, adapter.get("default_skill", "ct-literature"))
    else:
        raw_entries = parse_linelist(raw, adapter.get("default_skill", "ct-literature"))

    entries = []
    used_ids = {}
    for i, fe in enumerate(raw_entries):
        e = _build_entry_dict(fe, adapter, i)
        cid = e["id"]
        if cid in used_ids:
            used_ids[cid] += 1
            cid = "%s_%d" % (cid, used_ids[cid])
        else:
            used_ids[cid] = 1
        e["id"] = cid
        entries.append(e)

    batch_out = os.path.abspath(args.out_dir)
    os.makedirs(batch_out, exist_ok=True)
    skill_root = os.path.dirname(engine_script_dir)

    run_mode = "run" if args.run else "dry-run"
    lint = args.lint
    n_exec = sum(1 for e in entries if e["status"] == "pending")

    # 配额闸门
    quota = adapter.get("quota")
    if quota and args.run and not lint:
        est = n_exec * quota.get("per_entry_estimate", 1)
        warn_at = quota.get("warn_at", 90)
        if est > warn_at and not args.force and not args.max_total:
            sys.stderr.write(
                "\n[batch] ⚠️ 配额预警：预计 %d 次 API 命中"
                "（%s 免 key 上限 %s/天）。\n"
                "         使用 --force 强制，或 --max-total N 封顶。已中止（未联网）。\n"
                % (est, quota.get("api", "?"), quota.get("free_daily", "?")))
            return 3

    # --max-total 封顶（按出现顺序）
    if args.max_total is not None:
        cnt = 0
        for e in entries:
            if e["status"] != "pending":
                continue
            cnt += 1
            if cnt > args.max_total:
                e["status"] = "skipped"
                e["reason"] = "--max-total %d 封顶" % args.max_total

    # 构建命令（dry-run 与 run 共用）
    for e in entries:
        if e["status"] != "pending":
            continue
        eout = e["out_dir_override"] or os.path.join(batch_out, e["id"])
        e["out_dir"] = os.path.abspath(eout)
        e["cmd"] = _build_cmd(e, adapter, engine_script_dir, e["out_dir"])

    # Lint 模式
    if lint:
        ok = True
        for e in entries:
            mark = {"pending": "OK  ", "error": "ERR ", "skipped": "SKIP"}.get(e["status"], "????")
            if e["status"] != "pending":
                ok = False
            print("[lint] %s %-28s %s" % (mark, e["id"], e["reason"] or e["label"]))
        return 0 if ok else 1

    # Dry-run 模式
    if run_mode == "dry-run":
        print("\n[batch] DRY-RUN（默认安全预览，未联网）。确认计划无误后加 --run 执行。")
        print("[batch] spec=%s  format=%s  entries=%d  executable=%d\n"
              % (spec_file, fmt, len(entries), n_exec))
        for e in entries:
            if e["status"] == "pending":
                cmd_str = " ".join(shlex.quote(a) for a in e["cmd"])
                print("  • %s  [%s]\n      %s\n      out: %s"
                      % (e["label"], e["id"], cmd_str, e["out_dir"]))
            else:
                print("  - %s  [%s]  (%s: %s)"
                      % (e["label"], e["id"], e["status"], e["reason"]))
        if getattr(args, "pack", False):
            _print_pack_plan(entries, adapter, engine_script_dir, args)
        _write_manifest(batch_out, spec_file, fmt, run_mode, entries, adapter)
        print("\n[batch] 计划已写入 %s" % os.path.join(batch_out, "batch_manifest.json"))
        return 0

    # Run 模式
    mode_desc = ("pack 打包调用" if args.pack else
                 ("顺序执行" if args.concurrency <= 1
                  else "并发 %d" % args.concurrency))
    print("\n[batch] RUN 模式：开始执行 %d 个 entry（%s）..." % (n_exec, mode_desc))
    _write_manifest(batch_out, spec_file, fmt, run_mode, entries, adapter)
    errors_log = []
    _mlock = threading.Lock()
    _plock = threading.Lock()

    def _log(msg):
        with _plock:
            print(msg)

    def _manifest():
        with _mlock:
            _write_manifest(batch_out, spec_file, fmt, run_mode, entries, adapter)

    def _finalize_entry(e, rc, proc, dt):
        e["elapsed_sec"] = round(dt, 1)
        e["returncode"] = rc
        if rc == 0:
            e["status"] = "ok"
            try:
                with open(os.path.join(e["out_dir"], ".done"), "w",
                          encoding="utf-8") as f:
                    f.write(_now_iso())
            except OSError:
                pass
            e["n_results"] = _count_results(e["out_dir"])
            _log("  ✓ %s  (%.1fs, %s 条)" % (e["id"], dt, e["n_results"]))
        else:
            e["status"] = "error"
            errmsg = (proc.stderr or proc.stdout or "") if proc else "TIMEOUT"
            with _mlock:
                errors_log.append((e["id"], rc, errmsg))
            _log("  ✗ %s  (exit %s, %.1fs)" % (e["id"], rc, dt))
        _manifest()

    def _resume_skip(e):
        """--resume 且已完成 → 标记 resumed；返回 True 表示已跳过。"""
        done_marker = os.path.join(e["out_dir"], ".done")
        if args.resume and os.path.isfile(done_marker):
            e["status"] = "resumed"
            e["reason"] = "跳过（--resume 且已完成）"
            e["n_results"] = _count_results(e["out_dir"])
            _log("  ↷ 跳过(已完成): %s" % e["id"])
            _manifest()
            return True
        return False

    def _execute_normal(e):
        if _resume_skip(e):
            return
        os.makedirs(e["out_dir"], exist_ok=True)
        t0 = time.time()
        try:
            proc = subprocess.run(e["cmd"], cwd=skill_root, capture_output=True,
                                  text=True, timeout=args.timeout)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            rc, proc = -1, None
        _finalize_entry(e, rc, proc, time.time() - t0)

    def _execute_from_pack(e):
        if _resume_skip(e):
            return
        os.makedirs(e["out_dir"], exist_ok=True)
        cmd = _pack_cmd(e)
        t0 = time.time()
        try:
            proc = subprocess.run(cmd, cwd=skill_root, capture_output=True,
                                  text=True, timeout=args.timeout)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            rc, proc = -1, None
        if rc != 0:
            # from-pack 失败 → 原命令（常规联网检索）自动重试一次
            _log("  ⟳ %s from-pack 失败(exit %s)，回退常规检索重试"
                 % (e["id"], rc))
            with _mlock:
                errors_log.append((e["id"] + " [from-pack]", rc,
                                   (proc.stderr or proc.stdout or "")
                                   if proc else "TIMEOUT"))
            e["status"] = "pending"
            _execute_normal(e)
            return
        _finalize_entry(e, rc, proc, time.time() - t0)

    def _run_all(pending, fn):
        pending = list(pending)

        def _safe(e):
            # 单条目异常（out_dir 建不动、manifest 写失败等）不得拖垮整批：
            # 捕获 → 标记 error → 记 errors_log → 继续其余条目。
            try:
                fn(e)
            except Exception as ex:  # noqa: BLE001
                e["status"] = "error"
                e["reason"] = "执行异常: %s: %s" % (type(ex).__name__, ex)
                with _mlock:
                    errors_log.append((e["id"], -1,
                                       "%s: %s" % (type(ex).__name__, ex)))
                _log("  ✗ %s  (exception: %s: %s)"
                     % (e["id"], type(ex).__name__, ex))
                _manifest()

        if args.concurrency > 1 and len(pending) > 1:
            with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
                list(ex.map(_safe, pending))
        else:
            for i, e in enumerate(pending):
                if i and args.delay:
                    time.sleep(args.delay)
                _safe(e)

    if args.pack:
        rc_early = _execute_pack(entries, adapter, engine_script_dir, args,
                                 batch_out, spec_file, fmt, run_mode,
                                 _log, _manifest, _execute_from_pack,
                                 _execute_normal, _run_all)
        if rc_early is not None:
            _write_errors(batch_out, errors_log)
            _write_index_html(batch_out, entries, adapter)
            _write_summary_md(batch_out, entries, adapter, spec_file, fmt)
            _print_summary(entries, args.progress)
            return rc_early
    else:
        _run_all([e for e in entries if e["status"] == "pending"],
                 _execute_normal)

    _write_errors(batch_out, errors_log)
    _write_index_html(batch_out, entries, adapter)
    _write_summary_md(batch_out, entries, adapter, spec_file, fmt)
    _print_summary(entries, args.progress)
    return 0


def build_arg_parser():
    """供各技能 batch.py 复用的通用参数解析器。"""
    ap = argparse.ArgumentParser(
        description="ct-* 批量检索：按规格文件依次检索并聚合结果。")
    ap.add_argument("spec_file", help="检索关键词文档（行列表 .txt 或 YAML .yaml）")
    ap.add_argument("--run", action="store_true",
                    help="执行检索（联网）。默认仅打印计划（SAFE PREVIEW）。")
    ap.add_argument("--out-dir", default="./batch_out",
                    help="批量结果根目录（默认 ./batch_out，每 entry 一个子目录）")
    ap.add_argument("--lint", action="store_true",
                    help="仅校验规格，不执行、不联网")
    ap.add_argument("--max-total", type=int, default=None,
                    help="最多执行前 N 个有效 entry（配额封顶）")
    ap.add_argument("--force", action="store_true",
                    help="忽略配额预警强制执行")
    ap.add_argument("--resume", action="store_true",
                    help="跳过已完成（存在 .done 标记）的 entry，支持断点续跑")
    ap.add_argument("--delay", type=float, default=0.0,
                    help="每 entry 之间间隔秒数（限流友好）")
    ap.add_argument("--timeout", type=int, default=1800,
                    help="单 entry 超时秒数（默认 1800）")
    ap.add_argument("--concurrency", type=int, default=1,
                    help="entry 级并发数（默认 1 顺序执行；子进程层并发，"
                         "不改写各技能 CLI）")
    ap.add_argument("--pack", action="store_true",
                    help="打包模式：多个 entry 合成一次 Coze 调用"
                         "（mode=batch_search），Coze 端拆解逐条执行后批量返回；"
                         "端点不支持时自动回退逐 entry 模式")
    ap.add_argument("--pack-size", type=int, default=8,
                    help="每包 entry 数（默认 8；keyless 时 ≈40 个 source 查询，"
                         "贴近家族 50/批上限）")
    ap.add_argument("--pack-retries", type=int, default=1,
                    help="单包发送失败重试次数（默认 1）")
    ap.add_argument("--pack-fallback", default="auto",
                    choices=["auto", "strict"],
                    help="包失败时行为：auto=回退逐 entry 检索（默认）；"
                         "strict=中止")
    ap.add_argument("--progress", default="human", choices=["human", "json"])
    return ap
