#!/usr/bin/env python3
"""
从本地文件导入文档到钉钉文档

用法:
    python import_docs.py <file.md> [title]

参数:
    file.md: Markdown 文件路径
    title: 可选，文档标题（默认使用文件名）

示例:
    python import_docs.py README.md
    python import_docs.py notes.md "项目笔记"
"""

import sys
from pathlib import Path
from typing import Optional

from mcporter_utils import run_mcporter, parse_response, get_root_dentry_uuid, resolve_safe_path

# ============== 安全常量 ==============
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_CONTENT_LENGTH = 50000  # 最大内容长度
ALLOWED_EXTENSIONS = ['.md', '.txt', '.markdown']

# ============== 安全函数 ==============

def validate_file_extension(filename: str) -> bool:
    """验证文件扩展名"""
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS

def validate_file_size(path: Path) -> bool:
    """验证文件大小"""
    size = path.stat().st_size
    if size > MAX_FILE_SIZE:
        print(f"❌ 文件过大：{size / 1024 / 1024:.2f}MB（最大 {MAX_FILE_SIZE / 1024 / 1024}MB）")
        return False
    return True

def create_doc(title: str, parent_uuid: str) -> Optional[str]:
    """创建文档"""
    success, output = run_mcporter('dingtalk-docs.create_doc_under_node', {
        'name': title,
        'parentDentryUuid': parent_uuid
    })

    if not success:
        print(f"❌ 创建文档失败：{output}")
        return None

    result = parse_response(output)
    if result is None:
        return None
    return result.get('dentryUuid')

def write_content(doc_uuid: str, content: str) -> bool:
    """写入内容"""
    success, output = run_mcporter('dingtalk-docs.write_content_to_document', {
        'content': content,
        'updateType': 0,
        'targetDentryUuid': doc_uuid
    })

    if not success:
        print(f"❌ 写入内容失败：{output}")
        return False

    return True

def read_file(path: Path) -> str:
    """读取文件内容"""
    try:
        # 检查文件大小
        if not validate_file_size(path):
            sys.exit(1)

        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        with open(path, 'r', encoding='gbk') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取文件失败：{e}")
        sys.exit(1)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("错误：缺少文件参数")
        sys.exit(1)

    file_path = sys.argv[1]
    title = sys.argv[2].strip() if len(sys.argv) > 2 else None

    # 验证文件扩展名
    if not validate_file_extension(file_path):
        print(f"❌ 不支持的文件类型：{Path(file_path).suffix}")
        print(f"支持的类型：{', '.join(ALLOWED_EXTENSIONS)}")
        sys.exit(1)

    # 解析并验证路径
    try:
        safe_path = resolve_safe_path(file_path)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    if not safe_path.exists():
        print(f"❌ 文件不存在：{safe_path}")
        sys.exit(1)

    # 使用文件名作为标题（如果没有提供）
    if not title:
        title = safe_path.stem

    print(f"📝 导入文档：{title}")
    print(f"   源文件：{safe_path}")
    print("-" * 50)

    # 读取文件内容
    print("步骤 1: 读取文件内容...")
    content = read_file(safe_path)
    print(f"   内容长度：{len(content)} 字符")

    if len(content) > MAX_CONTENT_LENGTH:
        print(f"⚠️  内容过长，截断到 {MAX_CONTENT_LENGTH} 字符")
        content = content[:MAX_CONTENT_LENGTH]

    # 获取根目录 ID
    print("\n步骤 2: 获取根目录 ID...")
    root_uuid = get_root_dentry_uuid()
    if not root_uuid:
        sys.exit(1)

    # 创建文档
    print("\n步骤 3: 创建文档...")
    doc_uuid = create_doc(title, root_uuid)
    if not doc_uuid:
        sys.exit(1)

    # 写入内容
    print("\n步骤 4: 写入内容...")
    if not write_content(doc_uuid, content):
        sys.exit(1)

    print("-" * 50)
    print("✅ 导入完成！")
    print(f"\n文档链接：https://alidocs.dingtalk.com/i/nodes/{doc_uuid}")

if __name__ == '__main__':
    main()
