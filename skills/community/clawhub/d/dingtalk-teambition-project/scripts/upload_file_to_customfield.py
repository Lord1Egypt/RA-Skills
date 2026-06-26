#!/usr/bin/env python3
"""
上传文件到任务的自定义字段（一站式脚本）
用法: uv run scripts/upload_file_to_customfield.py --task-id <ID> --file-path <路径> --customfield-id <字段ID>

自动完成三步流程：
1. 上传文件获取 fileToken（scope: task:<taskId>/attachment, category: attachment）
2. 更新任务自定义字段（包含 metaString + title）
"""

import json
import os
import sys
from typing import Optional

import call_api
import upload_file


def upload_file_to_customfield(task_id: str, file_path: str, customfield_id: str) -> dict:
    """
    上传文件到任务的自定义字段。
    
    Args:
        task_id: 任务 ID
        file_path: 本地文件路径
        customfield_id: 自定义字段 ID
    
    Returns:
        包含上传结果的字典
    """
    # 验证文件存在
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    file_name = os.path.basename(file_path)
    
    # Step 1: 上传文件获取 fileToken
    print(f"📤 正在上传文件: {file_name}...", file=sys.stderr)
    scope = f"task:{task_id}/attachment"
    file_token = upload_file.upload_file(file_path, scope, "attachment")
    
    # Step 2: 更新任务自定义字段
    print("📝 正在更新自定义字段...", file=sys.stderr)
    payload = {
        "customfieldId": customfield_id,
        "value": [{
            "metaString": json.dumps({"fileToken": file_token}, ensure_ascii=False),
            "title": file_name
        }]
    }
    
    result = call_api.post(f"v3/task/{task_id}/customfield/update", payload)
    
    print(f"✅ 文件已成功上传到自定义字段！", file=sys.stderr)
    
    return {
        "success": True,
        "taskId": task_id,
        "customfieldId": customfield_id,
        "fileName": file_name,
        "fileToken": file_token,
        "result": result
    }


def main() -> None:
    if "--help" in sys.argv or len(sys.argv) < 2:
        print("""用法: uv run scripts/upload_file_to_customfield.py --task-id <ID> --file-path <路径> --customfield-id <字段ID>

必需参数:
  --task-id <ID>           任务 ID
  --file-path <路径>       本地文件路径
  --customfield-id <ID>    自定义字段 ID

可选:
  --help                   显示帮助

示例:
  uv run scripts/upload_file_to_customfield.py \\
    --task-id '69b79d53f1c083201b98f83a' \\
    --file-path '/path/to/document.pdf' \\
    --customfield-id '699eb728848fa96f9be04ef6'

说明:
  此脚本自动完成以下步骤：
  1. 上传文件到 OSS（scope: task:<taskId>/attachment, category: attachment）
  2. 更新任务的自定义字段（包含 metaString + title）
  
  查找自定义字段 ID：
  1. 获取任务的 sfcId: uv run scripts/query_task_detail.py <taskId> --detail-level detailed
  2. 获取字段列表: uv run scripts/get_custom_fields.py <projectId> --sfc-id <sfcId>
  3. 找到 type 为 'work' 的字段，其 ID 即为自定义字段 ID""")
        sys.exit(0)
    
    task_id: Optional[str] = None
    file_path: Optional[str] = None
    customfield_id: Optional[str] = None
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--task-id" and i + 1 < len(sys.argv):
            task_id = sys.argv[i + 1]
            i += 2
        elif arg == "--file-path" and i + 1 < len(sys.argv):
            file_path = sys.argv[i + 1]
            i += 2
        elif arg == "--customfield-id" and i + 1 < len(sys.argv):
            customfield_id = sys.argv[i + 1]
            i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr)
            sys.exit(1)
    
    if not task_id:
        print("❌ 缺少 --task-id", file=sys.stderr)
        sys.exit(1)
    if not file_path:
        print("❌ 缺少 --file-path", file=sys.stderr)
        sys.exit(1)
    if not customfield_id:
        print("❌ 缺少 --customfield-id", file=sys.stderr)
        sys.exit(1)
    
    result = upload_file_to_customfield(task_id, file_path, customfield_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
