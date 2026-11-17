#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config_health_check.py — Convbox-DiagClaw Prof.Skill 配置与 API 健康自检工具
（聚焦凭证与接口连通，区别于店铺「经营健康」分析）。

两阶段：
  阶段一 · 配置完整性 —— CONVBOX_API_KEY 是否就绪、access.yaml 是否合法。
  阶段二 · API 健康   —— 按 access.yaml 对全部端点逐个真实探测，
                         并按其字段定义逐项校验响应 schema。

凭证只读自环境变量 CONVBOX_API_KEY，绝不打印 Key 本体。
依赖：PyYAML（标准成熟开源库）。其余仅用 Python 标准库。

退出码：0 全部通过（可含 SKIP/INFO）；1 存在 WARN（schema 偏差等，--strict 下视为失败）；2 存在 FAIL。
"""

import argparse
import datetime as _dt
import json
import os
import sys
import urllib.error
import urllib.request

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "缺少依赖 PyYAML。请先安装：pip install pyyaml --break-system-packages\n"
    )
    sys.exit(2)

ENV_KEY = "CONVBOX_API_KEY"

OK, WARN, FAIL, SKIP, INFO = "OK", "WARN", "FAIL", "SKIP", "INFO"
# Keep status markers ASCII-safe so the checker works in Windows GBK consoles.
_ICON = {OK: "OK", WARN: "WARN", FAIL: "FAIL", SKIP: "SKIP", INFO: "INFO"}


class Check:
    """单条检查结果。"""

    def __init__(self, name, status, detail=""):
        self.name = name
        self.status = status
        self.detail = detail

    def as_dict(self):
        return {"name": self.name, "status": self.status, "detail": self.detail}


# ---------------------------------------------------------------------------
# 阶段一 · 配置完整性
# ---------------------------------------------------------------------------
def check_config(access_path):
    """校验 API Key 与 access.yaml；返回 (checks, access_doc_or_None)。"""
    checks = []

    # 1) API Key 就绪（只判存在与非空，绝不回显）
    key = os.environ.get(ENV_KEY, "")
    if not key.strip():
        checks.append(
            Check(
                f"环境变量 {ENV_KEY}",
                FAIL,
                f"未配置或为空。请在环境中设置 {ENV_KEY}（不要写入任何包内文件）。",
            )
        )
    else:
        checks.append(
            Check(f"环境变量 {ENV_KEY}", OK, f"已配置（长度 {len(key.strip())}，已脱敏）")
        )

    # 2) access.yaml 存在且可解析
    if not os.path.isfile(access_path):
        checks.append(Check("access.yaml 存在", FAIL, f"未找到：{access_path}"))
        return checks, None
    try:
        with open(access_path, "r", encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        checks.append(Check("access.yaml 解析", FAIL, f"YAML 语法错误：{exc}"))
        return checks, None
    checks.append(Check("access.yaml 解析", OK, access_path))

    # 3) access.yaml 必需结构
    if not isinstance(doc, dict):
        checks.append(Check("access.yaml 结构", FAIL, "顶层不是映射"))
        return checks, None

    meta = doc.get("meta") or {}
    base_url = meta.get("base_url")
    if not base_url:
        checks.append(Check("meta.base_url", FAIL, "缺失"))
    else:
        checks.append(Check("meta.base_url", OK, base_url))

    auth = meta.get("auth") or {}
    header_name = auth.get("header_name")
    env_from = auth.get("value_from_env")
    if not header_name:
        checks.append(Check("meta.auth.header_name", FAIL, "缺失"))
    else:
        checks.append(Check("meta.auth.header_name", OK, header_name))
    if env_from and env_from != ENV_KEY:
        checks.append(
            Check(
                "meta.auth.value_from_env",
                WARN,
                f"access 声明取自 {env_from}，与脚本默认 {ENV_KEY} 不一致",
            )
        )

    endpoints = doc.get("endpoints") or []
    if not isinstance(endpoints, list) or not endpoints:
        checks.append(Check("endpoints", FAIL, "为空或非列表"))
        return checks, None
    # 端点最小字段
    bad = [
        ep.get("id", "<no-id>")
        for ep in endpoints
        if not (ep.get("id") and ep.get("path") and ep.get("method"))
    ]
    if bad:
        checks.append(
            Check("endpoints 字段完整性", FAIL, f"缺 id/path/method：{', '.join(bad)}")
        )
    else:
        checks.append(
            Check("endpoints 字段完整性", OK, f"{len(endpoints)} 个端点定义齐全")
        )

    return checks, doc


# ---------------------------------------------------------------------------
# 阶段二 · API 健康 + schema 校验
# ---------------------------------------------------------------------------
def _expected_fields(ep):
    """从端点定义推断「单条记录应含字段集合」。优先 response_fields，否则取样例。"""
    rf = ep.get("response_fields")
    if rf:
        return {f["name"] for f in rf if isinstance(f, dict) and f.get("name")}
    # 退而从 sample_response 推断
    sample = (ep.get("sample_response") or {}).get("data")
    rec = _first_record(sample)
    return set(rec.keys()) if isinstance(rec, dict) else set()


def _find_container(data):
    """返回 (容器键, 列表) —— data 中承载记录列表的键（records/goals…）；无则 (None, None)。"""
    if isinstance(data, dict):
        for key in ("records", "goals", "list", "rows"):
            if isinstance(data.get(key), list):
                return key, data[key]
    return None, None


def _first_record(data):
    """取一条代表性记录用于字段比对。"""
    _, lst = _find_container(data)
    if lst:
        return lst[0] if lst else {}
    if isinstance(data, dict):
        return data  # 汇总型端点：data 自身即记录
    return {}


def _build_request_body(ep, account_map, recent_window):
    """组装最小可用请求体。返回 (body_or_None, skip_reason_or_None)。"""
    body = dict(ep.get("sample_request") or {})
    ep_id = ep.get("id")

    # 透传端点需要真实 account_id；无连接账户则跳过
    if ep_id in ("meta_query", "google_query"):
        platform = "facebook" if ep_id == "meta_query" else "google"
        acc = account_map.get(platform)
        if not acc:
            return None, f"无已连接的 {platform} 账户，跳过透传探测"
        body["account_id"] = acc

    # 可选：把日期窗口收敛到最近 N 天，降低取数量（仍可能空数据，属正常）
    if recent_window and ep_id not in ("meta_query", "google_query"):
        if "start_date" in body and "end_date" in body:
            today = _dt.date.today()
            body["start_date"] = (today - _dt.timedelta(days=recent_window)).isoformat()
            body["end_date"] = today.isoformat()
    return body, None


def _post(base_url, path, header_name, key, body, timeout):
    """发起一次 POST，返回 (status_code, parsed_json_or_None, raw_or_error_text)。"""
    url = base_url.rstrip("/") + "/" + path.lstrip("/")
    data = json.dumps(body or {}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header(header_name, key)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            code = resp.getcode()
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace") if exc.fp else ""
        return exc.code, _try_json(raw), raw
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return None, None, f"{type(exc).__name__}: {exc}"
    return code, _try_json(raw), raw


def _try_json(text):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return None


def probe_endpoints(doc, key, timeout, recent_window):
    """对全部端点探测；返回检查列表。"""
    checks = []
    meta = doc["meta"]
    base_url = meta["base_url"]
    header_name = (meta.get("auth") or {}).get("header_name") or "ApiKey"
    endpoints = doc["endpoints"]

    # 预解析已连接账户（供透传端点取 account_id）
    account_map = {}
    conn = next((e for e in endpoints if e.get("id") == "connection_source"), None)
    if conn:
        _, parsed, _ = _post(
            base_url, conn["path"], header_name, key, {}, timeout
        )
        if parsed and parsed.get("code") == 1:
            for rec in ((parsed.get("data") or {}).get("records") or []):
                pt, aid = rec.get("platform_type"), rec.get("account_id")
                if pt and aid and pt not in account_map:
                    account_map[pt] = aid

    for ep in endpoints:
        ep_id = ep.get("id", "<no-id>")
        body, skip_reason = _build_request_body(ep, account_map, recent_window)
        if skip_reason:
            checks.append(Check(f"[{ep_id}] 探测", SKIP, skip_reason))
            continue

        code, parsed, raw = _post(base_url, ep["path"], header_name, key, body, timeout)

        # 传输层
        if code is None:
            checks.append(Check(f"[{ep_id}] 连通性", FAIL, raw))
            continue
        if code < 200 or code >= 300:
            checks.append(
                Check(f"[{ep_id}] HTTP", FAIL, f"HTTP {code}：{(raw or '')[:200]}")
            )
            continue
        if parsed is None:
            checks.append(
                Check(f"[{ep_id}] 响应解析", FAIL, f"非 JSON 响应：{(raw or '')[:200]}")
            )
            continue

        # 响应封套
        env_issues = []
        for field in ("code", "message", "data"):
            if field not in parsed:
                env_issues.append(field)
        if parsed.get("code") != 1:
            checks.append(
                Check(
                    f"[{ep_id}] 业务状态",
                    FAIL,
                    f"code={parsed.get('code')} message={parsed.get('message')!r}",
                )
            )
            continue
        if env_issues:
            checks.append(
                Check(f"[{ep_id}] 响应封套", WARN, f"缺字段：{', '.join(env_issues)}")
            )

        # schema 字段校验（access 为「代表性 schema」，偏差记 WARN 而非 FAIL）
        expected = _expected_fields(ep)
        data = parsed.get("data")
        _, lst = _find_container(data)
        if lst is not None and len(lst) == 0:
            checks.append(
                Check(
                    f"[{ep_id}] schema",
                    OK,
                    "连通正常，区间内无记录（空数据属正常，不据空编造结论）",
                )
            )
            continue

        actual = set(_first_record(data).keys())
        if not actual:
            checks.append(
                Check(f"[{ep_id}] schema", WARN, "响应无可校验记录结构")
            )
            continue

        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        if missing:
            detail = f"缺字段 {len(missing)}/{len(expected)}：{', '.join(missing)}"
            if extra:
                detail += f"；额外字段：{', '.join(extra)}"
            checks.append(Check(f"[{ep_id}] schema", WARN, detail))
        else:
            note = f"{len(expected)} 个定义字段齐全"
            if extra:
                note += f"（另含未文档化字段：{', '.join(extra)}）"
            checks.append(Check(f"[{ep_id}] schema", OK, note))

    return checks


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------
def render(stage1, stage2, as_json):
    all_checks = stage1 + stage2
    counts = {s: sum(1 for c in all_checks if c.status == s) for s in (OK, WARN, FAIL, SKIP, INFO)}

    if as_json:
        out = {
            "summary": counts,
            "config": [c.as_dict() for c in stage1],
            "api": [c.as_dict() for c in stage2],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return counts

    print("=" * 64)
    print("Convbox-DiagClaw · Prof.Skill 健康自检")
    print("=" * 64)
    print("\n阶段一 · 配置完整性")
    print("-" * 64)
    for c in stage1:
        print(f"  [{_ICON[c.status]}] {c.name}: {c.detail}")
    print("\n阶段二 · API 健康 + Schema 校验")
    print("-" * 64)
    if stage2:
        for c in stage2:
            print(f"  [{_ICON[c.status]}] {c.name}: {c.detail}")
    else:
        print("  （阶段一未通过，已跳过 API 探测）")
    print("\n" + "-" * 64)
    print(
        f"汇总：{counts[OK]} 通过 · {counts[WARN]} 警告 · "
        f"{counts[FAIL]} 失败 · {counts[SKIP]} 跳过"
    )
    print("=" * 64)
    return counts


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    default_access = os.path.normpath(os.path.join(here, "..", "..", "access.yaml"))

    p = argparse.ArgumentParser(description="Convbox-DiagClaw Prof.Skill 配置与 API 健康自检")
    p.add_argument("--access", default=default_access, help="access.yaml 路径")
    p.add_argument("--timeout", type=float, default=15.0, help="单次请求超时（秒）")
    p.add_argument(
        "--recent-window",
        type=int,
        default=0,
        metavar="N",
        help="将日期型端点窗口收敛为最近 N 天（默认 0=用 access 样例日期）",
    )
    p.add_argument("--config-only", action="store_true", help="只做阶段一，不发请求")
    p.add_argument("--json", action="store_true", help="以 JSON 输出")
    p.add_argument("--strict", action="store_true", help="WARN 也视为失败（CI 用）")
    args = p.parse_args(argv)

    stage1, doc = check_config(args.access)
    stage1_fail = any(c.status == FAIL for c in stage1)

    stage2 = []
    if not args.config_only and not stage1_fail and doc is not None:
        key = os.environ[ENV_KEY].strip()
        stage2 = probe_endpoints(doc, key, args.timeout, args.recent_window)

    counts = render(stage1, stage2, args.json)

    if counts[FAIL] > 0:
        return 2
    if args.strict and counts[WARN] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
