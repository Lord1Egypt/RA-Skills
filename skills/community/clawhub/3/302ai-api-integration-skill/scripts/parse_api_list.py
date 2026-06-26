#!/usr/bin/env python3
"""
302.AI API 列表解析脚本

自动从 https://doc.302.ai/llms.txt 获取最新 API 列表并解析
提取 API 名称、分类、文档链接和描述
"""

import re
import sys
import requests
from typing import List, Dict, Optional

# 302.AI API 列表 URL
LLMS_TXT_URL = "https://doc.302.ai/llms.txt"


def fetch_llms_txt(url: str = LLMS_TXT_URL) -> str:
    """
    从 302.AI 获取最新的 API 列表

    Args:
        url: llms.txt 的 URL（默认使用官方地址）

    Returns:
        llms.txt 文件内容

    Raises:
        Exception: 如果请求失败
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"获取 API 列表失败: {e}")


def parse_llms_txt(content: str) -> List[Dict[str, str]]:
    """
    解析 llms.txt 内容，提取所有 API 信息

    Args:
        content: llms.txt 文件内容

    Returns:
        API 信息列表，每个元素包含：
        - category: 分类路径（如：语言大模型 > OpenAI）
        - name: API 名称
        - link: 文档链接
        - description: API 描述
    """
    apis = []

    # 正则表达式匹配格式：- 分类 > 子分类 [API名称](文档链接): 描述
    # 示例：- 语言大模型 > OpenAI [Chat（聊天）](https://doc.302.ai/147522039e0.md): 描述内容
    pattern = r'^-\s+(.+?)\s+\[(.+?)\]\((.+?)\):\s*(.*)$'

    for line in content.split('\n'):
        line = line.strip()
        if not line or not line.startswith('-'):
            continue

        match = re.match(pattern, line)
        if match:
            category = match.group(1).strip()
            name = match.group(2).strip()
            link = match.group(3).strip()
            description = match.group(4).strip()

            apis.append({
                'category': category,
                'name': name,
                'link': link,
                'description': description
            })

    return apis


def search_apis(apis: List[Dict[str, str]],
                keyword: Optional[str] = None,
                category: Optional[str] = None) -> List[Dict[str, str]]:
    """
    搜索 API

    Args:
        apis: API 列表
        keyword: 关键词（在名称和描述中搜索）
        category: 分类关键词（在分类路径中搜索）

    Returns:
        匹配的 API 列表
    """
    results = apis

    if category:
        category_lower = category.lower()
        results = [
            api for api in results
            if category_lower in api['category'].lower()
        ]

    if keyword:
        keyword_lower = keyword.lower()
        results = [
            api for api in results
            if keyword_lower in api['name'].lower() or
               keyword_lower in api['description'].lower()
        ]

    return results


def extract_doc_id(link: str) -> str:
    """
    从文档链接中提取文档 ID

    Args:
        link: 文档链接（如：https://doc.302.ai/147522039e0.md）

    Returns:
        文档 ID（如：147522039e0）
    """
    match = re.search(r'/([^/]+)\.md$', link)
    if match:
        return match.group(1)
    return ''


def format_api_info(api: Dict[str, str], index: int = 0) -> str:
    """
    格式化 API 信息为可读文本

    Args:
        api: API 信息字典
        index: 序号（0 表示不显示序号）

    Returns:
        格式化的文本
    """
    prefix = f"{index}. " if index > 0 else ""
    doc_id = extract_doc_id(api['link'])

    return f"""{prefix}**{api['name']}**
   - 分类：{api['category']}
   - 描述：{api['description']}
   - 文档：{api['link']}
   - 文档ID：{doc_id}"""


def main():
    """
    命令行使用示例
    """
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("使用方法:")
        print("  python parse_api_list.py [关键词] [分类]")
        print()
        print("说明:")
        print("  脚本会自动从 https://doc.302.ai/llms.txt 获取最新 API 列表")
        print()
        print("示例:")
        print("  python parse_api_list.py                    # 列出所有 API")
        print("  python parse_api_list.py GPT                # 搜索包含 GPT 的 API")
        print("  python parse_api_list.py 聊天 语言大模型      # 搜索语言大模型分类下的聊天 API")
        print("  python parse_api_list.py nano-banana        # 搜索 nano-banana 相关 API")
        sys.exit(0)

    keyword = sys.argv[1] if len(sys.argv) > 1 else None
    category = sys.argv[2] if len(sys.argv) > 2 else None

    # 获取最新的 API 列表
    print("正在从 302.AI 获取最新 API 列表...")
    try:
        content = fetch_llms_txt()
        print("✓ 获取成功")
        print()
    except Exception as e:
        print(f"✗ {e}")
        sys.exit(1)

    # 解析 API 列表
    apis = parse_llms_txt(content)
    print(f"总共找到 {len(apis)} 个 API")
    print()

    # 搜索
    if keyword or category:
        results = search_apis(apis, keyword, category)
        print(f"搜索结果：{len(results)} 个匹配的 API")
        print()

        if len(results) == 0:
            print("未找到匹配的 API，请尝试其他关键词")
            sys.exit(0)

        for i, api in enumerate(results, 1):
            print(format_api_info(api, i))
            print()
    else:
        # 显示所有 API（限制前 20 个）
        print("显示前 20 个 API（使用关键词或分类进行筛选）:")
        print()
        for i, api in enumerate(apis[:20], 1):
            print(format_api_info(api, i))
            print()

        if len(apis) > 20:
            print(f"... 还有 {len(apis) - 20} 个 API 未显示")
            print("使用关键词或分类参数进行筛选")


if __name__ == '__main__':
    main()
