#!/usr/bin/env python3
"""
解析 agent-browser eval --json 输出，提取豆包对话全文并保存。

用法:
    python3 parse_doubao.py [--input /tmp/doubao_raw.json] [--output /path/to/output.txt]
"""
import json
import argparse
import sys

def parse_and_save(input_path: str, output_path: str) -> int:
    try:
        with open(input_path) as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"文件未找到: {input_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}", file=sys.stderr)
        sys.exit(1)

    data = raw.get('data', {})
    result = data.get('result', '')

    if not result or result == 'NOT_FOUND':
        print("未能提取到内容，请确保豆包页面已完全加载且滚动到底部。", file=sys.stderr)
        sys.exit(1)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    char_count = len(result)
    print(f"提取成功: {char_count} 字 → {output_path}")
    return char_count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='解析豆包对话 JSON 并保存为文本文件')
    parser.add_argument('--input', '-i', default='/tmp/doubao_raw.json',
                        help='agent-browser eval --json 输出文件路径')
    parser.add_argument('--output', '-o',
                        default='./豆包对话全文.txt',
                        help='输出文本文件路径')
    args = parser.parse_args()
    parse_and_save(args.input, args.output)
