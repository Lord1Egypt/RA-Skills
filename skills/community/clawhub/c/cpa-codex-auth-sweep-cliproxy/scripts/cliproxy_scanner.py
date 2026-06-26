#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from urllib.parse import quote, urlparse

DEFAULT_BASE_URL = os.environ.get("CLIPROXY_BASE_URL", "")
DEFAULT_MGMT_KEY = os.environ.get("CLIPROXY_MANAGEMENT_KEY", "")
DEFAULT_AUTH_FILES_ENDPOINT = os.environ.get("CLIPROXY_AUTH_FILES_ENDPOINT", "/v0/management/auth-files")
DEFAULT_API_CALL_ENDPOINT = os.environ.get("CLIPROXY_API_CALL_ENDPOINT", "/v0/management/api-call")
DEFAULT_AUTH_DELETE_ENDPOINT = os.environ.get("CLIPROXY_AUTH_DELETE_ENDPOINT", "/v0/management/auth-files")
DEFAULT_PROBE_URL = os.environ.get("CODEX_PROBE_URL", "https://chatgpt.com/backend-api/codex/responses")
DEFAULT_ALLOWED_PROBE_HOSTS = os.environ.get("CLIPROXY_ALLOWED_PROBE_HOSTS", "chatgpt.com")
DEFAULT_WORKERS = int(os.environ.get("SCAN_WORKERS", "80"))
DEFAULT_PROBE_WORKERS = int(os.environ.get("PROBE_WORKERS", str(DEFAULT_WORKERS)))
DEFAULT_DELETE_WORKERS = int(os.environ.get("DELETE_WORKERS", "16"))
DEFAULT_MAX_ACTIVE_PROBES = int(os.environ.get("MAX_ACTIVE_PROBES", "120"))

INVALID_TOKEN_KEYWORDS = [
    '"status": 401',
    '"status":401',
    'token_invalidated',
    'token_revoked',
    'invalid auth',
    'unauthorized',
    'Your authentication token has been invalidated.',
    'Encountered invalidated oauth token for user',
]


@dataclass
class AuthEntry:
    name: str
    provider: str
    auth_index: str
    status_message: str
    unavailable: bool


@dataclass
class CheckResult:
    name: str
    auth_index: str
    status_code: int | None
    unauthorized_401: bool
    weekly_quota_zero: bool
    error: str
    response_preview: str
    reason: str = ""


def _json_request(url: str, method: str, headers: dict[str, str], body_obj: dict | None, timeout: int, insecure: bool) -> tuple[int, dict | str]:
    data = None
    if body_obj is not None:
        data = json.dumps(body_obj, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, headers=headers, data=data, method=method.upper())
    ctx = ssl._create_unverified_context() if insecure else ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            code = r.getcode()
            text = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        code = e.code
        text = e.read().decode("utf-8", "replace")
    if not text:
        return code, ""
    try:
        return code, json.loads(text)
    except Exception:
        return code, text


def _is_weekly_quota_zero(status_code: int | None, text: str) -> bool:
    t = (text or "").lower()
    markers = ["weekly", "week", "per week", "weekly quota", "weekly limit", "week limit", "本周", "周限额", "周额度"]
    qwords = ["quota", "limit", "exceeded", "reached", "用尽", "耗尽", "超出"]
    if status_code == 429 and any(m in t for m in markers) and any(q in t for q in qwords):
        return True
    return any(m in t for m in markers) and any(q in t for q in qwords)


def _probe_payload() -> dict:
    return {
        "model": "gpt-5",
        "instructions": "ping",
        "store": False,
        "input": [{"role": "user", "content": [{"type": "input_text", "text": "ping"}]}],
        "max_output_tokens": 1,
    }


def _match_static_reason(auth: AuthEntry) -> str:
    s = (auth.status_message or "")
    sl = s.lower()
    for kw in INVALID_TOKEN_KEYWORDS:
        if kw.lower() in sl:
            return f"status_message:{kw}"
    return ""


def _list_codex_auths(base_url: str, key: str, endpoint: str, insecure: bool) -> list[AuthEntry]:
    url = base_url.rstrip("/") + endpoint
    code, resp = _json_request(
        url,
        "GET",
        {"Authorization": f"Bearer {key}", "Accept": "application/json"},
        None,
        timeout=30,
        insecure=insecure,
    )
    if code >= 400:
        raise RuntimeError(f"list auth-files failed: {code} {resp}")
    files = resp.get("files") if isinstance(resp, dict) else []
    out: list[AuthEntry] = []
    for f in files or []:
        if not isinstance(f, dict):
            continue
        name = str(f.get("name") or "").strip()
        provider = str(f.get("provider") or f.get("type") or "").strip().lower()
        auth_index = str(f.get("auth_index") or "").strip()
        if not name or not auth_index:
            continue
        if provider == "codex" or "codex" in name.lower():
            out.append(
                AuthEntry(
                    name=name,
                    provider=provider or "codex",
                    auth_index=auth_index,
                    status_message=str(f.get("status_message") or ""),
                    unavailable=bool(f.get("unavailable") or False),
                )
            )
    return out


def _probe_via_management_api_call(base_url: str, key: str, api_call_endpoint: str, probe_url: str, auth: AuthEntry, insecure: bool) -> CheckResult:
    url = base_url.rstrip("/") + api_call_endpoint
    token_magic = "$" + "TOKEN$"
    body = {
        "auth_index": auth.auth_index,
        "method": "POST",
        "url": probe_url,
        "header": {
            "Authorization": "Bearer " + token_magic,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "codex_cli_rs/0.98.0 (cliproxy-api-call-sweep)",
        },
        "data": json.dumps(_probe_payload(), ensure_ascii=False),
    }
    try:
        code, resp = _json_request(
            url,
            "POST",
            {"Authorization": f"Bearer {key}", "Accept": "application/json", "Content-Type": "application/json"},
            body,
            timeout=60,
            insecure=insecure,
        )
    except Exception as e:  # noqa: BLE001
        return CheckResult(auth.name, auth.auth_index, None, False, False, f"api_call error: {e}", "", "probe_error")

    if code >= 400:
        return CheckResult(auth.name, auth.auth_index, None, False, False, f"management api_call failed: {code}", str(resp)[:220], "management_api_call_failed")

    if not isinstance(resp, dict):
        return CheckResult(auth.name, auth.auth_index, None, False, False, "invalid api_call response", str(resp)[:220], "invalid_api_call_response")

    status_code = resp.get("status_code")
    body_text = resp.get("body") if isinstance(resp.get("body"), str) else json.dumps(resp.get("body"), ensure_ascii=False)
    low = (body_text or "").lower()

    unauthorized = (status_code == 401) or ("invalid auth" in low) or ("revoked" in low)
    weekly_zero = _is_weekly_quota_zero(status_code, body_text or "")
    reason = ""
    if status_code == 401:
        reason = "probe_status_401"
    elif "invalid auth" in low or "revoked" in low:
        reason = "probe_invalid_or_revoked"
    elif weekly_zero:
        reason = "probe_weekly_quota_zero"
    return CheckResult(auth.name, auth.auth_index, status_code, unauthorized, weekly_zero, "", (body_text or "")[:220], reason)


def _delete_auth_file(base_url: str, key: str, endpoint: str, name: str, insecure: bool) -> bool:
    url = f"{base_url.rstrip('/')}{endpoint}?name={quote(name, safe='')}"
    code, _ = _json_request(
        url,
        "DELETE",
        {"Authorization": f"Bearer {key}", "Accept": "application/json"},
        None,
        timeout=30,
        insecure=insecure,
    )
    return code < 400


def _normalize_hosts_csv(raw: str) -> set[str]:
    return {h.strip().lower() for h in (raw or "").split(",") if h.strip()}


def _assert_probe_url_safe(probe_url: str, allowed_hosts_csv: str, unsafe_allow: bool) -> None:
    parsed = urlparse(probe_url)
    if parsed.scheme != "https":
        raise SystemExit("Security check failed: --probe-url must use https")
    host = (parsed.hostname or "").lower()
    allowed = _normalize_hosts_csv(allowed_hosts_csv)
    if not host:
        raise SystemExit("Security check failed: --probe-url host is empty")
    if host not in allowed:
        if unsafe_allow:
            return
        raise SystemExit(
            f"Security check failed: probe host '{host}' not in allowlist {sorted(allowed)}. "
            "Use --allow-unsafe-probe-host only if you fully trust this host."
        )


def _progress(msg: str, enabled: bool) -> None:
    if not enabled:
        return
    print(msg, file=sys.stderr, flush=True)


def main() -> int:
    p = argparse.ArgumentParser(description="Scan Codex auth via CLI Proxy management api-call (supports runtime refresh/quota view)")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    p.add_argument("--management-key", default=DEFAULT_MGMT_KEY)
    p.add_argument("--auth-files-endpoint", default=DEFAULT_AUTH_FILES_ENDPOINT)
    p.add_argument("--api-call-endpoint", default=DEFAULT_API_CALL_ENDPOINT)
    p.add_argument("--auth-delete-endpoint", default=DEFAULT_AUTH_DELETE_ENDPOINT)
    p.add_argument("--probe-url", default=DEFAULT_PROBE_URL)
    p.add_argument("--allowed-probe-hosts", default=DEFAULT_ALLOWED_PROBE_HOSTS, help="Comma-separated allowlist for probe host, default: chatgpt.com")
    p.add_argument("--allow-unsafe-probe-host", action="store_true", help="Allow probe host outside allowlist (DANGEROUS)")
    p.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    p.add_argument("--probe-workers", type=int, default=DEFAULT_PROBE_WORKERS)
    p.add_argument("--delete-workers", type=int, default=DEFAULT_DELETE_WORKERS)
    p.add_argument("--max-active-probes", type=int, default=DEFAULT_MAX_ACTIVE_PROBES)
    p.add_argument("--delete-401", action="store_true")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification (DANGEROUS)")
    p.add_argument("--allow-insecure-tls", action="store_true", help="Second confirmation for --insecure")
    p.add_argument("--progress", action="store_true", help="Print live progress logs")
    p.add_argument("--progress-every", type=int, default=10, help="Progress report interval, default: 10")
    p.add_argument("--output-json", action="store_true")
    args = p.parse_args()

    if not args.base_url or not args.management_key:
        raise SystemExit("Missing required params: --base-url and --management-key")
    if args.workers < 1 or args.probe_workers < 1 or args.delete_workers < 1:
        raise SystemExit("--workers/--probe-workers/--delete-workers must be >= 1")
    if args.max_active_probes < 0:
        raise SystemExit("--max-active-probes must be >= 0")
    if args.progress_every < 1:
        raise SystemExit("--progress-every must be >= 1")
    if args.insecure and not args.allow_insecure_tls:
        raise SystemExit("Security check failed: --insecure requires explicit --allow-insecure-tls")
    _assert_probe_url_safe(args.probe_url, args.allowed_probe_hosts, args.allow_unsafe_probe_host)

    _progress("[skill] 开始执行扫描任务", args.progress)
    auths = _list_codex_auths(args.base_url, args.management_key, args.auth_files_endpoint, args.insecure)
    total = len(auths)
    _progress(f"[skill] 已获取 auth files：{total} 条", args.progress)

    results: list[CheckResult] = []

    # Stage 1: static quick match from status_message
    static_invalid: list[CheckResult] = []
    active_candidates: list[AuthEntry] = []
    for a in auths:
        reason = _match_static_reason(a)
        if reason:
            static_invalid.append(CheckResult(a.name, a.auth_index, None, True, False, "", a.status_message[:220], reason))
        else:
            active_candidates.append(a)

    # Stage 2: active probe with cap
    if args.max_active_probes > 0 and len(active_candidates) > args.max_active_probes:
        _progress(f"[skill] 主动探测候选 {len(active_candidates)} 条，仅探测前 {args.max_active_probes} 条", args.progress)
        active_candidates = active_candidates[: args.max_active_probes]

    _progress(f"[skill] 开始校验：静态命中 {len(static_invalid)}，主动探测 {len(active_candidates)}", args.progress)
    results.extend(static_invalid)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.probe_workers) as ex:
        futs = [ex.submit(_probe_via_management_api_call, args.base_url, args.management_key, args.api_call_endpoint, args.probe_url, a, args.insecure) for a in active_candidates]
        done = 0
        step = args.progress_every
        total_probe = len(active_candidates)
        for f in concurrent.futures.as_completed(futs):
            results.append(f.result())
            done += 1
            if done == 1 or done % step == 0 or done == total_probe:
                _progress(f"[skill] 正在处理第 {done} 条 / 共 {total_probe} 条", args.progress)

    _progress("[skill] 全部校验完成", args.progress)

    to_delete = [r.name for r in results if r.unauthorized_401]
    deleted = 0
    if args.delete_401 and args.yes and to_delete:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.delete_workers) as ex:
            futs = [ex.submit(_delete_auth_file, args.base_url, args.management_key, args.auth_delete_endpoint, name, args.insecure) for name in to_delete]
            for f in concurrent.futures.as_completed(futs):
                if f.result():
                    deleted += 1

    management_quota_exhausted = sum(
        1
        for a in auths
        if a.unavailable and (("quota" in a.status_message.lower()) or ("限额" in a.status_message) or ("额度" in a.status_message))
    )

    status_buckets: dict[str, int] = {}
    for r in results:
        k = str(r.status_code) if r.status_code is not None else "none"
        status_buckets[k] = status_buckets.get(k, 0) + 1

    reason_buckets: dict[str, int] = {}
    for r in results:
        k = r.reason or ""
        if not k:
            continue
        reason_buckets[k] = reason_buckets.get(k, 0) + 1

    payload = {
        "summary": {
            "total": len(results),
            "unauthorized_401": sum(1 for r in results if r.unauthorized_401),
            "weekly_quota_zero": sum(1 for r in results if r.weekly_quota_zero),
            "ok": sum(1 for r in results if r.status_code is not None and 200 <= r.status_code < 300),
            "errors": sum(1 for r in results if r.error),
            "management_quota_exhausted": management_quota_exhausted,
            "status_code_buckets": status_buckets,
            "reason_buckets": reason_buckets,
            "static_matched": len(static_invalid),
            "active_probed": len(active_candidates),
        },
        "deletion": {
            "requested": bool(args.delete_401),
            "target_count": len(to_delete),
            "confirmed": bool(args.delete_401 and args.yes),
            "deleted_count": deleted,
        },
        "results": [asdict(r) for r in results],
    }

    if args.output_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        s = payload["summary"]
        print(f"total={s['total']} invalid={s['unauthorized_401']} weekly_zero={s['weekly_quota_zero']} ok={s['ok']} errors={s['errors']} mgmt_quota_exhausted={s['management_quota_exhausted']}")
        print(f"status_code_buckets={json.dumps(s['status_code_buckets'], ensure_ascii=False)}")
        print(f"reason_buckets={json.dumps(s['reason_buckets'], ensure_ascii=False)}")

    return 1 if payload["summary"]["unauthorized_401"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
