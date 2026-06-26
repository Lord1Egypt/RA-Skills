#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness Engineering - 导出报告脚本
生成Markdown或JSON格式的完整复盘报告
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

# 获取skill目录
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / "data"
LEDGER_FILE = DATA_DIR / "error_ledger.jsonl"


def load_errors() -> List[dict]:
    """加载所有错误记录"""
    errors = []
    if LEDGER_FILE.exists():
        with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        errors.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return errors


def filter_by_date_range(errors: List[dict], from_date: str, to_date: str) -> List[dict]:
    """按日期范围过滤"""
    filtered = []
    for error in errors:
        try:
            ts = datetime.fromisoformat(error.get('timestamp', ''))
            if from_date and ts < datetime.strptime(from_date, '%Y-%m-%d'):
                continue
            if to_date and ts > datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1):
                continue
            filtered.append(error)
        except (ValueError, TypeError):
            continue
    return filtered


def generate_markdown_report(errors: List[dict], output_path: str) -> str:
    """生成Markdown格式的复盘报告"""
    lines = []
    
    # 标题
    lines.append("# Harness Engineering 错误复盘报告")
    lines.append("")
    lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**错误总数**：{len(errors)}")
    lines.append("")
    
    if not errors:
        lines.append("## 🎉 暂无错误记录")
        lines.append("")
        lines.append("继续保持，让 OpenClaw 越来越聪明！")
        return '\n'.join(lines)
    
    # 统计概览
    lines.append("## 📊 统计概览")
    lines.append("")
    
    from collections import Counter
    
    type_counter = Counter(e.get('error_type', '未知') for e in errors)
    level_counter = Counter(e.get('level', '未知') for e in errors)
    status_counter = Counter(e.get('fix_status', '未知') for e in errors)
    
    lines.append("### 按错误类型")
    lines.append("")
    lines.append("| 错误类型 | 数量 | 占比 |")
    lines.append("|----------|------|------|")
    for et, count in type_counter.most_common():
        pct = round(count / len(errors) * 100, 1)
        lines.append(f"| {et} | {count} | {pct}% |")
    lines.append("")
    
    lines.append("### 按错误等级")
    lines.append("")
    lines.append("| 等级 | 数量 | 占比 |")
    lines.append("|------|------|------|")
    for lv in ['严重', '高', '中', '低']:
        count = level_counter.get(lv, 0)
        if count > 0:
            pct = round(count / len(errors) * 100, 1)
            lines.append(f"| {lv} | {count} | {pct}% |")
    lines.append("")
    
    lines.append("### 按修复状态")
    lines.append("")
    lines.append("| 状态 | 数量 | 占比 |")
    lines.append("|------|------|------|")
    for st, count in status_counter.most_common():
        pct = round(count / len(errors) * 100, 1)
        lines.append(f"| {st} | {count} | {pct}% |")
    lines.append("")
    
    fixed = status_counter.get('已修复', 0) + status_counter.get('已规避', 0)
    fix_rate = round(fixed / len(errors) * 100, 1)
    lines.append(f"**修复率**：{fix_rate}%")
    lines.append("")
    
    # 错误详情
    lines.append("## 📝 错误详情")
    lines.append("")
    
    for i, error in enumerate(errors, 1):
        lines.append(f"### {i}. {error.get('error_id', '未知')}")
        lines.append("")
        lines.append(f"- **时间**：{error.get('timestamp', '未知')}")
        lines.append(f"- **场景**：{error.get('scene', '未知')}")
        lines.append(f"- **类型**：{error.get('error_type', '未知')}")
        lines.append(f"- **等级**：{error.get('level', '未知')}")
        lines.append(f"- **状态**：{error.get('fix_status', '未知')}")
        lines.append(f"- **来源**：{error.get('source', '未知')}")
        if error.get('tags'):
            lines.append(f"- **标签**：{', '.join(error.get('tags', []))}")
        lines.append("")
        
        lines.append("**问题**：")
        lines.append(f"> {error.get('question', '无')}")
        lines.append("")
        
        lines.append("**错误回答**：")
        lines.append(f"```\n{error.get('wrong_answer', '无')}\n```")
        lines.append("")
        
        lines.append("**正确答案**：")
        lines.append(f"```\n{error.get('correct_answer', '无')}\n```")
        lines.append("")
        
        lines.append("**原因分析**：")
        lines.append(f"{error.get('reason', '无')}")
        lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # 改进建议
    lines.append("## 💡 改进建议")
    lines.append("")
    
    # 基于错误类型给出建议
    if '代码错误' in type_counter:
        lines.append("### 代码质量改进")
        lines.append("")
        lines.append("- 在回答代码问题前，先查询错误台账，避免重复犯错")
        lines.append("- 对于涉及编码、文件操作的代码，特别注意跨平台兼容性")
        lines.append("- 提供代码前先进行逻辑自查")
        lines.append("")
    
    if '逻辑错误' in type_counter:
        lines.append("### 逻辑推理改进")
        lines.append("")
        lines.append("- 回答涉及条件判断的问题时，列举所有边界情况")
        lines.append("- 对于复杂推理，先列出推理链条，再给出结论")
        lines.append("")
    
    if '漏信息' in type_counter:
        lines.append("### 完整性改进")
        lines.append("")
        lines.append("- 回答前先列出回答提纲，确保覆盖所有要点")
        lines.append("- 提供操作步骤时，包含前置条件检查")
        lines.append("")
    
    if '幻觉' in type_counter:
        lines.append("### 事实准确性改进")
        lines.append("")
        lines.append("- 对于不确定的事实，明确说明不确定性")
        lines.append("- 涉及版本、API等具体信息时，优先查询官方文档")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*本报告由 Harness Engineering 自动生成*")
    
    return '\n'.join(lines)


def generate_json_report(errors: List[dict]) -> dict:
    """生成JSON格式的报告"""
    from collections import Counter
    
    type_counter = Counter(e.get('error_type', '未知') for e in errors)
    level_counter = Counter(e.get('level', '未知') for e in errors)
    status_counter = Counter(e.get('fix_status', '未知') for e in errors)
    
    fixed = status_counter.get('已修复', 0) + status_counter.get('已规避', 0)
    fix_rate = round(fixed / len(errors) * 100, 1) if errors else 0
    
    return {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total": len(errors),
            "by_type": dict(type_counter),
            "by_level": dict(level_counter),
            "by_status": dict(status_counter),
            "fix_rate": fix_rate
        },
        "errors": errors
    }


def main():
    parser = argparse.ArgumentParser(description='导出错误复盘报告')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', 
                       help='输出格式')
    parser.add_argument('--from', dest='from_date', help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--to', dest='to_date', help='结束日期 (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # 加载错误
    errors = load_errors()
    
    # 按日期范围过滤
    if args.from_date or args.to_date:
        errors = filter_by_date_range(errors, args.from_date, args.to_date)
    
    # 生成报告
    if args.format == 'json':
        report = generate_json_report(errors)
        content = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        content = generate_markdown_report(errors, args.output)
    
    # 写入文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')
    
    print(json.dumps({
        "status": "ok",
        "output": str(output_path.absolute()),
        "format": args.format,
        "errors_count": len(errors)
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
