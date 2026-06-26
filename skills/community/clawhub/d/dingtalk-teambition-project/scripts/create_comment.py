#!/usr/bin/env python3
"""
为 Teambition 任务创建评论，支持按姓名 @人
用法: uv run scripts/create_comment.py --task-id <ID> --content <内容> [--mention "张三,李四"] [--render-mode markdown]
"""

import json
import sys
from typing import List, Optional

import call_api

def create_comment(
    task_id: str,
    content: str,
    mention_names: Optional[List[str]] = None,
    mention_ids: Optional[List[str]] = None,
    render_mode: str = "plain",
    file_tokens: Optional[List[str]] = None,
) -> None:
    mention_user_ids: List[str] = []
    if mention_ids:
        mention_user_ids.extend(mention_ids)
    if mention_names:
        for name in mention_names:
            name = name.strip()
            if not name:
                continue
            uid = call_api.search_member(name)
            mention_user_ids.append(uid)
            print(f"✅ @{name} → userId: {uid}", file=sys.stderr)

    body = {"content": content, "renderMode": render_mode}
    if mention_user_ids:
        body["mentionUserIds"] = mention_user_ids
    if file_tokens:
        body["fileTokens"] = file_tokens

    data = call_api.post(f"v3/task/{task_id}/comment", body)
    print(json.dumps(data.get("result", data), ensure_ascii=False, indent=2))

def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/create_comment.py --task-id <ID> --content <内容> [选项]

必需:
  --task-id <ID>          任务 ID
  --content <内容>        评论内容

可选:
  --mention <姓名列表>    按姓名 @人，逗号分隔（如 "张三,李四"）
                          脚本自动搜索 userId；姓名不唯一时打印候选列表并退出
  --mention-id <ID列表>   直接传 userId @人，逗号分隔（如 "uid1,uid2"）
                          与 --mention 互斥，优先使用此参数
  --file-tokens <token列表> 附件 fileToken，逗号分隔（由 upload_file.py 返回）
  --render-mode <模式>    plain（默认）或 markdown
  --help                  显示帮助

示例:
  uv run scripts/create_comment.py \\
    --task-id 'xxx' --content '已完成初稿'

  uv run scripts/create_comment.py \\
    --task-id 'xxx' --content '请 @张三 评审' --mention '张三'

  uv run scripts/create_comment.py \\
    --task-id 'xxx' --content '请 @张三 @李四 确认' --mention '张三,李四'
    
  uv run scripts/create_comment.py \\
    --task-id 'xxx' --content '请确认' --mention-id '61cad8021deea2ac89a4cbf3'

  uv run scripts/create_comment.py \\
    --task-id 'xxx' --content '附件已上传，请查收' --file-tokens 'token1,token2'""")
        sys.exit(0)

    task_id: Optional[str] = None
    content: Optional[str] = None
    mention_names: Optional[List[str]] = None
    mention_ids: Optional[List[str]] = None
    render_mode = "plain"
    file_tokens: Optional[List[str]] = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--task-id" and i + 1 < len(sys.argv):
            task_id = sys.argv[i + 1]; i += 2
        elif arg == "--content" and i + 1 < len(sys.argv):
            content = sys.argv[i + 1]; i += 2
        elif arg == "--mention" and i + 1 < len(sys.argv):
            mention_names = [n.strip() for n in sys.argv[i + 1].split(",") if n.strip()]; i += 2
        elif arg == "--mention-id" and i + 1 < len(sys.argv):
            mention_ids = [n.strip() for n in sys.argv[i + 1].split(",") if n.strip()]; i += 2
        elif arg == "--file-tokens" and i + 1 < len(sys.argv):
            file_tokens = [t.strip() for t in sys.argv[i + 1].split(",") if t.strip()]; i += 2
        elif arg == "--render-mode" and i + 1 < len(sys.argv):
            render_mode = sys.argv[i + 1]; i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr); sys.exit(1)

    if not task_id:
        print("❌ 缺少 --task-id", file=sys.stderr); sys.exit(1)
    if not content:
        print("❌ 缺少 --content", file=sys.stderr); sys.exit(1)

    create_comment(task_id, content, mention_names, mention_ids, render_mode, file_tokens)

if __name__ == "__main__":
    main()