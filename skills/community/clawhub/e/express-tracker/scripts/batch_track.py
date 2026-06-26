#!/usr/bin/env python3
"""
批量快递查询脚本
支持从文件或命令行读取多个快递单号生成查询链接
"""

import argparse
import sys
import json
import time

# 导入查询脚本
sys.path.insert(0, '/Users/junjian/.openclaw/workspace/skills/express-tracker/scripts')
from track_express import get_query_info


def read_express_list(file_path: str) -> list:
    """
    从文件读取快递单号列表

    Args:
        file_path: 文件路径

    Returns:
        快递单号列表
    """
    express_list = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # 支持格式：单号 或 单号,公司代码
                    parts = line.split(',')
                    nu = parts[0].strip()
                    com = parts[1].strip() if len(parts) > 1 else None
                    express_list.append({'nu': nu, 'com': com})

    except FileNotFoundError:
        print(f"文件不存在：{file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件出错：{str(e)}")
        sys.exit(1)

    return express_list


def batch_process(express_list: list) -> list:
    """
    批量处理快递单号

    Args:
        express_list: 快递单号列表

    Returns:
        查询结果列表
    """
    results = []

    for item in express_list:
        nu = item['nu']
        com = item.get('com')
        result = get_query_info(nu, com)
        results.append(result)

    return results


def format_batch_text(results: list) -> str:
    """格式化为文本输出"""
    lines = []

    lines.append(f"📦 批量快递查询报告")
    lines.append(f"📊 查询时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"📈 总计：{len(results)} 个快递")
    lines.append("")

    for i, result in enumerate(results, 1):
        lines.append("━" * 50)
        lines.append(f"【{i}】 {result['nu']}")

        if result.get('com_name'):
            lines.append(f"    快递公司：{result['com_name']}")

        lines.append(f"    🔗 查询链接：{result['query_url']}")
        lines.append("")

    lines.append("━" * 50)
    lines.append("")
    lines.append("💡 提示：点击上方链接在快递100查看详细物流信息")

    return '\n'.join(lines)


def format_batch_markdown(results: list) -> str:
    """格式化为 Markdown 输出"""
    lines = []

    lines.append(f"# 📦 批量快递查询报告")
    lines.append("")
    lines.append(f"- **查询时间**：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- **总计**：{len(results)} 个快递")
    lines.append("")

    # 汇总表格
    lines.append("## 📊 查询汇总")
    lines.append("")
    lines.append("| 序号 | 快递单号 | 快递公司 | 查询链接 |")
    lines.append("|------|---------|---------|---------|")

    for i, result in enumerate(results, 1):
        com_name = result.get('com_name', '-')
        lines.append(f"| {i} | {result['nu']} | {com_name} | [链接]({result['query_url']}) |")

    lines.append("")
    lines.append("## 💡 提示")
    lines.append("点击表格中的链接在快递100查看详细物流信息")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='批量快递查询工具')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', help='快递列表文件')
    group.add_argument('--nus', help='快递单号列表，逗号分隔')

    parser.add_argument('--format', choices=['text', 'json', 'markdown'], default='text', help='输出格式')
    parser.add_argument('--output', help='输出到文件')

    args = parser.parse_args()

    # 准备快递列表
    express_list = []

    if args.file:
        express_list = read_express_list(args.file)
    elif args.nus:
        nus = args.nus.split(',')
        for nu in nus:
            nu = nu.strip()
            if nu:
                express_list.append({'nu': nu, 'com': None})

    if not express_list:
        print("没有有效的快递单号")
        sys.exit(1)

    # 批量处理
    results = batch_process(express_list)

    # 格式化输出
    if args.format == 'json':
        output = json.dumps(results, ensure_ascii=False, indent=2)
    elif args.format == 'markdown':
        output = format_batch_markdown(results)
    else:
        output = format_batch_text(results)

    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已保存到：{args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
