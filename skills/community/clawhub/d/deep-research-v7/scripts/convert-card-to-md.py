#!/usr/bin/env python3
"""
convert-card-to-md.py - 将JSON卡片转换为Markdown格式

用法: python convert-card-to-md.py <card_json_file> [options]
       python convert-card-to-md.py <card_id> --by-id [options]

示例:
  python convert-card-to-md.py sources/card-web-001.json
  python convert-card-to-md.py card-web-001 --by-id
  python convert-card-to-md.py sources/card-web-001.json --output cards/
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


def format_date(date_str: Optional[str]) -> str:
    """格式化日期字符串"""
    if not date_str:
        return "未知"
    
    # 尝试解析常见格式
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.split('+')[0].split('.')[0], fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    return date_str[:10] if len(date_str) > 10 else date_str


def generate_markdown_card(card_data: Dict[str, Any]) -> str:
    """
    将卡片数据转换为Markdown格式
    
    遵循深度研究v6.0卡片规范
    """
    
    source = card_data.get("source", {})
    content = card_data.get("content", {})
    metrics = card_data.get("extracted_metrics", {})
    quality = card_data.get("quality", {})
    verification = card_data.get("verification_status", {})
    meta = card_data.get("meta", {})
    
    card_id = card_data.get("card_id", "unknown")
    title = source.get("title", "无标题")
    url = source.get("url", "")
    source_type = source.get("type", "unknown")
    
    # 构建Markdown
    md_lines = []
    
    # 头部元数据
    md_lines.append("---")
    md_lines.append(f"card_id: {card_id}")
    md_lines.append(f"source_type: {source_type}")
    md_lines.append(f"data_level: {content.get('data_level', 'unknown')}")
    md_lines.append(f"credibility: {quality.get('credibility', 'unknown')}")
    md_lines.append(f"word_count: {content.get('word_count', 0)}")
    md_lines.append(f"domain: {meta.get('domain', 'general')}")
    md_lines.append(f"created: {card_data.get('created_at', datetime.now().isoformat())[:10]}")
    md_lines.append("---")
    md_lines.append("")
    
    # 标题
    md_lines.append(f"# {title}")
    md_lines.append("")
    
    # 来源信息区块
    md_lines.append("## 来源信息")
    md_lines.append("")
    md_lines.append(f"- **URL**: [{url}]({url})")
    md_lines.append(f"- **来源类型**: {source_type.upper()}")
    md_lines.append(f"- **作者**: {source.get('author') or '*未识别*'}")
    md_lines.append(f"- **发布日期**: {format_date(source.get('published_date'))}")
    md_lines.append(f"- **访问时间**: {format_date(source.get('accessed_at'))}")
    md_lines.append("")
    
    # 内容预览
    md_lines.append("## 内容预览")
    md_lines.append("")
    preview = content.get("preview", "")
    if preview:
        md_lines.append(f"> {preview.replace(chr(10), chr(10)+'> ')}")
    else:
        md_lines.append("*无内容预览*")
    md_lines.append("")
    
    # 提取指标
    md_lines.append("## 关键指标")
    md_lines.append("")
    
    paper_type = quality.get('paper_type', 'unknown')
    has_quantitative = quality.get('has_quantitative_metrics', False)
    
    if paper_type == 'methodology':
        # 方法类论文显示方法描述表格
        md_lines.append("| 指标类型 | 提取结果 | 说明 |")
        md_lines.append("|----------|----------|------|")
        if "method_name" in metrics:
            md_lines.append(f"| 方法名称 | {metrics['method_name']} | 核心贡献 |")
        if "key_innovation" in metrics:
            md_lines.append(f"| 关键创新 | {metrics['key_innovation'][:50]}... | 技术创新点 |")
        if "baseline" in metrics:
            md_lines.append(f"| 对比基线 | {metrics['baseline'][:50]}... | 传统方法 |")
        if "application" in metrics:
            md_lines.append(f"| 适用场景 | {metrics['application'][:50]}... | 应用范围 |")
        md_lines.append(f"| 量化指标 | {'✅ 已报告' if has_quantitative else '⚠️ 未报告'} | {'含数值统计' if has_quantitative else '本文聚焦方法设计'} |")
    elif has_quantitative:
        # 性能类论文显示定量指标表格
        md_lines.append("| 指标 | 数值 | 单位/上下文 |")
        md_lines.append("|------|------|-------------|")
        if "sample_size" in metrics:
            md_lines.append(f"| 样本量 | {metrics['sample_size']} | 人 |")
        if "auc" in metrics:
            md_lines.append(f"| AUC | {metrics['auc']} | - |")
        if "accuracy" in metrics:
            md_lines.append(f"| 准确率 | {metrics['accuracy']}% | 百分比 |")
        if "sensitivity" in metrics:
            md_lines.append(f"| 敏感性 | {metrics['sensitivity']}% | 百分比 |")
        if "specificity" in metrics:
            md_lines.append(f"| 特异性 | {metrics['specificity']}% | 百分比 |")
        if "f1_score" in metrics:
            md_lines.append(f"| F1 Score | {metrics['f1_score']} | - |")
        if "precision" in metrics:
            md_lines.append(f"| 精确率 | {metrics['precision']} | - |")
        if "recall" in metrics:
            md_lines.append(f"| 召回率 | {metrics['recall']} | - |")
    else:
        md_lines.append("*未提取到定量指标*")
    
    md_lines.append("")
    
    # 数据质量评估
    md_lines.append("## 数据质量评估")
    md_lines.append("")
    md_lines.append(f"- **数据级别**: {content.get('data_level', 'unknown').upper()}")
    md_lines.append(f"- **可信度**: {quality.get('credibility', 'unknown').upper()}")
    md_lines.append(f"- **全文可用**: {'✅ 是' if quality.get('has_full_text') else '⚠️ 否'} ({content.get('word_count', 0)} 字)")
    md_lines.append(f"- **有定量指标**: {'✅ 是' if quality.get('has_quantitative_metrics') else '❌ 否'}")
    md_lines.append("")
    
    # 验证状态（v6.0诚实度）
    md_lines.append("## 验证状态")
    md_lines.append("")
    
    if verification.get("needs_manual_check"):
        md_lines.append("⚠️ **需要人工复核**: 内容较短，数据可能不完整")
        md_lines.append("")
    
    missing = verification.get("missing_fields", [])
    if missing:
        md_lines.append("**缺失字段**:")
        for field in missing:
            field_names = {
                "author": "作者信息",
                "published_date": "发布日期",
                "quantitative_data": "定量数据"
            }
            md_lines.append(f"- ⚠️ {field_names.get(field, field)}")
    else:
        md_lines.append("✅ **数据完整**")
    
    # 验证建议
    suggestions = verification.get("suggestions", [])
    if suggestions:
        md_lines.append("")
        md_lines.append("### 验证建议")
        md_lines.append("")
        for suggestion in suggestions:
            md_lines.append(f"- {suggestion}")
    
    md_lines.append("")
    
    # 原文直接引用
    key_quote = card_data.get("key_quote", {})
    if key_quote and key_quote.get("quote"):
        md_lines.append("## 原文直接引用")
        md_lines.append("")
        md_lines.append(f"> \"{key_quote['quote']}\"")
        md_lines.append(f"> —— {key_quote.get('location', 'Unknown')}")
        md_lines.append("")
    
    # 完整内容（可选，如果字数适中）
    full_text = content.get("full_text")
    if full_text and content.get("word_count", 0) < 3000:
        md_lines.append("## 完整内容")
        md_lines.append("")
        md_lines.append("<details>")
        md_lines.append("<summary>点击展开全文</summary>")
        md_lines.append("")
        md_lines.append(full_text)
        md_lines.append("")
        md_lines.append("</details>")
        md_lines.append("")
    
    # 元数据
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("*卡片由 Web Fetcher v1.1 + Deep Research v6.0 自动生成*")
    md_lines.append(f"*抓取重试次数: {meta.get('retries_used', 0)}*")
    
    return "\n".join(md_lines)


def convert_card(
    input_path: Path,
    output_dir: Optional[Path] = None,
    verbose: bool = False
) -> Optional[Path]:
    """
    转换单个JSON卡片为Markdown
    
    Returns:
        输出文件路径，失败返回None
    """
    
    if verbose:
        print(f"[Convert] 读取: {input_path}")
    
    # 读取JSON
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            card_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        return None
    except FileNotFoundError:
        print(f"❌ 文件不存在: {input_path}")
        return None
    
    # 生成Markdown
    markdown = generate_markdown_card(card_data)
    
    # 确定输出路径
    card_id = card_data.get("card_id", input_path.stem)
    
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{card_id}.md"
    else:
        output_path = input_path.with_suffix('.md')
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    if verbose:
        print(f"[Convert] 输出: {output_path}")
    
    return output_path


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="将JSON卡片转换为Markdown格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换单个文件
  python convert-card-to-md.py sources/card-web-001.json
  
  # 通过ID转换（自动查找sources/目录）
  python convert-card-to-md.py card-web-001 --by-id
  
  # 指定输出目录
  python convert-card-to-md.py sources/card-web-001.json --output cards/
  
  # 批量转换
  python convert-card-to-md.py sources/*.json
        """
    )
    
    parser.add_argument("input", help="输入文件路径或卡片ID")
    parser.add_argument("--by-id", "-i", action="store_true",
                       help="通过ID查找（自动在sources/目录查找）")
    parser.add_argument("--output", "-o", type=Path,
                       help="输出目录（默认与输入同目录）")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="详细日志")
    
    args = parser.parse_args()
    
    # 确定输入文件
    if args.by_id:
        input_path = Path("sources") / f"{args.input}.json"
    else:
        input_path = Path(args.input)
    
    # 检查是否为通配符批量处理
    if '*' in str(input_path):
        import glob
        files = glob.glob(str(input_path))
        if not files:
            print(f"❌ 未找到匹配文件: {input_path}")
            sys.exit(1)
        
        print(f"批量转换 {len(files)} 个文件...")
        success_count = 0
        for f in files:
            output = convert_card(Path(f), args.output, args.verbose)
            if output:
                success_count += 1
                print(f"✅ {f} -> {output}")
        
        print(f"\n完成: {success_count}/{len(files)} 个文件转换成功")
    else:
        # 单文件转换
        output = convert_card(input_path, args.output, args.verbose)
        
        if output:
            print(f"✅ 转换成功: {output}")
            sys.exit(0)
        else:
            print(f"❌ 转换失败")
            sys.exit(1)


if __name__ == "__main__":
    main()
