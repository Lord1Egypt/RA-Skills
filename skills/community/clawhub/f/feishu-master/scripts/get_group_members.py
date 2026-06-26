#!/usr/bin/env python3
"""
获取飞书群组成员列表

获取指定飞书群组的成员列表，支持分页查询。

Usage:
    python3 get_group_members.py <chat_id> [options]

Parameters:
    chat_id: 群组 ID (open_chat_id)

Options:
    --page-size: 每页数量，默认为 20
    --page-token: 分页标记，用于获取下一页
    --help, -h: 显示帮助信息

Output:
    JSON 格式输出:
    {
      "code": 0,
      "msg": "success",
      "data": {
        "items": [
          {
            "member_id": "ou_xxxxxxxxxxxxxxxx",
            "member_id_type": "open_id",
            "name": "张三",
            "type": "user"
          }
        ],
        "page_token": "next_page_token",
        "has_more": true
      }
    }

Error Codes:
    0: 成功
    1: 参数错误
    2: API 调用失败

Examples:
    # 获取群组成员列表（第一页）
    python3 get_group_members.py <open_chat_id>

    # 获取 50 个群组成员
    python3 get_group_members.py <open_chat_id> --page-size 50

    # 获取下一页成员
    python3 get_group_members.py <open_chat_id> --page-token "next_page_token"

References:
    飞书 API 文档: https://open.feishu.cn/document/server-docs/im-v1/group-group/get_group_member_list
"""

import sys
import json
import subprocess
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests 库未安装，请运行: pip install requests", file=sys.stderr)
    sys.exit(1)

# 配置
TOKEN_SCRIPT = Path(__file__).parent / "get_token.py"
API_URL = "https://open.feishu.cn/open-apis/im/v1/chats"


def get_token():
    """获取飞书 token"""
    result = subprocess.run(
        [sys.executable, str(TOKEN_SCRIPT)],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def get_group_members(chat_id, page_size=20, page_token="", token=None):
    """获取群组成员 API 调用"""
    if token is None:
        token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    params = {
        "page_size": page_size
    }

    if page_token:
        params["page_token"] = page_token

    url = f"{API_URL}/{chat_id}/members"
    response = requests.get(url, headers=headers, params=params, timeout=30)
    data = response.json()

    return data


def parse_arguments():
    """解析命令行参数"""
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    chat_id = sys.argv[1]
    page_size = 20
    page_token = ""

    # 解析可选参数
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--page-size" and i + 1 < len(sys.argv):
            try:
                page_size = int(sys.argv[i + 1])
            except ValueError:
                print("Error: --page-size 必须是整数", file=sys.stderr)
                sys.exit(1)
            i += 2
        elif sys.argv[i].startswith("--page-token") and i + 1 < len(sys.argv):
            page_token = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    return chat_id, page_size, page_token


def main():
    # 解析参数
    chat_id, page_size, page_token = parse_arguments()

    # 获取 token
    token = get_token()

    # 调用 API
    result = get_group_members(chat_id, page_size, page_token, token)

    # 输出 JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 根据返回码设置退出状态
    if result.get("code") != 0:
        sys.exit(2)


if __name__ == "__main__":
    main()