#!/usr/bin/env python3
"""
summarize.py - 生成新闻摘要

调用 LLM 为每条新闻生成一句话摘要。
支持批量处理以提高效率。

用法:
    python summarize.py --input deduped.json --output summarized.json [--max-length 50]

注意:
    此脚本需要与 OpenClaw 集成，通过 agent 调用 LLM。
     standalone 模式下仅返回原始标题作为占位符。
"""

import json
import sys
from pathlib import Path

def generate_summary(title, snippet="", max_length=50):
    """
    生成一句话摘要
    
    在 OpenClaw 环境中，这里会调用 LLM。
    Standalone 模式下返回标题的简化版本。
    """
    # Standalone 模式：使用标题作为摘要（简化版）
    # 实际使用时，OpenClaw 会替换此逻辑为真正的 LLM 调用
    
    summary = title
    
    # 如果标题太长，截断
    if len(summary) > max_length:
        summary = summary[:max_length-3] + "..."
    
    return summary

def summarize_items(items, max_length=50):
    """
    为所有新闻项生成摘要
    
    返回:
    {
        "items": [
            {"title": "...", "url": "...", "summary": "..."},
            ...
        ],
        "processed_count": int
    }
    """
    result_items = []
    
    for item in items:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        
        summary = generate_summary(title, snippet, max_length)
        
        result_items.append({
            "title": title,
            "url": item.get("url", ""),
            "summary": summary,
            "source": item.get("source", "unknown"),
            "snippet": snippet  # 保留原始 snippet 供参考
        })
    
    return {
        "items": result_items,
        "processed_count": len(result_items),
        "max_length": max_length
    }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="生成新闻摘要")
    parser.add_argument("--input", type=str, required=True,
                        help="输入文件路径 (JSON)")
    parser.add_argument("--output", type=str, default="",
                        help="输出文件路径")
    parser.add_argument("--max-length", type=int, default=50,
                        help="摘要最大长度 (默认 50 字)")
    
    args = parser.parse_args()
    
    # 读取输入
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    items = data.get("items", [])
    
    # 生成摘要
    result = summarize_items(items, args.max_length)
    
    # 输出结果
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"摘要生成完成：{result['processed_count']} 条", file=sys.stderr)
    else:
        print(output)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
