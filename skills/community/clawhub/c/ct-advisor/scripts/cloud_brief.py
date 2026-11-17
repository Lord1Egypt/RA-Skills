#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ct-advisor → ct-search 端点 brief 薄客户端（2026-11-09，契约 v1.0.0）。

定位
====
把 need_tool 执行卡中 ct-registry / ct-safety / ct-literature 三技能的**执行位置**
从「本地技能 CLI」上移到 Coze ct-search 端点内的三个聚合 source。本模块只负责
「构造信封 / 发请求 / 校验三条护栏 / 确定性渲染」，不含任何检索或统计实现。

两条调用通道共用本契约（2026-11-09 15:51 之后云端节点已归档）：
  * 本地委托通道：``handle_need_tool.execute_card``；
  * 并行预取通道：``orchestrate._fire_prefetch``（Coze 等待窗口内执行）。
  两者都只在开关显式打开时调用；Coze 云端包内零凭据、无节点。

红线
====
* 开关 ``CT_ADVISOR_CLOUD_BRIEF`` **默认关闭**（2026-11-09 晚间架构重评）：
  客户端已可直接调用三个技能本体并拿到完整交付物，brief 只给非审计级速览，
  故默认主路径改为 handoff；未开时调用方 100% 走 handoff / 原执行卡。
* 任何失败（未部署 / 无凭证 / 超时 / status=error / 契约违约）一律返回 None，
  由调用方回落本地 need_tool 执行卡（ct-base §20.19.7 红线 2）。绝不伪造数据。
* ``doc_context`` 绝不进入本通道（F33 数据出域红线）。
* 参数白名单锁死，发送前二次过滤；响应缺 disclaimer / suggest_skill /
  suggest_text 任一即判契约违约（护栏 1/2/3）。

用法
====
    python scripts/cloud_brief.py --self-test          # 离线自测，不触网
    python scripts/cloud_brief.py --dry-run --tool ct-safety --params '{"drug":"aspirin","event":"hepatic failure"}'
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
for _p in (str(SCRIPT_DIR), str(SKILL_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

CONTRACT_PATH = SKILL_ROOT / "config" / "brief_contract.json"


# ── 契约与开关 ──────────────────────────────────────────────────────────────

def load_contract() -> dict:
    with open(CONTRACT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def enabled(contract: Optional[dict] = None) -> bool:
    """本地直连为 opt-in，默认关闭；显式 on 值才启用（否则走 handoff / 执行卡）。

    2026-11-09 晚间架构重评：客户端已可直接调用技能本体，brief 降级为快答路径，
    默认主路径是 handoff。Coze 云端仍不持有凭据、不发起需凭据的外部调用。
    """
    cfg = (contract or load_contract())["switch"]
    val = os.environ.get(cfg["local_env"], "").strip().lower()
    if val:
        if val in {v.lower() for v in cfg.get("off_values", [])}:
            return False
        if val in {v.lower() for v in cfg["on_values"]}:
            return True
    return bool(cfg["enabled_default"])


def source_for(tool: str, contract: dict) -> Optional[str]:
    return contract["skill_to_source"].get(tool)


def filter_params(tool: str, params: dict, contract: dict) -> Dict[str, Any]:
    """护栏 1：本地发送前二次过滤，未知键直接丢弃（云端另做 fail-closed 拒绝）。"""
    source = source_for(tool, contract)
    if not source:
        return {}
    allowed = contract["param_allowlist"][source]
    return {k: v for k, v in (params or {}).items() if k in allowed}


def _query_origin(card: dict) -> str:
    """ct-base §8.6：必须由客户端生成；绝不在此兜底造一个假 hash。"""
    origin = str(card.get("query_origin") or "").strip()
    if origin:
        return origin
    env = os.environ.get("CT_QUERY_ORIGIN", "").strip()
    if env:
        return env
    return ""


# ── 凭证 ────────────────────────────────────────────────────────────────────

def get_token() -> str:
    """共享公开凭据：env 覆盖优先，其次 ct-advisor 内嵌 blob（不依赖 ct-registry 已安装）。"""
    env = os.environ.get("CT_ADVISOR_BRIEF_TOKEN", "").strip()
    if env:
        return env
    try:
        from adapters import coze_token_embedded
        return coze_token_embedded.get_search_token() or ""
    except Exception:  # noqa: BLE001 - 凭证不可用时静默回落，由调用方降级
        return ""


# ── 信封与传输 ──────────────────────────────────────────────────────────────

def build_envelope(tool: str, params: dict, card: dict, contract: dict) -> dict:
    source = source_for(tool, contract)
    clean = filter_params(tool, params, contract)
    return {
        "source": source,
        "keyword": json.dumps(clean, ensure_ascii=False),
        "mode": contract["envelope"]["mode"],
        "query_origin": _query_origin(card),
        "skill_version": "ct-advisor/1.3.39",
        "locale": card.get("locale") or "zh-CN",
        "params": {"user_language": card.get("locale") or "zh-CN"},
    }


def _dig_payload(obj: Any) -> Optional[dict]:
    """Coze /run 与 /stream_run 的出参形态不一：递归找出含 brief/status 的信封。"""
    if isinstance(obj, dict):
        if "status" in obj and ("brief" in obj or "project_list" in obj or "projects" in obj):
            return obj
        for val in obj.values():
            got = _dig_payload(val)
            if got is not None:
                return got
    elif isinstance(obj, list):
        for val in obj:
            got = _dig_payload(val)
            if got is not None:
                return got
    elif isinstance(obj, str):
        s = obj.strip()
        if s.startswith("{") and ("brief" in s or "project_list" in s):
            try:
                return _dig_payload(json.loads(s))
            except ValueError:
                return None
    return None


def _parse_body(raw: str) -> Optional[dict]:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        obj = json.loads(raw)
    except ValueError:
        # SSE：逐行 data: {...}，取最后一个可解析且含业务字段的
        obj = None
        for line in raw.splitlines():
            line = line.strip()
            if not line.startswith("data:"):
                continue
            chunk = line[5:].strip()
            if not chunk or chunk == "[DONE]":
                continue
            try:
                cand = json.loads(chunk)
            except ValueError:
                continue
            if _dig_payload(cand) is not None:
                obj = cand
        if obj is None:
            return None
    return _dig_payload(obj)


def _cache_key(source: str, params: dict, contract: dict) -> str:
    import hashlib
    canon = json.dumps(params, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"))
    return hashlib.sha256(("%s|%s" % (source, canon)).encode("utf-8")).hexdigest()


def _cache_dir():
    import tempfile
    from pathlib import Path
    return Path(tempfile.gettempdir()) / "ct-advisor-brief-cache"


def _cache_on(contract: dict) -> bool:
    cfg = contract.get("cache") or {}
    off = {"0", "false", "no", "off"}
    return bool(cfg.get("enabled_default")) and \
        os.environ.get("CT_ADVISOR_BRIEF_CACHE", "").strip().lower() not in off


def _cache_get(source: str, params: dict, contract: dict) -> Optional[dict]:
    """P0-2：命中未过期的完整成功信封则跳过网络；任何异常静默回源。"""
    if not _cache_on(contract):
        return None
    import time
    p = _cache_dir() / (_cache_key(source, params, contract) + ".json")
    try:
        if not p.is_file():
            return None
        if (time.time() - p.stat().st_mtime) > int(contract["cache"]["ttl_sec"]):
            return None
        obj = json.loads(p.read_text(encoding="utf-8"))
        return obj if isinstance(obj, dict) and obj.get("status") == "ok" else None
    except Exception:  # noqa: BLE001 - 缓存是纯优化，不得影响主链路
        return None


def _cache_put(source: str, params: dict, payload: dict, contract: dict) -> None:
    """只缓存完整成功：error / accepted / partial_sources 非空一律不缓存。"""
    if not _cache_on(contract):
        return
    brief = payload.get("brief") or {}
    if payload.get("status") != "ok" or (brief.get("partial_sources") or []):
        return
    try:
        d = _cache_dir()
        d.mkdir(parents=True, exist_ok=True)
        p = d / (_cache_key(source, params, contract) + ".json")
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        tmp.replace(p)  # 原子覆盖，不删除历史文件
    except Exception:  # noqa: BLE001
        pass


def post(url: str, envelope: dict, token: str, timeout: int) -> Optional[dict]:
    body = json.dumps(envelope, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer %s" % token,
                 "Accept": "application/json, text/event-stream"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return _parse_body(resp.read().decode("utf-8", errors="replace"))


def run_brief(tool: str, params: dict, card: dict,
              contract: Optional[dict] = None) -> Optional[dict]:
    """返回校验通过的 brief 信封；任何失败返回 None（调用方回落本地执行卡）。"""
    cfg = contract or load_contract()
    source = source_for(tool, cfg)
    if not source:
        return None
    token = get_token()
    if not token:
        sys.stderr.write("[cloud-brief] 无 ct-search 凭证，回落本地执行卡\n")
        return None
    origin = _query_origin(card)
    if not origin:
        sys.stderr.write("[cloud-brief] query_origin 缺失（ct-base §8.6 禁止服务端兜底），回落本地执行卡\n")
        return None
    clean = filter_params(tool, params, cfg)
    for key in cfg["sources"][source]["required"]:
        if not clean.get(key):
            sys.stderr.write("[cloud-brief] 必填参数 %s 缺失，回落本地执行卡\n" % key)
            return None
    # P0-2：本地短 TTL 缓存命中即跳过网络（key 不含 query_origin）
    cached = _cache_get(source, clean, cfg)
    if cached is not None:
        return cached
    envelope = build_envelope(tool, params, card, cfg)
    # P0-1：按 source 分档超时；网关 60s 硬顶，统一 90s 永远等不到
    timeout = int(cfg["endpoint"]["per_source_timeout_sec"].get(
        source, cfg["endpoint"]["timeout_sec"]))
    try:
        payload = post(cfg["endpoint"]["run_url"], envelope, token, timeout)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write("[cloud-brief] %s 请求失败：%s，回落本地执行卡\n"
                         % (source, type(exc).__name__))
        return None
    if not payload:
        sys.stderr.write("[cloud-brief] 响应无法解析，回落本地执行卡\n")
        return None
    # 异步 accepted：本地通道不实现轮询（主通道是云端节点），直接回落
    if payload.get("status") == "accepted":
        sys.stderr.write("[cloud-brief] 异步任务已受理，本地通道不轮询，回落本地执行卡\n")
        return None
    if not validate_response(source, payload, cfg):
        return None
    _cache_put(source, clean, payload, cfg)
    return payload


def validate_response(source: str, payload: dict, contract: dict) -> bool:
    """三条护栏的客户端侧校验：缺任一即判契约违约，绝不静默放行。"""
    if payload.get("status") != "ok":
        sys.stderr.write("[cloud-brief] status=%s / error=%s，回落本地执行卡\n"
                         % (payload.get("status"), payload.get("error")))
        return False
    if payload.get("brief_kind") != source:
        sys.stderr.write("[cloud-brief] brief_kind 不匹配，回落本地执行卡\n")
        return False
    expected_allow = contract["param_allowlist"][source]
    if payload.get("param_allowlist") != expected_allow:
        sys.stderr.write("[cloud-brief] 护栏 1 违约：param_allowlist 不一致，回落本地执行卡\n")
        return False
    if payload.get("disclaimer") != contract["disclaimer_text"]:
        sys.stderr.write("[cloud-brief] 护栏 2 违约：disclaimer 缺失或不一致，回落本地执行卡\n")
        return False
    skill = contract["sources"][source]["skill"]
    if payload.get("suggest_skill") != skill or \
       payload.get("suggest_text") != contract["suggest_text"][skill]:
        sys.stderr.write("[cloud-brief] 护栏 3 违约：suggest_footer 缺失或不一致，回落本地执行卡\n")
        return False
    return True


# ── 确定性渲染（缝合层原样透出，无 LLM 改写）────────────────────────────────

def render_brief_text(source: str, payload: dict, contract: dict) -> str:
    brief = payload.get("brief") or {}
    lines = ["## 补充数据速览（Coze ct-search · `%s`）" % source, ""]
    kind = source

    if kind == "advisor_registry_brief":
        lines.append("- 检索词：`%s`｜命中 %s 条｜数据源：%s"
                     % (brief.get("query", ""), brief.get("total_hits", 0),
                        ", ".join(brief.get("sources_used") or []) or "无"))
        for label, key in (("分期分布", "phase_counts"), ("状态分布", "status_counts"),
                           ("主要申办方", "top_sponsors")):
            block = brief.get(key) or {}
            if block:
                lines.append("- %s：%s" % (label, "；".join(
                    "%s %s" % (k, v) for k, v in list(block.items())[:8])))
        for t in (brief.get("sample_trials") or [])[:5]:
            lines.append("  - %s ｜ %s ｜ %s" %
                         (t.get("id") or "-", (t.get("title") or "")[:90],
                          t.get("status") or "-"))
    elif kind == "advisor_safety_brief":
        lines.append("- 药物：`%s`｜事件：`%s`" %
                     (brief.get("drug") or "", brief.get("event") or "未指定"))
        counts = brief.get("counts_2x2") or {}
        if counts:
            lines.append("- 2×2 计数：a=%s b=%s c=%s d=%s" %
                         tuple(counts.get(k, "-") for k in ("a", "b", "c", "d")))
        m = brief.get("measures") or {}
        if m.get("prr") is not None:
            lines.append("- PRR=%s（95%%CI %s）｜ROR=%s（95%%CI %s）"
                         % (m.get("prr"), m.get("prr_ci95"), m.get("ror"), m.get("ror_ci95")))
        if m.get("note"):
            lines.append("- %s" % m["note"])
    elif kind == "advisor_literature_brief":
        lines.append("- 主题：`%s`｜命中 %s 条｜去重后 %s 篇｜数据源：%s"
                     % (brief.get("topic", ""), brief.get("total_hits", 0),
                        brief.get("unique_works", 0),
                        ", ".join(brief.get("sources_used") or []) or "无"))
        for w in (brief.get("top_works") or [])[:5]:
            lines.append("  - %s（%s，被引 %s）%s"
                         % ((w.get("title") or "")[:100], w.get("year") or "-",
                            w.get("cited_by_count", 0),
                            " DOI:" + w["doi"] if w.get("doi") else ""))

    if brief.get("partial_sources"):
        lines.append("- ⚠️ 部分数据源未完成：%s（已如实标注，未补齐）"
                     % ", ".join(brief["partial_sources"]))
    if brief.get("note"):
        lines.append("- %s" % brief["note"])
    lines += ["", payload["disclaimer"], "", payload["suggest_text"]]
    return "\n".join(lines)


def try_cloud_brief(card: dict) -> Optional[str]:
    """供 handle_need_tool.execute_card 调用：返回可缝合文本，或 None 表示应回落。"""
    cfg = load_contract()
    if not enabled(cfg):
        return None
    tool = card.get("need_tool") or ""
    if not source_for(tool, cfg):
        return None
    source = source_for(tool, cfg)
    payload = run_brief(tool, card.get("params") or {}, card, cfg)
    if payload is None:
        return None
    return render_brief_text(source, payload, cfg)


# ── 离线自测 ────────────────────────────────────────────────────────────────

def self_test() -> int:
    cfg = load_contract()
    ok = True

    def chk(label: str, cond: bool) -> None:
        nonlocal ok
        print("  [%s] %s" % ("PASS" if cond else "FAIL", label))
        ok = ok and cond

    print("cloud_brief 离线自测（不触网）")
    print("-" * 62)
    chk("本地直连默认关闭（opt-in 降级路径）", cfg["switch"]["enabled_default"] is False)
    chk("未设环境变量时 enabled() 为 False", enabled(cfg) is False)
    os.environ["CT_ADVISOR_CLOUD_BRIEF"] = "1"
    chk("显式 on 值可整条开启", enabled(cfg) is True)
    os.environ["CT_ADVISOR_CLOUD_BRIEF"] = "0"
    chk("显式 off 值可整条关闭", enabled(cfg) is False)
    os.environ.pop("CT_ADVISOR_CLOUD_BRIEF", None)
    chk("3 个 source 均已登记", len(cfg["sources"]) == 3)
    chk("白名单规模锁死 8/6/6",
        [len(v) for v in cfg["param_allowlist"].values()] == [8, 6, 6])
    chk("skill_to_source 覆盖三技能",
        set(cfg["skill_to_source"]) == {"ct-registry", "ct-safety", "ct-literature"})
    chk("doc_context 被明确禁止", "doc_context" in cfg["envelope"])
    chk("三条护栏齐备", len(cfg["guardrails"]) == 4)  # 含 enforcement

    # 白名单过滤
    dirty = {"drug": "aspirin", "event": "x", "trend": True, "case_level": 200}
    clean = filter_params("ct-safety", dirty, cfg)
    chk("护栏 1：越界参数被过滤", clean == {"drug": "aspirin", "event": "x"})

    # 响应校验：构造合规 / 违约信封
    src = "advisor_safety_brief"
    good = {
        "status": "ok", "brief_kind": src, "brief": {"drug": "aspirin"},
        "param_allowlist": cfg["param_allowlist"][src],
        "disclaimer": cfg["disclaimer_text"],
        "suggest_skill": "ct-safety",
        "suggest_text": cfg["suggest_text"]["ct-safety"],
    }
    chk("合规响应通过校验", validate_response(src, dict(good), cfg))
    for label, mut in (("护栏 2：缺 disclaimer", {"disclaimer": ""}),
                       ("护栏 3：缺 suggest_footer", {"suggest_text": ""}),
                       ("护栏 1：白名单不一致", {"param_allowlist": []}),
                       ("status=error 回落", {"status": "error"})):
        bad = dict(good)
        bad.update(mut)
        chk(label, not validate_response(src, bad, cfg))

    # 渲染
    text = render_brief_text(src, good, cfg)
    chk("渲染含免责与导流", cfg["disclaimer_text"] in text and "@skill:ct-safety" in text)
    chk("渲染不含 doc_context", "doc_context" not in text)

    # 信封
    card = {"need_tool": "ct-safety", "params": dirty,
            "query_origin": "sha256:" + "a" * 64, "locale": "zh-CN"}
    env = build_envelope("ct-safety", dirty, card, cfg)
    chk("信封 source 正确", env["source"] == src)
    chk("信封 keyword 为白名单内 JSON",
        set(json.loads(env["keyword"])) <= set(cfg["param_allowlist"][src]))
    chk("信封携带客户端 query_origin", env["query_origin"].startswith("sha256:"))
    chk("信封不含 doc_context", "doc_context" not in env)

    # P0-1 / P0-2：分档超时与短期缓存（隔离到临时目录，不污染真实缓存）
    per = cfg["endpoint"]["per_source_timeout_sec"]
    chk("按 source 分档超时齐备且均 < 网关 60s",
        set(per) == set(cfg["sources"]) and all(0 < v < 60 for v in per.values()))
    chk("缓存默认开启 / TTL 600s",
        cfg["cache"]["enabled_default"] is True and cfg["cache"]["ttl_sec"] == 600)
    import tempfile
    from pathlib import Path as _Path
    _orig_dir = _cache_dir
    with tempfile.TemporaryDirectory(prefix="wb-brief-cache-") as _td:
        globals()["_cache_dir"] = lambda: _Path(_td)
        os.environ.pop("CT_ADVISOR_BRIEF_CACHE", None)
        _cache_put(src, {"drug": "aspirin"}, dict(good), cfg)
        chk("完整成功信封可命中缓存",
            _cache_get(src, {"drug": "aspirin"}, cfg) == good)
        bad_partial = dict(good)
        bad_partial["brief"] = {"partial_sources": ["who"]}
        _cache_put(src, {"drug": "ibuprofen"}, bad_partial, cfg)
        chk("partial_sources 不写入缓存",
            _cache_get(src, {"drug": "ibuprofen"}, cfg) is None)
        bad_err = dict(good)
        bad_err["status"] = "error"
        _cache_put(src, {"drug": "naproxen"}, bad_err, cfg)
        chk("status=error 不写入缓存",
            _cache_get(src, {"drug": "naproxen"}, cfg) is None)
        os.environ["CT_ADVISOR_BRIEF_CACHE"] = "0"
        chk("env=0 可关闭缓存", _cache_get(src, {"drug": "aspirin"}, cfg) is None)
        os.environ.pop("CT_ADVISOR_BRIEF_CACHE", None)
    globals()["_cache_dir"] = _orig_dir
    print("-" * 62)
    print("结论：%s" % ("✅ 全部通过" if ok else "❌ 存在 FAIL"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="ct-advisor → ct-search brief 薄客户端")
    ap.add_argument("--self-test", action="store_true", help="离线自测，不触网")
    ap.add_argument("--dry-run", action="store_true", help="只打印信封，不发请求")
    ap.add_argument("--tool", default="", help="技能标识")
    ap.add_argument("--params", default="{}", help="执行卡参数 JSON")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    cfg = load_contract()
    try:
        params = json.loads(args.params)
    except ValueError as e:
        print("params JSON 解析失败: %s" % e, file=sys.stderr)
        return 2
    card = {"need_tool": args.tool, "params": params,
            "query_origin": "sha256:" + hashlib.sha256(b"dry-run").hexdigest(),
            "locale": "zh-CN"}
    if not source_for(args.tool, cfg):
        print("非 brief 技能：%s" % args.tool, file=sys.stderr)
        return 2
    print(json.dumps(build_envelope(args.tool, params, card, cfg),
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
