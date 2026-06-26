#!/usr/bin/env python3
"""
AI 驱动的 CSV 列检测器
让 AI 观察 CSV 前 N 行数据，智能识别正确的列索引
"""

import csv
import json
import sys
from pathlib import Path


def read_csv_sample(csv_path: str, max_rows: int = 20) -> dict:
    """
    读取 CSV 文件的前 N 行用于 AI 分析

    Returns:
        包含表头和样本数据的字典
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"文件不存在: {csv_path}")

    sample_data = {
        "file_name": csv_path.name,
        "total_rows": 0,
        "headers": [],
        "sample_rows": []
    }

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)

        # 读取表头
        try:
            headers = next(reader)
            sample_data["headers"] = headers
        except StopIteration:
            return sample_data

        # 读取样本数据
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
            # 只保存非空行
            if row and any(cell.strip() for cell in row):
                sample_data["sample_rows"].append(row)

        sample_data["total_rows"] = i + 1

    return sample_data


def create_ai_prompt(sample_data: dict) -> str:
    """
    创建 AI 分析提示词

    Args:
        sample_data: CSV 样本数据

    Returns:
        AI 提示词
    """
    headers = sample_data["headers"]
    rows = sample_data["sample_rows"][:5]  # 只用前5行作为示例

    # 构建表头展示
    header_display = "\n".join([
        f"列{i}: {h}" for i, h in enumerate(headers) if h
    ])

    # 构建数据行展示
    row_displays = []
    for row_idx, row in enumerate(rows[:3], 1):
        row_display = f"行{row_idx}: " + " | ".join([
            f"[{i}]{str(row[i])[:50] if i < len(row) else ''}"
            for i in range(min(len(headers), len(row)))
        ])
        row_displays.append(row_display)

    return f"""你是一个 CSV 数据分析专家。请分析以下电商评论数据的 CSV 结构，找出正确的列索引。

# CSV 表头
{header_display}

# 样本数据（前3行）
{chr(10).join(row_displays)}

# 你的任务

请仔细观察以上数据，找出以下列的**索引号**（从 0 开始）：

1. **rating_col**: 评分/星级列
   - 特征：包含数字 1-5，或包含 "star"、"rating"、"评分" 等关键词
   - 可能是 SVG URL（如 stars-5.svg）

2. **title_col**: 评论标题列（如果有）
   - 特征：简短的标题，通常 5-20 个字
   - 可能包含 "title"、"标题"、"subject" 等关键词

3. **content_col**: 评论内容列（必需）
   - 特征：较长的评论文本，通常 50-500 字
   - 这是核心列，请务必仔细识别
   - **跳过 CSS 类名列**（如 typography_body-m__k2UI7 这种包含 __ 或 class 关键词的）
   - 寻找真正包含用户评论内容的列

# 输出格式

请**只输出 JSON**，不要有任何其他文字：

```json
{{
  "rating_col": 索引数字,
  "title_col": 索引数字或null,
  "content_col": 索引数字,
  "confidence": "high/medium/low",
  "reasoning": "简短说明你的判断依据"
}}
```

# 注意事项

- 如果没有标题列，title_col 设为 null
- content_col 是最重要的，请确保找到正确的评论内容列
- confidence 表示你的判断信心程度
- reasoning 简要说明你如何识别这些列（比如"列7包含stars-5.svg"）
"""


def detect_columns_with_ai(csv_path: str) -> dict:
    """
    使用 AI 检测 CSV 列索引

    Args:
        csv_path: CSV 文件路径

    Returns:
        列索引映射字典
    """
    print(f"📂 正在分析 CSV 文件: {csv_path}")

    # 读取样本数据
    sample_data = read_csv_sample(csv_path, max_rows=20)

    if not sample_data["headers"]:
        raise ValueError("CSV 文件没有表头或为空")

    print(f"📊 CSV 信息:")
    print(f"   总列数: {len(sample_data['headers'])}")
    print(f"   样本行数: {len(sample_data['sample_rows'])}")
    print(f"   总行数: {sample_data['total_rows']}")

    # 生成提示词
    prompt = create_ai_prompt(sample_data)

    # 输出提示词供 AI 使用
    print("\n" + "=" * 60)
    print("🤖 请将以下内容发送给 AI 进行分析:")
    print("=" * 60)
    print(prompt)
    print("=" * 60)

    # 返回提示词供外部使用
    return {
        "prompt": prompt,
        "sample_data": sample_data
    }


def parse_ai_response(response_text: str) -> dict:
    """
    解析 AI 返回的 JSON 结果

    Args:
        response_text: AI 返回的文本

    Returns:
        解析后的列索引字典
    """
    # 提取 JSON 代码块
    import re

    # 查找 ```json ... ``` 代码块
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # 如果没有代码块，尝试直接解析
        json_str = response_text.strip()

    try:
        result = json.loads(json_str)
        print("\n✅ AI 检测结果:")
        print(f"   rating_col: {result.get('rating_col')}")
        print(f"   title_col: {result.get('title_col')}")
        print(f"   content_col: {result.get('content_col')}")
        print(f"   confidence: {result.get('confidence')}")
        print(f"   reasoning: {result.get('reasoning')}")
        return result
    except json.JSONDecodeError as e:
        print(f"\n❌ 解析 AI 响应失败: {e}")
        print(f"原始响应: {response_text[:200]}")
        raise


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='AI 驱动的 CSV 列检测器')
    parser.add_argument('input_csv', help='输入 CSV 文件路径')
    parser.add_argument('--save-prompt', help='将提示词保存到文件')
    parser.add_argument('--parse-response', help='解析 AI 响应（从文件或字符串）')

    args = parser.parse_args()

    # 模式1: 生成提示词
    if not args.parse_response:
        result = detect_columns_with_ai(args.input_csv)

        if args.save_prompt:
            with open(args.save_prompt, 'w', encoding='utf-8') as f:
                f.write(result['prompt'])
            print(f"\n💾 提示词已保存到: {args.save_prompt}")

        # 同时保存样本数据供调试
        sample_file = Path(args.input_csv).stem + '_sample.json'
        with open(sample_file, 'w', encoding='utf-8') as f:
            json.dump(result['sample_data'], f, ensure_ascii=False, indent=2)
        print(f"💾 样本数据已保存到: {sample_file}")

    # 模式2: 解析 AI 响应
    else:
        # 从文件读取或直接使用字符串
        try:
            with open(args.parse_response, 'r', encoding='utf-8') as f:
                response_text = f.read()
        except FileNotFoundError:
            response_text = args.parse_response

        column_map = parse_ai_response(response_text)

        # 输出为可用的参数格式
        print("\n" + "=" * 60)
        print("📋 可用于 csv_processor.py 的参数:")
        print("=" * 60)
        print(f"--rating-col {column_map['rating_col']} \\")
        print(f"--content-col {column_map['content_col']}")
        if column_map.get('title_col'):
            print(f"--title-col {column_map['title_col']}")


if __name__ == "__main__":
    main()
