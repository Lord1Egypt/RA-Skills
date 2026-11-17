#!/usr/bin/env python3
"""extsvc_client.py - Shared client for registry sources that need an EXTERNAL service.

WHY THIS EXISTS (architecture decision 2026-07-24):
  The ct-registry design rule is: NO local Playwright / headless browser. When a
  registry has no clean HTTP API (ISRCTN's query API returns 404; DRKS search is
  JS/redirect-based; ChiCTR has no public API), we delegate retrieval to an external
  workflow endpoint (the same Coze /run pattern already used by the archived / RETIRED 2026-08-12
  CDE/search_cde_workflow.py for China CDE). This module holds the shared machinery so each such source is a thin
  wrapper instead of 400 lines of duplication.

CONTRACT (mirrors CDE):
  - POST JSON to `<endpoint>` with `Authorization: Bearer <token>`.
  - The external service returns `{"records": [ ... ], "total_count": N, "run_id": ".."}`
    where each record is already in the shape the matching normalize adapter expects
    (ISRCTN -> isrctn/title/status/...; DRKS -> drks_id/title/status/...; CHICTR ->
    registry_id/title/url). The client just wraps it as
    `{"source": <SRC>, "records": [...], "total": N}`.
  - Token resolution (ct-base §5.236, no .dat file dependency):
    `--token` > env `CT_REGISTRY_COZE_TOKEN` (legacy alias `ICTRP_WORKFLOW_TOKEN`)
    > embedded public blob in `adapters/endpoint_token.py` (XOR+base64, shipped with the package).
    Public shared Coze workload-identity token; embedded per ct-base §5.239 / §5.243 so
    the published package works out-of-the-box (SkillHub strips *.dat silently).
    Legacy local `config/ictrp.dat` is only a silent fallback read (read-only; never persisted to disk).
  - SAFE PREVIEW by default: prints the exact request, performs NO network I/O unless --run.

EGRESS: only PUBLIC query terms are sent to the third-party endpoint. No confidential
subject / protocol / CRF data is ever transmitted (ct-base confidentiality red line).
"""
import argparse
import base64
import json
import os
import re
import sys
import time          # 异步轮询指数退避用
from pathlib import Path

import usage_guard

# 凭据解析改走 endpoint_token.py（ct-base §5：公开凭据内嵌 .py，不再依赖 .dat 文件）。
# 确保技能根目录在 sys.path，以便 `from endpoint_token import ...`（adapters/ 下同目录兄弟模块）。
import sys as _sys
from pathlib import Path as _Path
_SKILL_ROOT = _Path(__file__).resolve().parent.parent
# adapters/ modules import the pure-local shared util `usage_guard` from
# scripts/, and endpoint_token lives in adapters/ (same dir as this file). Expose both so
# `import usage_guard` / `from endpoint_token import ...` resolve whether this
# file is run as a subprocess (sys.path[0] == adapters/) or imported.
for _d in (str(_SKILL_ROOT), os.path.join(str(_SKILL_ROOT), "scripts")):
    if _d not in _sys.path:
        _sys.path.insert(0, _d)
from endpoint_token import (
    get_secret as _keys_get_secret,
    get_token as _keys_get_token,
)


def get_token(cli_token=None, token_env=None):
    """统一端点（coze）token。委托给 endpoint_token.get_token（ct-base §5）。

    解析优先级：CLI(--token) > env(CT_REGISTRY_COZE_TOKEN / 遗留 ICTRP_WORKFLOW_TOKEN)
    > 内嵌混淆 blob；不再读取/写入 config/ictrp.dat 作为发布机制。
    """
    return _keys_get_token(cli_token, token_env)


# Outbound authorization gate (ct-base §5.212). The script only emits an
# [AUTH-BLOCK] signal; the agent shows the unified confirmation prompt and, on
# user approval, persists the endpoint into config.json['auto_approve_endpoints'].
# The script NEVER mutates config.json itself.
_SESSION_AUTHORIZED = set()
_HOME_CONFIG_JSON = os.path.expanduser(
    "~/.workbuddy/skills/ct-registry/config/config.json")


def _authorized_endpoints():
    """汇总候选配置来源的 auto_approve_endpoints（取并集）：
    1) 应用/技能根相对路径 ``<root>/config/config.json`` —— 云端 publish-dist
       部署布局。云沙箱 home=/root 且工作目录为 /workspace，家目录路径必然
       缺失；发布包（build_publish.py 白名单）自带 config/config.json。
    2) 用户家目录 ``~/.workbuddy/skills/ct-registry/config/config.json`` ——
       本地技能开发布局（历史行为，保持不变；本地两个候选实为同一文件）。
    2026-10-13 修复：此前只读家目录绝对路径，云端部署的 WHO ICTRP / CDE /
    ChiCTR / ISRCTN / DRKS 出站 100% 被 AUTH-BLOCK，CT.gov 一遇网络抖动即
    整体静默返回 0 条（exit 0 + 空报告，前端无感知）。
    """
    out = set()
    for p in (os.path.join(str(_SKILL_ROOT), "config", "config.json"),
              _HOME_CONFIG_JSON):
        try:
            cfg = json.loads(Path(p).read_text(encoding="utf-8"))
            eps = cfg.get("auto_approve_endpoints") or []
            if isinstance(eps, list):
                out.update(str(e) for e in eps)
        except (OSError, json.JSONDecodeError):
            continue
    return out


def _check_outbound_authorization(endpoint):
    if endpoint in _SESSION_AUTHORIZED:
        return True
    if endpoint in _authorized_endpoints():
        return True
    sys.stderr.write(
        f"[AUTH-BLOCK] outbound to {endpoint} requires user confirmation.\n")
    return False


# ---- ct-base §5.50: 出站 payload 发送前剥离 PII（身份证 / 手机号 / 邮箱）----
_PII_PATTERNS = [
    (re.compile(r"\b1[3-9]\d{9}\b"), "<phone>"),              # 大陆手机号
    (re.compile(r"\b\d{17}[\dXx]\b"), "<id-card>"),            # 身份证
    (re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"), "<email>"),
]


def _sanitize_text(s: str) -> str:
    for pat, repl in _PII_PATTERNS:
        s = pat.sub(repl, s)
    return s


def _sanitize_payload(payload):
    """递归剥离出站 payload 中的 PII（ct-base §5.50）。只改值、不改结构。"""
    if isinstance(payload, dict):
        return {k: _sanitize_payload(v) for k, v in payload.items()}
    if isinstance(payload, list):
        return [_sanitize_payload(v) for v in payload]
    if isinstance(payload, str):
        return _sanitize_text(payload)
    return payload


# ---- ct-base §5.49: 代理残留自动重试（Windows 系统代理残留 → ProxyError/WinError 10061）----
def _request(method, url, **kwargs):
    """requests 封装：首次失败若为 ProxyError/ConnectionError（系统代理残留），
    自动绕过系统代理（proxies 置空）直连重试一次；直连仍失败则原样抛出。"""
    import requests
    try:
        return requests.request(method, url, **kwargs)
    except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
        kwargs.setdefault("proxies", {"http": None, "https": None})
        return requests.request(method, url, **kwargs)


def print_preview(source, endpoint, token, payload, out):
    print(f"[{source.lower()}-extsvc][PREVIEW] No network request will be made. Add --run to execute.")
    print(f"[{source.lower()}-extsvc][PREVIEW] Endpoint : {endpoint}")
    print(f"[{source.lower()}-extsvc][PREVIEW] Auth     : "
          f"Bearer <token set>" if token else "none (endpoint returns 401)")
    print(f"[{source.lower()}-extsvc][PREVIEW] Payload:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"[{source.lower()}-extsvc][PREVIEW] Output   : {out}")


def _status_guidance(code):
    if code == 200:
        return None  # success for all Coze ext-svc endpoints
    if code == 401:
        return "401 = missing/malformed Authorization header; send exactly 'Bearer <token>'."
    if code == 403:
        return "403 = token rejected (corrupted/revoked/invalid); re-issue only if it recurs (localized token is long-lived)."
    if code == 500:
        return "500 = payload schema error from the workflow; check field types."
    if code == 503:
        return "503 = auth gateway transient; retry (re-issue token only if 403 recurs)."
    return f"{code} = unexpected status."


def _resolve_out_path(out):
    """Normalize the --out path and ensure its parent directory exists.

    Robustness fix (2026-08-09): when the caller passes a POSIX-style path
    produced by Git Bash (e.g. `/tmp/ct_retest/A.json`), native Windows Python
    resolves it to `C:\\tmp\\ct_retest\\A.json`. If that directory does not
    exist the write fails with a raw traceback. We abspath + expanduser and
    create the parent dir up front so the write always lands somewhere
    predictable (and on Windows the POSIX path is anchored to the CWD drive).
    """
    p = os.path.expanduser(out)
    p = os.path.abspath(p)
    parent = os.path.dirname(p)
    if parent:
        try:
            os.makedirs(parent, exist_ok=True)
        except OSError:
            pass  # best-effort; the open() below will surface a clear error
    return p


def _write_out_json(out, obj):
    """Write the result dict as JSON; surface a clear error instead of a raw traceback."""
    try:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        return True
    except OSError as e:
        print(f"[extsvc-client][ERROR] 无法写入输出文件 {out}: {e}")
        print(f"[extsvc-client][ERROR] 请检查路径/父目录是否存在、是否有写权限；"
              f"建议改用绝对路径（如 C:/Users/you/out.json）。")
        return False


def _write_timeout(out, source, timeout, phase):
    """统一写 is_timeout=True 占位输出（提交阶段 / 轮询阶段超时共用）。"""
    out_obj = {
        "source": source,
        "records": [],
        "total": 0,
        "run_id": None,
        "is_timeout": True,
        "error_msg": f"timeout after {timeout}s ({phase}) (Coze search exceeded wait limit)",
    }
    _write_out_json(out, out_obj)
    print(f"[{source.lower()}-extsvc][TIMEOUT] 检索超过 {timeout}s 未返回，已超时退出（is_timeout=True）。")
    print(f"[{source.lower()}-extsvc][GUIDE] 数据可能不全：建议改用高级检索 / 缩小关键字，"
          f"或换其他注册源交叉验证。")


def _finalize_async(source, endpoint_base, data, out, timeout, run_id):
    """解析 /run/status 的最终结果（兼容两种返回形态）。"""
    if data.get("status") == "failed":
        sys.exit(f"[{source.lower()}-extsvc][ERROR] remote run failed: {data.get('error')}")
    if data.get("status") == "cancelled":
        _write_timeout(out, source, timeout, "cancelled")
        return

    # completed：data 可能是 {status, result} 或直接是 result dict
    result = data.get("result", data)

    # 兼容两种形态：
    #  (a) 平台已重命名：{"records": [...], "total_count": N, "run_id": ".."}
    #  (b) graph 原始输出：{"project_list": "<json string>", "total_count": N}
    records = result.get("records")
    if records is None and result.get("project_list"):
        try:
            inner = json.loads(result["project_list"])
            records = inner.get("projects") or inner.get("records") or []
        except Exception:
            records = []
    records = records or []

    # 透传节点层 P0 超时中断标记
    is_timeout = bool(result.get("is_timeout"))

    out_obj = {
        "source": source,
        "records": records,
        "total": result.get("total_count", len(records)),
        "run_id": result.get("run_id") or run_id,
        "is_timeout": is_timeout,
    }
    if is_timeout:
        print(f"[{source.lower()}-extsvc][TIMEOUT] 远程检索超时中断，返回已抓部分数据 {len(records)} 条（is_timeout=True）。")
    _write_out_json(out, out_obj)
    print(f"[{source.lower()}-extsvc] {len(records)} records -> {out}")


def _run_async_poll(source, endpoint, token, run_id, out, timeout,
                    finalize=None, on_timeout=None):
    """异步模式：轮询 /run/status/{run_id}，指数退避，总上限 timeout 秒。

    finalize: 可选回调，签名 (source, endpoint_base, data, out, timeout, run_id)；
        默认 _finalize_async。ictrp 等适配器可注入专属 finalize（如额外解析 payload）。
    on_timeout: 可选回调，签名 (out, source, timeout, phase)；默认 _write_timeout。
    """
    import requests
    endpoint_base = endpoint.rsplit("/run", 1)[0]
    status_url = f"{endpoint_base.rstrip('/')}/run/status/{run_id}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    deadline = time.time() + timeout
    wait = 5.0
    while time.time() < deadline:
        try:
            # ct-base §5.49：代理残留自动重试（ProxyError/ConnectionError → 绕代理直连）
            r = _request("GET", status_url, headers=headers, timeout=10)
        except requests.exceptions.Timeout:
            time.sleep(min(wait, max(1, deadline - time.time())))
            wait = min(wait * 2, 30)
            continue
        except requests.RequestException as e:
            sys.exit(f"[{source.lower()}-extsvc][ERROR] poll request failed: {e}")
        try:
            data = r.json()
        except Exception:
            data = {}
        status = data.get("status")
        if status == "running":
            time.sleep(min(wait, max(1, deadline - time.time())))
            wait = min(wait * 2, 30)
            continue
        if finalize is None:
            _finalize_async(source, endpoint_base, data, out, timeout, run_id)
        else:
            finalize(source, endpoint_base, data, out, timeout, run_id)
        return
    if on_timeout is None:
        _write_timeout(out, source, timeout, "poll")
    else:
        on_timeout(out, source, timeout, "poll")


def run(source, endpoint, token, payload, out, timeout):
    out = _resolve_out_path(out)
    import requests
    if not _check_outbound_authorization(endpoint):
        print(f"[{source.lower()}-extsvc][INFO] outbound not authorized this session; "
              f"see AUTH-BLOCK above.")
        return
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        print(f"[{source.lower()}-extsvc][WARN] no token -> endpoint returns 401")

    # ===== 阶段 1：提交（应毫秒级返回 run_id；用短超时，避免卡在网关）=====
    # ct-base §5.50：出站 payload 发送前脱敏（身份证/手机号/邮箱）；
    # ct-base §5.49：代理残留自动重试（ProxyError/ConnectionError → 绕代理直连）。
    safe_payload = _sanitize_payload(payload)
    try:
        submit_resp = _request("POST", endpoint, headers=headers, json=safe_payload, timeout=30)
    except requests.exceptions.Timeout:
        # 提交本身超时极罕见（异步 /run 只做 fire-and-forget）；按原超时逻辑降级
        _write_timeout(out, source, timeout, "submit")
        return
    except requests.RequestException as e:
        sys.exit(f"[{source.lower()}-extsvc][ERROR] request failed: {e}")

    # 探测响应形态：异步协议返回 {status:accepted, run_id} → 轮询；否则按同步协议
    try:
        submit_data = submit_resp.json()
    except Exception:
        submit_data = {}

    if submit_data.get("status") == "accepted" and submit_data.get("run_id"):
        _run_async_poll(source, endpoint, token, submit_data["run_id"], out, timeout)
        return

    # ===== 同步协议分支（Coze 端未部署 P4 时走这里，逻辑同原版）=====
    print(f"[{source.lower()}-extsvc] HTTP {submit_resp.status_code}")
    guide = _status_guidance(submit_resp.status_code)
    if guide:
        print(f"[{source.lower()}-extsvc][GUIDE] {guide}")
    if submit_resp.status_code != 200:
        print(f"[{source.lower()}-extsvc] body: {submit_resp.text[:600]}")
        print(f"[{source.lower()}-extsvc] no successful response -> output NOT written.")
        return
    try:
        data = submit_resp.json()
    except Exception:
        data = {"raw": submit_resp.text}
    records = data.get("records") or []
    out_obj = {"source": source, "records": records, "total": data.get("total_count", len(records)),
               "run_id": data.get("run_id"), "is_timeout": False}
    _write_out_json(out, out_obj)
    print(f"[{source.lower()}-extsvc] {len(records)} records -> {out}")


def make_base_parser(source, default_endpoint):
    ap = argparse.ArgumentParser(
        description=f"{source} search via external workflow (no local browser).")
    ap.add_argument("--q", help="free-text query / 检索词")
    ap.add_argument("--token", help="Bearer token (else env / config file)")
    ap.add_argument("--endpoint", default=default_endpoint,
                    help="workflow /run 基址（异步化后用于拼接 /run/status/{run_id} 轮询）")
    ap.add_argument("--out", default=f"{source.lower()}_extsvc.json")
    ap.add_argument("--run", action="store_true", help="actually POST (default preview)")
    ap.add_argument("--timeout", type=int, default=600,
                    help="轮询总超时上限（秒），默认 600 = 10 分钟；提交阶段单独用 30s 短超时。超时退出时返回值 is_timeout=True")
    ap.add_argument("--demand-id",
                    help="检索需求标识：同一 demand_id 当日只计 1 次配额（WHO+CDE/各源合并、"
                         "关键词微调/重复检索均不重复计数）。省略则每次调用各计 1 次。")
    # ct-base §20.12：计费身份标识预留透传（可选；服务端 extra='ignore' 安全忽略）
    ap.add_argument("--account-id",
                    help="（可选）付费账户标识，透传至统一端点（ct-base §20.12 计费预留；"
                         "服务端未部署计费中间件时忽略，向后兼容、不阻断）")
    ap.add_argument("--billing-token",
                    help="（可选）服务端签发的计费令牌，透传至统一端点")
    return ap


def _attach_billing(payload, args):
    """把调用方显式提供的计费标识并入出站 payload（ct-base §20.12）。

    payload 为 build_payload 返回的 dict；仅注入非空字段。服务端未部署计费时
    由 `extra='ignore'` 忽略，不改变既有检索行为。
    """
    if not isinstance(payload, dict):
        return
    if getattr(args, "account_id", None):
        payload["account_id"] = args.account_id
    if getattr(args, "billing_token", None):
        payload["billing_token"] = args.billing_token


def dispatch(source, default_endpoint, args, build_payload):
    """Common main() tail for the thin wrappers."""
    payload = build_payload(args)
    # ct-base §20.12：计费身份标识透传（可选，服务端 extra='ignore' 安全忽略）
    _attach_billing(payload, args)
    token = get_token(args.token)
    if not args.run:
        print_preview(source, args.endpoint, token, payload, args.out)
        return
    # §5.212 outbound authorization gate (before quota check + network I/O).
    if not _check_outbound_authorization(args.endpoint):
        return
    # Daily shared-resource guard: caps WHO/CDE/ChiCTR/ISRCTN/DRKS retrieval at 100/day,
    # charged ONCE per demand_id (sources merged; tweaks/repeats within a demand are free).
    # When the parent orchestrator (ct_registry.py) already performed the single
    # per-demand check (parallel-safe), it sets CT_DEMAND_CHECKED=1 so we skip the
    # check here and NEVER double-count across concurrently launched endpoint
    # subprocesses (a cross-process race would otherwise inflate the quota).
    if os.environ.get("CT_DEMAND_CHECKED") != "1":
        allowed, _remaining, guard_msg = usage_guard.check(
            demand_id=getattr(args, "demand_id", None) or os.environ.get("CT_DEMAND_ID"), source_label=source)
        print(guard_msg)
        if not allowed:
            return
    run(source, args.endpoint, token, payload, args.out, args.timeout)
