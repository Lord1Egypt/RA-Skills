
#!/usr/bin/env python3
"""
渲染任务富文本内容，提取文件和文本信息
用法: uv run scripts/render_rtf.py <taskId> <rtfField1[,rtfField2,...]>
"""

import json
import re
import sys
from typing import Any, Dict, List, Optional

import call_api


def parse_rtf_field(field: str, task_id: str) -> str:
    """
    解析富文本字段标识
    支持格式：
    - note: 备注
    - cf:字段ID: 自定义字段
    - trace:进展ID: 进展
    """
    if field == "note":
        return f"{task_id}:note"
    elif field.startswith("cf:"):
        field_id = field[3:]
        return f"{task_id}:cf:{field_id}"
    elif field.startswith("trace:"):
        trace_id = field[6:]
        return f"{task_id}:trace:{trace_id}"
    else:
        # 默认当作自定义字段处理
        return f"{task_id}:cf:{field}"


def extract_text_from_html(html: str) -> str:
    """从 HTML 中提取纯文本内容"""
    # 移除 style 标签及其内容
    html = re.sub(r'<style[^>]*>.*?</style>', '', html,
                  flags=re.DOTALL | re.IGNORECASE)
    # 移除所有 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', html)
    # 清理多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_files_from_html(html: str) -> List[Dict[str, Any]]:
    """从 HTML 中提取文件信息"""
    files = []

    # 提取 embed-card 类型的文件（文档、链接等）
    embed_pattern = r'<div[^>]*data-type="embed-[^"]*"[^>]*>.*?</div>'
    for match in re.finditer(embed_pattern, html, re.DOTALL):
        div_content = match.group(0)

        # 提取文件名
        name_match = re.search(
            r'<div[^>]*class="[^"]*ContentHeader[^"]*"[^>]*>([^<]+)</div>', div_content)
        file_name = name_match.group(1).strip() if name_match else "未知文件"

        # 提取文件大小
        size_match = re.search(
            r'<div[^>]*class="[^"]*ContentDesc[^"]*"[^>]*>([^<]+)</div>', div_content)
        file_size = size_match.group(1).strip() if size_match else ""

        # 提取下载链接
        link_match = re.search(r'<a[^>]*href="([^"]*)"[^>]*>', div_content)
        download_url = link_match.group(1) if link_match else ""

        if download_url:
            files.append({
                "name": file_name,
                "size": file_size,
                "downloadUrl": download_url,
                "type": "document"
            })

    # 提取图片
    img_pattern = r'<img[^>]*src="([^"]*)"[^>]*>'
    for match in re.finditer(img_pattern, html):
        img_url = match.group(1)

        # 跳过图标等小图
        if 'TB16zxhlHY1gK0jSZTE' in img_url or 'width="23px"' in match.group(0):
            continue

        # 提取图片名称
        name_match = re.search(r'fileName\*%3DUTF-8%27%27([^&"]+)', img_url)
        img_name = name_match.group(1) if name_match else "图片"
        # URL 解码文件名
        try:
            from urllib.parse import unquote
            img_name = unquote(unquote(img_name))
        except:
            pass

        files.append({
            "name": img_name,
            "downloadUrl": img_url,
            "type": "image"
        })

    return files


def render_rtf(task_id: str, rtf_fields: List[str], expire_seconds: int = 1800) -> None:
    """
    渲染任务富文本内容

    Args:
        task_id: 任务 ID
        rtf_fields: 富文本字段列表，支持 note, cf:字段ID, trace:进展ID
        expire_seconds: HTML 内容过期时间（秒），默认 1800，范围 600-3600
    """
    # 构建富文本字段标识
    field_ids = [parse_rtf_field(field, task_id) for field in rtf_fields]

    # 调用 API
    params = {
        "rtfFields": ",".join(field_ids),
        "htmlExpireSeconds": min(3600, max(600, expire_seconds))
    }
    headers = {
        "X-Canary": "prepub"
    }
    data = call_api.get("v3/task/rtf/render", params=params, headers=headers)
    results = data.get("result", [])

    if not results:
        print(json.dumps([], ensure_ascii=False, indent=2))
        return

    # 解析结果
    output = []
    for result in results:
        html = result.get("html", "")
        rtf_value_token = result.get("rtfValueToken", "")

        # 提取文本
        text = extract_text_from_html(html)

        # 解析 rtfValueToken 获取附件信息（真实的下载地址）
        attachments = {}
        if rtf_value_token:
            try:
                token_data = json.loads(rtf_value_token)
                attachments = token_data.get("attachments", {})
            except:
                pass

        output.append({
            "taskId": result.get("taskId"),
            "rtfField": result.get("rtfField"),
            "text": text,
            "attachments": attachments
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) < 3 or "--help" in sys.argv:
        print("""用法: uv run scripts/render_rtf.py <taskId> <rtfField1[,rtfField2,...]> [--expire <seconds>]

参数:
  taskId          任务 ID
  rtfFields       富文本字段，多个用逗号分隔。支持格式：
                  - note: 备注
                  - cf:字段ID: 自定义字段（可简写为字段ID）
                  - trace:进展ID: 进展

选项:
  --expire        HTML 内容过期时间（秒），默认 1800，范围 600-3600
  --help          显示帮助

示例:
  # 查看任务备注
  uv run scripts/render_rtf.py 67ec9b8c3c6130ac88605c3e note
  
  # 查看自定义字段
  uv run scripts/render_rtf.py 67ec9b8c3c6130ac88605c3e cf:63d61d1cbde6c83a2ce729d6
  
  # 查看进展
  uv run scripts/render_rtf.py 67ec9b8c3c6130ac88605c3e trace:63d61d1cbde6c83a2ce729d6
  
  # 同时查看多个字段
  uv run scripts/render_rtf.py 67ec9b8c3c6130ac88605c3e note,cf:63d61d1cbde6c83a2ce729d6""")
        sys.exit(0 if "--help" in sys.argv else 1)

    task_id = sys.argv[1]
    rtf_fields = [f.strip() for f in sys.argv[2].split(",")]
    expire_seconds = 1800

    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--expire" and i + 1 < len(sys.argv):
            try:
                expire_seconds = int(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"❌ 无效的过期时间: {sys.argv[i + 1]}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr)
            sys.exit(1)

    render_rtf(task_id, rtf_fields, expire_seconds)


if __name__ == "__main__":
    main()
