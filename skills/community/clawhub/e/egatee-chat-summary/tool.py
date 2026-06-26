#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import uuid
from collections import Counter
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

import requests


def get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env: {name}")
    return value


def get_optional_env(name: str) -> str:
    return os.getenv(name, "").strip()


def infer_base_url_by_api_key(api_key: str) -> str:
    """
    根据 apiKey 前缀自动选择环境：
    - uat_*  -> http://api.uat.egatee.net
    - 其他   -> https://api.egatee.com
    """
    k = (api_key or "").strip()
    if k.lower().startswith("uat_"):
        return "http://api.uat.egatee.net"
    return "https://api.egatee.com"


def get_notify_base_url(api_key: str) -> str:
    # 允许显式覆盖（比如临时走 matata-global 域名/私有网关）
    explicit = get_optional_env("EGATEE_NOTIFY_BASE_URL")
    if explicit:
        return explicit.rstrip("/")
    inferred = infer_base_url_by_api_key(api_key).rstrip("/")
    _debug_log(f"EGATEE_NOTIFY_BASE_URL not set, inferred base_url={inferred}")
    return inferred


def build_headers(api_key: str = "", auth_token: str = "") -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    # 用于后端日志定位（CommonConstant.REQUEST_ID = "ADMIN_REQUEST_ID"）
    request_id = os.getenv("EGATEE_REQUEST_ID", "").strip()
    if not request_id:
        request_id = uuid.uuid4().hex
    headers["ADMIN_REQUEST_ID"] = request_id
    return headers


def _is_debug() -> bool:
    return os.getenv("EGATEE_DEBUG", "").strip() in ("1", "true", "TRUE", "yes", "YES", "on", "ON")


def _redact_headers(headers: Dict[str, str]) -> Dict[str, str]:
    safe = dict(headers or {})
    if "X-API-Key" in safe and safe["X-API-Key"]:
        v = safe["X-API-Key"]
        safe["X-API-Key"] = f"{v[:8]}...{v[-6:]}" if len(v) > 14 else "***"
    if "Authorization" in safe and safe["Authorization"]:
        safe["Authorization"] = "Bearer ***"
    return safe


def _debug_log(msg: str):
    if not _is_debug():
        return
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def post_json(url: str, headers: Dict[str, str], body: Dict[str, Any], timeout: int) -> Dict:
    try:
        _debug_log(f"HTTP POST {url}")
        _debug_log(f"  headers={json.dumps(_redact_headers(headers), ensure_ascii=False)}")
        _debug_log(f"  body={json.dumps(body, ensure_ascii=False)}")
        resp = requests.post(url, headers=headers, data=json.dumps(body), timeout=timeout)
    except requests.RequestException as e:
        raise RuntimeError(
            f"HTTP request failed: method=POST, url={url}, body={json.dumps(body, ensure_ascii=False)}, err={e}"
        ) from e

    raw_text = resp.text
    _debug_log(f"HTTP {resp.status_code} {url}")
    if resp.status_code < 200 or resp.status_code >= 300:
        raise RuntimeError(
            "HTTP status error: "
            f"method=POST, url={url}, status={resp.status_code}, "
            f"request_body={json.dumps(body, ensure_ascii=False)}, "
            f"response_body={raw_text}"
        )

    try:
        payload = resp.json()
    except ValueError as e:
        raise RuntimeError(
            "JSON decode error: "
            f"method=POST, url={url}, status={resp.status_code}, "
            f"request_body={json.dumps(body, ensure_ascii=False)}, "
            f"response_body={raw_text}"
        ) from e

    code = payload.get("code")
    msg = payload.get("msg")
    success = payload.get("success")
    not_success = payload.get("notSuccess")
    _debug_log(
        "  parsed="
        + json.dumps(
            {"code": code, "msg": msg, "success": success, "notSuccess": not_success},
            ensure_ascii=False,
        )
    )

    # 兼容 ResultVo：部分接口 code=1 但 success=true / notSuccess=false 仍表示成功
    ok = False
    if success is True or not_success is False:
        ok = True
    elif code in (0, 1) and isinstance(msg, str) and msg.lower() == "success":
        ok = True

    if not ok:
        raise RuntimeError(
            "API business error: "
            f"url={url}, code={code}, msg={msg}, success={success}, notSuccess={not_success}, "
            f"request_body={json.dumps(body, ensure_ascii=False)}, "
            f"response_body={raw_text}"
        )
    return payload.get("data")


def extract_text_from_msg_body(msg_body: List) -> str:
    if not isinstance(msg_body, list):
        return ""
    texts: List[str] = []
    for item in msg_body:
        if isinstance(item, dict):
            msg_content = item.get("MsgContent")
            if isinstance(msg_content, dict):
                text = msg_content.get("Text")
                if isinstance(text, str) and text.strip():
                    texts.append(text.strip())
    return " ".join(texts)


def summarize(records: List[Dict]) -> Dict:
    peer_set = set()
    text_samples: List[str] = []
    for r in records:
        peer = r.get("peerAccount")
        if peer:
            peer_set.add(peer)
        txt = extract_text_from_msg_body(r.get("msgBody", []))
        if txt:
            text_samples.append(txt)

    # 简单关键词统计（按空格切分，保留长度>=2的词）
    tokens: List[str] = []
    for text in text_samples:
        for t in text.replace("\n", " ").split(" "):
            t = t.strip()
            if len(t) >= 2:
                tokens.append(t)
    top_keywords = Counter(tokens).most_common(20)

    return {
        "message_count": len(records),
        "active_peer_count": len(peer_set),
        "top_keywords": [{"keyword": k, "count": v} for k, v in top_keywords],
    }


def build_peer_summaries(
    records: List[Dict],
    peer_profiles: Optional[Dict[str, Any]] = None,
    top_n: int = 10,
    sample_per_peer: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    按 peerAccount 聚合，输出更易读的会话摘要。
    """
    peer_profiles = peer_profiles or {}
    buckets: Dict[str, List[Dict]] = {}
    for r in records:
        peer = r.get("peerAccount") or ""
        if not peer:
            continue
        buckets.setdefault(peer, []).append(r)

    items: List[Dict[str, Any]] = []
    for peer, msgs in buckets.items():
        prof = peer_profiles.get(peer) if isinstance(peer_profiles, dict) else None
        peer_nick = prof.get("nick") if isinstance(prof, dict) else None
        peer_avatar = prof.get("avatar") if isinstance(prof, dict) else None

        msgs_sorted = sorted(msgs, key=lambda x: extract_msg_time(x) or 0)
        texts = []
        for m in msgs_sorted:
            t = extract_text_from_msg_body(m.get("msgBody", []))
            if t:
                texts.append(t)
        items.append(
            {
                "peerAccount": peer,
                "peerNick": peer_nick,
                "peerAvatar": peer_avatar,
                "message_count": len(msgs),
                "first_msg_time": extract_msg_time(msgs_sorted[0]) if msgs_sorted else 0,
                "last_msg_time": extract_msg_time(msgs_sorted[-1]) if msgs_sorted else 0,
                "text_samples": (texts[:sample_per_peer] if isinstance(sample_per_peer, int) and sample_per_peer > 0 else texts),
            }
        )

    items.sort(key=lambda x: x.get("message_count", 0), reverse=True)
    return items[: max(1, top_n)]


def build_report_markdown(meta: Dict[str, Any], summary: Dict[str, Any], peer_summaries: List[Dict[str, Any]]) -> str:
    """
    生成一段可读性更强的中文 Markdown 报告（便于直接粘贴到IM/飞书/邮件）。
    """
    im_account = meta.get("imAccount") or ""
    start_time = meta.get("startTime")
    end_time = meta.get("endTime")
    total = summary.get("message_count", 0)
    peer_cnt = summary.get("active_peer_count", 0)

    lines: List[str] = []
    lines.append("## 聊天汇总")
    lines.append(f"- IM账号：`{im_account}`")
    lines.append(f"- 时间范围：`{start_time}` ~ `{end_time}`（秒）")
    lines.append(f"- 消息总数：**{total}**")
    lines.append(f"- 活跃对端数：**{peer_cnt}**")

    top_kw = summary.get("top_keywords") or []
    if isinstance(top_kw, list) and top_kw:
        lines.append("")
        lines.append("## 高频关键词（Top 10）")
        for it in top_kw[:10]:
            k = it.get("keyword")
            c = it.get("count")
            if k:
                lines.append(f"- {k}（{c}）")

    if peer_summaries:
        lines.append("")
        lines.append("## 活跃对端摘要（Top 10）")
        for p in peer_summaries[:10]:
            peer = p.get("peerAccount", "")
            mc = p.get("message_count", 0)
            lines.append(f"- 对端：`{peer}`，消息数：**{mc}**")
            samples = p.get("text_samples") or []
            if isinstance(samples, list) and samples:
                for s in samples[:3]:
                    s = (s or "").strip()
                    if s:
                        lines.append(f"  - {s}")

    return "\n".join(lines).strip() + "\n"

def extract_to_account(session: Dict) -> str:
    # 尽量兼容不同会话结构
    for key in ("userIDOrGroupID", "userID"):
        val = session.get(key)
        if isinstance(val, str) and val:
            return val
    user_profile = session.get("userProfile")
    if isinstance(user_profile, dict):
        uid = user_profile.get("userID")
        if isinstance(uid, str) and uid:
            return uid
    return ""


def extract_msg_time(msg: Dict) -> int:
    for key in ("msgTime", "time", "timestamp"):
        val = msg.get(key)
        if isinstance(val, int):
            return val
        if isinstance(val, str) and val.isdigit():
            return int(val)
    return 0


def pull_all_records(day: int, page_size: int, max_pages: int, timeout: int) -> Tuple[Dict, List[Dict], Dict[str, Any]]:
    """
    仅调用 notify 新接口：
    /api/notify/im/openapi/getChatHistoryByApiKey
    """
    from_account = get_optional_env("EGATEE_FROM_ACCOUNT")
    auth_token = get_optional_env("EGATEE_AUTH_TOKEN")
    api_key = get_optional_env("EGATEE_CHAT_API_KEY")
    if not api_key:
        raise RuntimeError(
            "未配置 Egatee 聊天拉取所需的 API Key。\n"
            "请在 OpenClaw 中为该 Skill 配置环境变量 EGATEE_CHAT_API_KEY（绑定 IM 账号的密钥，与 uat_/prod_ 前缀对应环境）。\n"
            "可选：EGATEE_NOTIFY_BASE_URL（不填则按 key 前缀自动选择：uat_ -> http://api.uat.egatee.net，其它 -> https://api.egatee.com）。\n"
            "在 OpenClaw Secret / 本地环境变量中设置上述变量即可。"
        )

    base_url = get_notify_base_url(api_key)
    headers = build_headers(api_key=api_key, auth_token=auth_token)
    openapi_url = f"{base_url}/api/notify/im/openapi/getChatHistoryByApiKey"
    req_body = {
        "day": day,
        "current": 1,
        "size": page_size,
    }
    openapi_data = post_json(openapi_url, headers, req_body, timeout)
    if not isinstance(openapi_data, dict):
        raise RuntimeError(f"Unexpected data format from openapi: {openapi_data}")

    all_records = openapi_data.get("records") or []
    if not isinstance(all_records, list):
        all_records = []

    peer_profiles = openapi_data.get("peerProfiles") or {}
    if not isinstance(peer_profiles, dict):
        peer_profiles = {}

    meta = {
        "imAccount": openapi_data.get("imAccount", from_account),
        "startTime": openapi_data.get("startTime"),
        "endTime": openapi_data.get("endTime"),
        "total": openapi_data.get("total", len(all_records)),
        "current": openapi_data.get("current"),
        "size": openapi_data.get("size"),
    }
    return meta, all_records, peer_profiles


def main():
    parser = argparse.ArgumentParser(description="Egatee Chat Summary Skill Tool")
    parser.add_argument("--day", type=int, default=1, help="Query recent days, 1~7")
    parser.add_argument("--size", type=int, default=100, help="Page size")
    parser.add_argument("--max-pages", type=int, default=20, help="Max pages to fetch")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds")
    args = parser.parse_args()

    if args.day < 1 or args.day > 7:
        raise RuntimeError("day must be between 1 and 7")
    if args.size < 1 or args.size > 500:
        raise RuntimeError("size must be between 1 and 500")

    meta, records, peer_profiles = pull_all_records(args.day, args.size, args.max_pages, args.timeout)
    peer_summaries = build_peer_summaries(records, peer_profiles=peer_profiles, top_n=10)
    result = {
        "meta": meta,
        "peer_summaries": peer_summaries,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

