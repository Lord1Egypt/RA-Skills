#!/usr/bin/env python3
"""飞书（lark-cli）监听入口。通用引擎见 listen_core.py。

用法:
  python3 feishu_listen_cli.py --chat-id oc_xxx [--sender ou_xxx] [--keyword 词]
          [--interval 60] [--init latest|zero] [--timeout 秒]
  python3 feishu_listen_cli.py --user-id ou_xxx      # 私聊场景免查 chat_id

回复命令（agent 接管后用，以本人身份）:
  lark-cli im +messages-send --chat-id oc_xxx --msg-type text --as user --text "$(cat /tmp/reply.txt)"
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from listen_core import main

ADAPTER = {
    "cli": "lark-cli",
    "cmd_list": ["im", "+chat-messages-list", "--chat-id", "{chat_id}",
                 "--order", "desc", "--limit", "10", "--as", "user"],
    # 同一个端点接受 --user-id：服务端直接解析 p2p 会话，免去先枚举/查 chat_id
    "cmd_list_user": ["im", "+chat-messages-list", "--user-id", "{user_id}",
                      "--order", "desc", "--limit", "10", "--as", "user"],
    "cmd_mget": ["im", "+messages-mget", "--message-ids", "{ids}", "--as", "user"],
    "cmd_whoami": ["auth", "status"],
    # lark-cli 实际返回 data.messages（旧版为 body.items），双路径兜底
    "f_items": [["data", "messages"], ["messages"], ["items"], ["body", "items"]],
    "f_msg_id": [["message_id"]],
    "f_sender": [["sender", "id"], ["sender", "sender_id", "open_id"]],
    "f_content_list": [["content"], ["body", "content"]],
    "f_content_mget": [["content"], ["body", "content"]],
    "f_create_time": [["create_time"], ["create_at"]],
    "f_self_id": [["identities", "user", "openId"]],
}

if __name__ == "__main__":
    main("feishu", ADAPTER)
