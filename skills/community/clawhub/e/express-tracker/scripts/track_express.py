#!/usr/bin/env python3
"""
快递查询脚本
支持圆通、中通、申通、韵达、顺丰、京东等主流快递公司
生成快递100查询链接，简单可靠
"""

import argparse
import sys
import json
import webbrowser
import platform

# 导入快递公司代码库
sys.path.insert(0, '/Users/junjian/.openclaw/workspace/skills/express-tracker/scripts')
from express_codes import detect_express, get_express_name


def get_query_info(nu: str, com: str = None) -> dict:
    """
    获取快递查询信息

    Args:
        nu: 快递单号
        com: 快递公司代码（可选）

    Returns:
        快递信息字典
    """
    result = {
        'nu': nu,
        'com': com,
        'com_name': None,
        'query_url': f"https://www.kuaidi100.com/chaxun?nu={nu}"
    }

    # 自动识别快递公司
    if not com:
        com, com_name = detect_express(nu)
        if com:
            result['com'] = com
            result['com_name'] = com_name

    if com and not result['com_name']:
        result['com_name'] = get_express_name(com)

    return result


def format_text(result: dict) -> str:
    """格式化为文本输出"""
    lines = []

    lines.append(f"📦 快递单号：{result['nu']}")
    if result['com_name']:
        lines.append(f"🏢 快递公司：{result['com_name']}")
    lines.append(f"🔗 查询链接：{result['query_url']}")
    lines.append("")
    lines.append("💡 提示：点击上方链接查看详细物流信息")

    return '\n'.join(lines)


def format_markdown(result: dict) -> str:
    """格式化为 Markdown 输出"""
    lines = []

    lines.append(f"# 📦 快递查询：{result['nu']}")
    lines.append("")
    lines.append("## 基本信息")
    lines.append(f"- **快递单号**：{result['nu']}")
    if result['com_name']:
        lines.append(f"- **快递公司**：{result['com_name']}")
    lines.append(f"- **查询链接**：[{result['query_url']}]({result['query_url']})")
    lines.append("")
    lines.append("## 💡 提示")
    lines.append("点击上方链接在快递100查看详细物流信息")

    return '\n'.join(lines)


def open_in_browser(url: str):
    """在浏览器中打开链接"""
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"无法自动打开浏览器：{e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='快递查询工具')
    parser.add_argument('--nu', required=True, help='快递单号')
    parser.add_argument('--com', help='快递公司代码（可选）')
    parser.add_argument('--format', choices=['text', 'json', 'markdown'], default='text', help='输出格式')
    parser.add_argument('--output', help='输出到文件')
    parser.add_argument('--open', action='store_true', help='自动在浏览器中打开查询链接')

    args = parser.parse_args()

    # 获取查询信息
    result = get_query_info(args.nu, args.com)

    # 格式化输出
    if args.format == 'json':
        output = json.dumps(result, ensure_ascii=False, indent=2)
    elif args.format == 'markdown':
        output = format_markdown(result)
    else:
        output = format_text(result)

    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已保存到：{args.output}")
    else:
        print(output)

    # 自动打开浏览器
    if args.open:
        print("\n正在打开浏览器...")
        open_in_browser(result['query_url'])


if __name__ == '__main__':
    main()
