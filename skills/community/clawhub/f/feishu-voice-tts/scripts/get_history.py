#!/usr/bin/env python3
"""获取飞书群消息历史，按时间排序"""
import argparse
import os
import time
from datetime import datetime

import requests

TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
MSG_URL = "https://open.feishu.cn/open-apis/im/v1/messages"


def fail(msg: str, code: int = 1):
    raise SystemExit(f"Error: {msg}")


def _json(resp: requests.Response):
    try:
        return resp.json()
    except ValueError:
        fail(f"non-JSON response (HTTP {resp.status_code}): {resp.text[:300]}")


def get_token(timeout=30):
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        fail("请设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量")

    try:
        resp = requests.post(TOKEN_URL, json={"app_id": app_id, "app_secret": app_secret}, timeout=timeout)
    except requests.RequestException as e:
        fail(f"获取 token 请求失败: {e}")

    data = _json(resp)
    if resp.status_code >= 400 or data.get("code") != 0:
        fail(f"获取 token 失败: {data}")
    return data["tenant_access_token"]


def _fetch_messages(token, chat_id, page_size=50, start_time=None, end_time=None, timeout=30):
    all_messages = []
    page_token = None
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        params = {
            "container_id_type": "chat",
            "container_id": chat_id,
            "page_size": page_size,
        }
        if start_time is not None:
            params["start_time"] = int(start_time)
        if end_time is not None:
            params["end_time"] = int(end_time)
        if page_token:
            params["page_token"] = page_token

        try:
            resp = requests.get(MSG_URL, headers=headers, params=params, timeout=timeout)
        except requests.RequestException as e:
            fail(f"获取消息请求失败: {e}")

        data = _json(resp)
        if resp.status_code >= 400 or data.get("code") != 0:
            fail(f"获取消息失败: {data}")

        body = data.get("data", {})
        items = body.get("items", [])
        if not isinstance(items, list):
            fail(f"响应格式异常: {data}")
        all_messages.extend(items)

        if not body.get("has_more"):
            break
        page_token = body.get("page_token")
        if not page_token:
            break

    return all_messages


def main():
    parser = argparse.ArgumentParser(description="获取飞书群消息历史")
    parser.add_argument("--chat_id", required=True, help="飞书群 ID")
    parser.add_argument("--hours", type=int, default=24, help="获取最近几小时的消息，默认 24 小时")
    parser.add_argument("--all", action="store_true", help="获取所有消息（不使用时间过滤）")
    parser.add_argument("--limit", type=int, default=30, help="显示最近多少条消息，默认 30 条")
    parser.add_argument("--type", help="只显示指定类型的消息，如 audio, file, text, image 等")
    args = parser.parse_args()

    if args.hours <= 0:
        fail("--hours 必须大于 0")
    if args.limit <= 0:
        fail("--limit 必须大于 0")

    print("获取 token...")
    token = get_token()

    if args.all:
        print("获取全部消息...")
        messages = _fetch_messages(token, args.chat_id)
    else:
        now = int(time.time())
        start_time = now - (args.hours * 3600)
        print(f"获取最近 {args.hours} 小时消息...")
        messages = _fetch_messages(token, args.chat_id, start_time=start_time, end_time=now)

    print(f"共获取 {len(messages)} 条消息")
    messages.sort(key=lambda x: int(x.get("create_time", 0)), reverse=True)

    if args.type:
        messages = [m for m in messages if m.get("msg_type") == args.type]
        print(f"过滤后 {len(messages)} 条消息")

    print(f"\n最近 {min(args.limit, len(messages))} 条消息:")
    print("-" * 60)
    for i, m in enumerate(messages[: args.limit], start=1):
        ts = int(m.get("create_time", 0)) / 1000 if m.get("create_time") else 0
        dt = datetime.fromtimestamp(ts) if ts else "N/A"
        print(f"{i:2}. {m.get('msg_type', 'unknown'):12} | {dt} | {m.get('message_id', 'N/A')}")
        if m.get("msg_type") in ["audio", "file", "image"]:
            content = str(m.get("body", {}).get("content", ""))[:100]
            print(f"    {content}")


if __name__ == "__main__":
    main()
