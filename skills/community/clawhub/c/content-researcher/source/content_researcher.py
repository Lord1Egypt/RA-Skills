#!/usr/bin/env python3
"""
Content Researcher - 内容研究员
批量搜索、收集、总结内容，生成结构化素材库
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def search_web(query: str, max_results: int = 10):
    """使用 web_search 工具搜索"""
    try:
        # 调用 OpenClaw web_search 工具
        result = subprocess.run(
            ["claw", "tools", "web_search", "--query", query, "--count", str(max_results), "--json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"⚠️  搜索失败: {result.stderr}")
            return []
    except Exception as e:
        print(f"⚠️  搜索异常: {e}")
        return []


def summarize_text(text: str, model: str = "google/gemini-3-flash-preview") -> str:
    """使用 summarize 工具总结文本"""
    try:
        # 调用 summarize 工具
        result = subprocess.run(
            ["summarize", "--model", model, "--length", "medium"],
            input=text,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"⚠️  总结失败: {result.stderr}")
            return text[:500] + "..."
    except Exception as e:
        print(f"⚠️  总结异常: {e}")
        return text[:500] + "..."


def generate_report(keywords: list, results: list, output_format: str = "markdown") -> str:
    """生成调研报告"""

    if output_format == "markdown":
        report = []
        report.append(f"# 内容调研报告")
        report.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**关键词**：{', '.join(keywords)}")
        report.append("")

        report.append("## 📊 搜索结果概览")
        report.append(f"共找到 {len(results)} 条相关结果")
        report.append("")

        for i, item in enumerate(results, 1):
            report.append(f"### {i}. {item.get('title', '无标题')}")
            report.append(f"**来源**：{item.get('source', item.get('url', '未知'))}")
            report.append(f"**链接**：{item.get('url', '无')}")
            report.append("")
            if 'snippet' in item:
                report.append("**摘要**：")
                report.append(item['snippet'])
                report.append("")
            if 'summary' in item:
                report.append("**AI 总结**：")
                report.append(item['summary'])
                report.append("")
            report.append("---")
            report.append("")

        report.append("## 📈 趋势分析")
        report.append("（需要更多数据才能进行趋势分析）")
        report.append("")

        report.append("## 💡 关键发现")
        report.append("- " + "\n- ".join([f"结果 {i+1} 提供了关于 {keywords[0]} 的最新信息" for i in range(min(5, len(results)))]))

        return "\n".join(report)
    else:
        return json.dumps({
            "keywords": keywords,
            "generated_at": datetime.now().isoformat(),
            "total_results": len(results),
            "results": results
        }, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="内容研究员——批量搜索、总结内容，生成结构化素材库"
    )
    parser.add_argument("--keywords", required=True,
                        help="搜索关键词，逗号分隔（如：AI,自媒体,内容创作）")
    parser.add_argument("--max-results", type=int, default=20,
                        help="总结果数限制（默认 20）")
    parser.add_argument("--per-keyword", type=int, default=10,
                        help="每个关键词搜索数量（默认 10）")
    parser.add_argument("--output", default="content_research_report.md",
                        help="输出文件路径")
    parser.add_argument("--summarize", action="store_true",
                        help="为每个结果生成 AI 总结（慢，但更有用）")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown",
                        help="输出格式")
    parser.add_argument("--model", default="google/gemini-3-flash-preview",
                        help="总结模型（默认：google/gemini-3-flash-preview）")

    args = parser.parse_args()

    # 解析关键词
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    if not keywords:
        print("❌ 至少需要提供一个关键词")
        sys.exit(1)

    print(f"🔍 开始内容调研，关键词：{', '.join(keywords)}")
    print(f"📊 每个关键词搜索数量：{args.per_keyword}")
    print(f"🎯 目标总结果数：{args.max_results}")

    all_results = []

    # 搜索每个关键词
    for keyword in keywords:
        print(f"\n🔎 搜索：{keyword}")
        try:
            results = search_web(keyword, max_results=args.per_keyword)
            if results:
                print(f"✅ 找到 {len(results)} 条结果")
                for r in results:
                    r['_keyword'] = keyword  # 标记来源关键词
                all_results.extend(results)
            else:
                print("⚠️  无结果")
        except Exception as e:
            print(f"❌ 搜索错误: {e}")

    # 去重（基于 URL）
    seen_urls = set()
    unique_results = []
    for r in all_results:
        url = r.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)

    print(f"\n📈 去重后共 {len(unique_results)} 条结果")

    # 截取到最大数量
    if len(unique_results) > args.max_results:
        unique_results = unique_results[:args.max_results]
        print(f"✂️  截取前 {args.max_results} 条")

    # 为每个结果生成 AI 总结（如果启用）
    if args.summarize:
        print("\n🤖 正在生成 AI 总结（这可能需要几分钟）...")
        for i, result in enumerate(unique_results, 1):
            print(f"  [{i}/{len(unique_results)}] 处理：{result.get('title', '无标题')[:50]}...")
            text_to_summarize = result.get('snippet', '')
            if text_to_summarize:
                try:
                    summary = summarize_text(text_to_summarize, args.model)
                    result['summary'] = summary
                except Exception as e:
                    result['summary'] = f"总结失败：{e}"
            else:
                result['summary'] = "无内容可总结"

    # 生成报告
    print(f"\n📝 生成 {args.format} 格式报告...")
    report = generate_report(keywords, unique_results, args.format)

    # 保存文件
    output_path = Path(args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ 报告已保存：{output_path.absolute()}")
    print(f"📄 文件大小：{output_path.stat().st_size / 1024:.1f} KB")

    # 生成摘要
    print(f"\n📊 调研摘要：")
    print(f"   关键词：{len(keywords)} 个")
    print(f"   总结果：{len(unique_results)} 条")
    print(f"   已总结：{sum(1 for r in unique_results if 'summary' in r)} 条")
    print(f"   输出格式：{args.format}")


if __name__ == "__main__":
    main()
