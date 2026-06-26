#!/usr/bin/env python3
"""
查询 Teambition 企业成员
用法: 
  uv run scripts/query_members.py --keyword <关键词>
  uv run scripts/query_members.py --user-ids <用户ID1,用户ID2,...>
"""

import json
import sys
from typing import Any, Dict, List, Optional

import call_api

def query_members_by_keyword(keyword: str) -> List[Dict[str, Any]]:
    """按关键词搜索成员"""
    data = call_api.post(f"v3/member/query?q={keyword}")
    members: List[Dict[str, Any]] = data.get("result", [])
    return members

def query_members_by_ids(user_ids: List[str]) -> List[Dict[str, Any]]:
    """按用户ID批量查询成员"""
    # API 的 userIds 参数接受逗号分隔的字符串
    ids_str = ",".join(user_ids)
    data = call_api.post(f"v3/member/query?userIds={ids_str}")
    members: List[Dict[str, Any]] = data.get("result", [])
    return members

def simplify_members(members: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """简化成员信息，只保留关键字段"""
    return [
        {
            "userId": m.get("userId"),
            "name": m.get("name"),
            "email": m.get("email"),
            "phone": m.get("phone"),
        }
        for m in members
    ]

def main() -> None:
    if "--help" in sys.argv or len(sys.argv) < 2:
        print("""用法: uv run scripts/query_members.py [选项]

选项:
  --keyword <关键词>      按姓名/邮箱/工号搜索成员
  --user-ids <用户IDs>    按用户ID批量查询，逗号分隔
  --help                 显示帮助

示例:
  uv run scripts/query_members.py --keyword '张三'
  uv run scripts/query_members.py --user-ids 'id1,id2,id3'""")
        sys.exit(0 if "--help" in sys.argv else 1)

    keyword: Optional[str] = None
    user_ids: Optional[str] = None
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--keyword" and i + 1 < len(sys.argv):
            keyword = sys.argv[i + 1]
            i += 2
        elif arg == "--user-ids" and i + 1 < len(sys.argv):
            user_ids = sys.argv[i + 1]
            i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr)
            sys.exit(1)

    if not keyword and not user_ids:
        print("❌ 需要提供 --keyword 或 --user-ids", file=sys.stderr)
        sys.exit(1)

    if user_ids:
        # 批量查询用户ID
        ids_list = [id.strip() for id in user_ids.split(",") if id.strip()]
        members = query_members_by_ids(ids_list)
        if not members:
            print(f"未找到指定用户ID的成员。", file=sys.stderr)
            print(json.dumps([], ensure_ascii=False, indent=2))
            return
    else:
        # 按关键词搜索
        members = query_members_by_keyword(keyword)
        if not members:
            print(f"未找到姓名包含「{keyword}」的成员。", file=sys.stderr)
            print(json.dumps([], ensure_ascii=False, indent=2))
            return

    simplified = simplify_members(members)
    print(json.dumps(simplified, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()