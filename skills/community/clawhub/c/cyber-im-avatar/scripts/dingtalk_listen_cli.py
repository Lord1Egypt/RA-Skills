#!/usr/bin/env python3
"""钉钉（dws / dingtalk-workspace-cli）监听入口。通用引擎见 listen_core.py。

按 dws v1.0.66 实测命令实现（2026-10 校准，本机 npm i -g dingtalk-workspace-cli）：
  本人 ID : dws profile list            → profiles[].userId（未登录时为空数组）
  群消息  : dws chat +chat-messages --group <群名|openConversationId> --limit N
  单聊    : dws chat +chat-messages --user <userId> --limit N
  会话列表: dws chat +recent-conversations（最近有新消息的单聊+群聊）
  搜人    : dws contact user search --query "关键词" → result[].userId
  发送    : dws chat +messages-send / dws chat +dm --to 姓名 --content "..."

实测要点：
1. `+chat-messages` 输出 ledger：顶层 messages[] / count / hasMore / complete /
   failures / stopReason，**默认 order=desc（最新在前）**。
2. 同一个进程可能先打结果 JSON、再打错误块 JSON —— 引擎只取第一个 JSON 文档。
3. 目标参数互斥：群聊 --group，单聊 --user 或 --open-dingtalk-id。
4. 省略时间参数时默认从当前时间向前读最近消息，无需传时间窗。
5. dws 需要先 `dws auth login`（企业管理员授权），未登录时 profile list 为空。

用法:
  python3 dingtalk_listen_cli.py --user-id <userId>            # 单聊
  python3 dingtalk_listen_cli.py --chat-id <openConversationId> # 群聊
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from listen_core import main

ADAPTER = {
    "cli": "dws",
    "cmd_whoami": ["profile", "list"],
    "f_self_id": [["profiles", 0, "userId"], ["current", "userId"], ["data", "userId"]],
    "cmd_list": ["chat", "+chat-messages", "--group", "{chat_id}", "--limit", "20"],
    "cmd_list_user": ["chat", "+chat-messages", "--user", "{user_id}", "--limit", "20"],
    "order": "desc",
    "f_items": [["messages"], ["data", "messages"], ["result", "messages"]],
    "f_count": [["count"], ["data", "count"]],
    "f_has_more": [["hasMore"], ["data", "hasMore"]],
    "f_msg_id": [["messageId"], ["msgId"], ["message_id"], ["id"]],
    "f_sender": [["senderId"], ["sender", "userId"], ["sender", "id"], ["sender"]],
    "f_content_list": [["text", "content"], ["text"], ["content"]],
    "f_create_time": [["createTime"], ["sendTime"], ["create_time"]],
}

if __name__ == "__main__":
    main("dingtalk", ADAPTER)
