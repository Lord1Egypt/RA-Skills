#!/usr/bin/env python3
"""
上传文件到 Teambition（两步：获取上传凭证 → PUT 到 OSS）
用法: uv run scripts/upload_file.py --file-path <路径> --scope <scope> --category <类别>

scope 格式: task:<taskId> | project:<projectId> | rich-text:<id>
category: attachment（最常用）| rich-text | rich-text-attachment | work
"""

import json
import mimetypes
import os
import sys
from typing import Optional

import requests

import call_api


def upload_file(file_path: str, scope: str, category: str) -> str:
    """
    完整上传流程：获取凭证 → PUT 到 OSS → 返回 fileToken。
    失败时 exit(1)。
    """
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}", file=sys.stderr)
        sys.exit(1)

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    print(f"文件: {file_name} ({file_size} bytes, {file_type})", file=sys.stderr)

    # Step 1: 获取上传凭证
    print("Step 1: 获取上传凭证...", file=sys.stderr)
    token_data = call_api.post("v3/awos/upload-token", {
        "scope": scope,
        "fileSize": file_size,
        "fileType": file_type,
        "fileName": file_name,
        "category": category,
    })
    result = token_data.get("result", {})
    upload_url: Optional[str] = result.get("uploadUrl")
    file_token: Optional[str] = result.get("token")

    if not upload_url or not file_token:
        print(f"❌ 获取上传凭证失败，响应: {result}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ 凭证获取成功，fileToken: {file_token}", file=sys.stderr)

    # Step 2: PUT 文件到 OSS
    print("Step 2: 上传文件到 OSS...", file=sys.stderr)
    with open(file_path, "rb") as f:
        resp = requests.put(upload_url, data=f, timeout=120)

    if resp.status_code not in (200, 204):
        print(f"❌ OSS 上传失败 (HTTP {resp.status_code}): {resp.text[:200]}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ 上传成功！", file=sys.stderr)
    print(json.dumps({"fileToken": file_token, "fileName": file_name}, ensure_ascii=False, indent=2))
    return file_token


def main() -> None:
    if "--help" in sys.argv or len(sys.argv) < 2:
        print("""用法: uv run scripts/upload_file.py --file-path <路径> --scope <scope> --category <类别>

必需:
  --file-path <路径>      本地文件路径
  --scope <scope>         业务范围
                          - 评论附件: task:<taskId>
                          - 文件类型自定义字段: task:<taskId>/attachment
                          - 项目: project:<projectId>
                          - 富文本: rich-text:<id>
  --category <类别>       attachment（推荐）| rich-text | rich-text-attachment | work

可选:
  --help                  显示帮助

示例:
  # 上传文件到评论附件
  uv run scripts/upload_file.py \\
    --file-path '/path/to/doc.pdf' \\
    --scope 'task:67ec9b8c3c6130ac88605c3e' \\
    --category 'attachment'

  # 上传文件到文件类型自定义字段（注意 scope 格式）
  uv run scripts/upload_file.py \\
    --file-path '/path/to/doc.pdf' \\
    --scope 'task:67ec9b8c3c6130ac88605c3e/attachment' \\
    --category 'work'

输出: JSON 包含 fileToken，可用于评论附件或自定义字段""")
        sys.exit(0)

    file_path: Optional[str] = None
    scope: Optional[str] = None
    category: Optional[str] = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--file-path" and i + 1 < len(sys.argv):
            file_path = sys.argv[i + 1]; i += 2
        elif arg == "--scope" and i + 1 < len(sys.argv):
            scope = sys.argv[i + 1]; i += 2
        elif arg == "--category" and i + 1 < len(sys.argv):
            category = sys.argv[i + 1]; i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr); sys.exit(1)

    if not file_path:
        print("❌ 缺少 --file-path", file=sys.stderr); sys.exit(1)
    if not scope:
        print("❌ 缺少 --scope", file=sys.stderr); sys.exit(1)
    if not category:
        print("❌ 缺少 --category", file=sys.stderr); sys.exit(1)

    valid_categories = {"attachment", "rich-text", "rich-text-attachment", "work"}
    if category not in valid_categories:
        print(f"❌ 无效 category: {category}，有效值: {', '.join(sorted(valid_categories))}", file=sys.stderr)
        sys.exit(1)

    upload_file(file_path, scope, category)


if __name__ == "__main__":
    main()
