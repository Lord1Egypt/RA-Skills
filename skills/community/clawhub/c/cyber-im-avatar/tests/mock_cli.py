#!/usr/bin/env python3
"""mock_cli.py — 假 IM CLI，用于在无真实账号时端到端验证监听引擎。

它模仿三种真实 CLI 的输出形态：
  MOCK_SHAPE=wecom  → 企微形态：正序、无消息 ID、带 security_notice 噪声、需时间窗参数
  MOCK_SHAPE=dws    → 钉钉形态：倒序、有 messageId、stdout 连续两个 JSON 文档
  MOCK_SHAPE=bad    → 字段全不对（验证 SCHEMA_MISMATCH 的诊断路径）

消息数据来自 $MOCK_DATA（JSON: {"messages":[{id,sender,content,time}]}，最新在前）。
"""
import json
import os
import sys

SHAPE = os.environ.get("MOCK_SHAPE", "wecom")
SELF = os.environ.get("MOCK_SELF", "self_id")
DATA = os.environ.get("MOCK_DATA", "")


def load_msgs():
    try:
        with open(DATA) as f:
            return json.load(f).get("messages", [])
    except Exception:
        return []


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False))


def main():
    argv = sys.argv[1:]

    # ---- 身份 ----
    if argv[:2] == ["profile", "list"]:
        emit({"success": True, "profiles": [{"userId": SELF, "corpId": "c1"}]})
        return 0
    if argv[:2] == ["auth", "show"]:
        print(f"Status: authorized\nBot ID: {SELF}")
        return 0
    if argv[:2] == ["auth", "status"]:
        emit({"success": True, "authenticated": True})
        return 0

    # ---- 消息 ----
    target = ""
    if "--chat-id" in argv:
        target = argv[argv.index("--chat-id") + 1]
    elif "--user" in argv:
        target = argv[argv.index("--user") + 1]
    elif "--group" in argv:
        target = argv[argv.index("--group") + 1]
    msgs = load_msgs()

    if SHAPE == "bad":
        emit({"data": {"records": [{"x": 1}], "total": 1}})
        return 0

    if SHAPE == "wecom":
        out = []
        for m in reversed(msgs):  # 企微正序
            out.append({
                "userid": m["sender"], "user_name": "mock",
                "send_time": m["time"], "msg_type": "text",
                "text": {"content": m["content"]},
            })
        emit({"security_notice": "<security_notice>noise</security_notice>",
              "extra_identity_context": "<extra_identity_context>noise</extra_identity_context>",
              "messages": out, "messages_count": len(out), "has_more": False})
        return 0

    # dws 形态：倒序 + 有 messageId + 第二个 JSON 文档
    out = [{"messageId": m["id"], "senderId": m["sender"],
            "text": {"content": m["content"]}, "createTime": m["time"]} for m in msgs]
    emit({"contractVersion": "im.message-list.v1", "messages": out,
          "count": len(out), "hasMore": False, "complete": True})
    emit({"error": {"code": 0, "message": "trailing block, not the payload"}})
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
