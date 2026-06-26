#!/usr/bin/env python3
"""
在钉钉文档中创建新文档并写入内容

用法:
    python create_doc.py <title> [content]

参数:
    title: 文档标题
    content: 可选，文档内容（支持 Markdown 格式，默认空内容）

示例:
    python create_doc.py "项目计划" "# 项目计划\n\n## 目标\n完成 Q1 目标"
    python create_doc.py "会议纪要"
"""

import sys
from typing import Optional

from mcporter_utils import run_mcporter, parse_response, get_root_dentry_uuid

# ============== 安全常量 ==============
MAX_CONTENT_LENGTH = 50000  # 最大内容长度（字符）

# ============== 业务函数 ==============

def create_doc(title: str, parent_uuid: str) -> Optional[str]:
    """
    创建文档

    Args:
        title: 文档标题
        parent_uuid: 父节点 ID

    Returns:
        新文档的 dentryUuid，失败返回 None
    """
    success, output = run_mcporter('dingtalk-docs.create_doc_under_node', {
        'name': title,
        'parentDentryUuid': parent_uuid
    })

    if not success:
        print(f"❌ 创建文档失败：{output}")
        return None

    result = parse_response(output)
    if result is None:
        print(f"❌ 解析响应失败：{output}")
        return None

    dentry_uuid = result.get('dentryUuid')
    url = result.get('pcUrl') or result.get('url', 'N/A')
    print(f"✅ 文档创建成功：{title}")
    print(f"   文档 ID: {dentry_uuid}")
    print(f"   访问链接：{url}")
    return dentry_uuid

def write_content(doc_uuid: str, content: str, update_type: int = 0) -> bool:
    """
    写入文档内容

    Args:
        doc_uuid: 文档 ID
        content: 内容（Markdown 格式）
        update_type: 0=覆盖，1=续写

    Returns:
        成功返回 True
    """
    if len(content) > MAX_CONTENT_LENGTH:
        print(f"⚠️  内容过长（{len(content)} 字符），截断到 {MAX_CONTENT_LENGTH} 字符")
        content = content[:MAX_CONTENT_LENGTH]

    success, output = run_mcporter('dingtalk-docs.write_content_to_document', {
        'content': content,
        'updateType': update_type,
        'targetDentryUuid': doc_uuid
    })

    if not success:
        print(f"❌ 写入内容失败：{output}")
        return False

    print(f"✅ 内容写入成功（模式：{'覆盖' if update_type == 0 else '续写'}）")
    return True

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("错误：缺少文档标题参数")
        sys.exit(1)

    title = sys.argv[1].strip()
    content = sys.argv[2] if len(sys.argv) > 2 else ""

    if not title:
        print("错误：文档标题不能为空")
        sys.exit(1)

    print(f"📝 开始创建文档：{title}")
    print("-" * 50)

    # 1. 获取根目录 ID
    print("步骤 1: 获取根目录 ID...")
    root_uuid = get_root_dentry_uuid()
    if not root_uuid:
        sys.exit(1)
    print(f"   根目录 ID: {root_uuid}")

    # 2. 创建文档
    print("\n步骤 2: 创建文档...")
    doc_uuid = create_doc(title, root_uuid)
    if not doc_uuid:
        sys.exit(1)

    # 3. 写入内容（如果有）
    if content:
        print("\n步骤 3: 写入内容...")
        # 处理转义字符
        content = content.replace('\\n', '\n').replace('\\t', '\t')
        if not write_content(doc_uuid, content):
            sys.exit(1)

    print("-" * 50)
    print("✅ 完成！")
    print(f"\n文档链接：https://alidocs.dingtalk.com/i/nodes/{doc_uuid}")

if __name__ == '__main__':
    main()
