#!/usr/bin/env python3
"""企业微信（wecom-cli / @wecom/cli）监听入口。通用引擎见 listen_core.py。

按 wecom-cli 1.3.4 实测命令实现（2026-10 校准）：
  whoami : wecom-cli auth show            → 文本 "Status: authorized / Bot ID: ..."
  list   : wecom-cli chat messages list   → --chat-id / --begin-time / --end-time（必填，仅最近 7 天）
  send   : wecom-cli message send         → --chat-id / --msg-type text / --text '{"content":"..."}'
  找人   : wecom-cli contact users search --keywords "关键词"  → userid（单聊 chat_id 就用它）

平台特性（决定了适配写法）：
1. **没有消息 ID**：ChatMessage 只有 userid / user_name / send_time / msg_type / 内容族，
   所以用「发送时间+发送者+正文」复合指纹当水位（f_msg_id_compose）。
2. **必须带时间窗**：begin_time / end_time 每次必填，引擎按 --lookback-min 每轮生成。
3. **返回按时间正序**：order = asc，引擎内部统一翻成最新在前。
4. **单聊的 chat_id 就是对方 userid**，所以 --user-id 直接可用。
5. 每条响应都带 security_notice / extra_identity_context（含身份声明，禁止外泄），
   引擎只取 messages 字段，不会把这两段带出去。

用法:
  python3 wecom_listen_cli.py --user-id <对方userid> [--keyword 词] [--lookback-min 60]
  python3 wecom_listen_cli.py --chat-id <群会话ID>
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from listen_core import main

ADAPTER = {
    "cli": "wecom-cli",
    "cmd_whoami": ["auth", "show"],
    "self_id_regex": r"Bot ID:\s*(\S+)",
    "cmd_list": ["chat", "messages", "list",
                 "--chat-id", "{chat_id}",
                 "--begin-time", "{begin_time}",
                 "--end-time", "{end_time}"],
    "order": "asc",
    "f_items": [["messages"], ["data", "messages"]],
    "f_count": [["messages_count"], ["data", "messages_count"]],
    "f_has_more": [["has_more"], ["data", "has_more"]],
    # 无原生消息 ID → 复合指纹（顺序固定：时间|发送者|正文）
    "f_msg_id_compose": [["send_time"], ["userid"], ["text", "content"]],
    "f_sender": [["userid"], ["sender"], ["from", "userid"]],
    "f_content_list": [["text", "content"], ["content"]],
    "f_create_time": [["send_time"], ["create_time"]],
    # 身份来自 auth show 文本；identity whoami 的 extra_identity_context 禁止外泄，不解析它
    "f_self_id": [["bot_id"]],
}

if __name__ == "__main__":
    main("wecom", ADAPTER)
