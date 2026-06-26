#!/usr/bin/env python3
"""
导出钉钉文档到本地文件

用法:
    python export_docs.py <doc_url> [output.md]

参数:
    doc_url: 钉钉文档 URL（格式：https://alidocs.dingtalk.com/i/nodes/{dentryUuid}）
    output.md: 可选，输出文件路径（默认：<doc_id>.md）

示例:
    python export_docs.py https://alidocs.dingtalk.com/i/nodes/abc123
    python export_docs.py https://alidocs.dingtalk.com/i/nodes/abc123 output.md
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional

from mcporter_utils import run_mcporter, parse_response, resolve_safe_path

# ============== 安全常量 ==============
MAX_CONTENT_LENGTH = 100000  # 最大内容长度
ALLOWED_ROOT = os.environ.get('OPENCLAW_WORKSPACE', os.getcwd())
DOC_URL_PATTERN = re.compile(
    r'^https://alidocs\.dingtalk\.com/i/nodes/([a-zA-Z0-9]+)$',
    re.IGNORECASE
)

# ============== 安全函数 ==============

def extract_doc_uuid(url: str) -> Optional[str]:
    """从 URL 提取文档 ID"""
    match = DOC_URL_PATTERN.match(url.strip())
    if match:
        return match.group(1)
    return None

def get_document_content(doc_url: str) -> Optional[str]:
    """获取文档内容"""
    success, output = run_mcporter('dingtalk-docs.get_document_content_by_url', {
        'docUrl': doc_url
    })

    if not success:
        print(f"❌ 获取文档内容失败：{output}")
        return None

    result = parse_response(output)
    if result is None:
        print(f"❌ 解析响应失败：{output}")
        return None
    return result.get('content', '')

def save_content(content: str, path: Path) -> bool:
    """保存内容到文件"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ 保存文件失败：{e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("错误：缺少文档 URL 参数")
        sys.exit(1)

    doc_url = sys.argv[1].strip()
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    # 提取文档 ID
    doc_uuid = extract_doc_uuid(doc_url)
    if not doc_uuid:
        print("❌ 无效的文档 URL 格式")
        print("正确格式：https://alidocs.dingtalk.com/i/nodes/{dentryUuid}")
        sys.exit(1)

    # 确定输出文件路径
    if not output_path:
        output_path = f"{doc_uuid}.md"

    # 解析并验证输出路径
    try:
        safe_output = resolve_safe_path(output_path)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # 确保输出文件在允许的目录内
    safe_output = safe_output.resolve()
    if not str(safe_output).startswith(ALLOWED_ROOT):
        safe_output = Path(ALLOWED_ROOT) / safe_output.name

    print(f"📥 导出文档")
    print(f"   源 URL: {doc_url}")
    print(f"   目标文件：{safe_output}")
    print("-" * 50)

    # 获取文档内容
    print("步骤 1: 获取文档内容...")
    content = get_document_content(doc_url)
    if content is None:
        sys.exit(1)

    print(f"   内容长度：{len(content)} 字符")

    if len(content) > MAX_CONTENT_LENGTH:
        print(f"⚠️  内容过长，截断到 {MAX_CONTENT_LENGTH} 字符")
        content = content[:MAX_CONTENT_LENGTH]

    # 保存文件
    print("\n步骤 2: 保存文件...")
    if not save_content(content, safe_output):
        sys.exit(1)

    print("-" * 50)
    print("✅ 导出完成！")
    print(f"\n文件路径：{safe_output}")

if __name__ == '__main__':
    main()
