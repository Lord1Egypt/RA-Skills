#!/usr/bin/env python3
"""
日报质量检查脚本
检测报告内容的完整性和质量
"""

import sys
from pathlib import Path

def check_report_quality(report_path):
    """检查报告质量"""
    if not Path(report_path).exists():
        return {
            "score": 0,
            "stars": "❌",
            "reason": "报告文件不存在",
            "sections_found": [],
            "quality_found": [],
            "issues": ["报告文件不存在"],
        }
    
    content = Path(report_path).read_text()
    if len(content.strip()) == 0:
        return {
            "score": 0,
            "stars": "❌",
            "reason": "报告文件为空",
            "char_count": 0,
            "sections_found": [],
            "quality_found": [],
            "issues": ["报告文件为空"],
        }
    
    content = Path(report_path).read_text()
    issues = []
    score = 0
    max_score = 100
    
    # 1. 字数检查（30分）
    char_count = len(content)
    if char_count < 100:
        issues.append(f"字数不足（{char_count} < 100）")
    elif char_count < 200:
        score += 15
        issues.append(f"字数偏少（{char_count}）")
    elif char_count < 500:
        score += 25
    else:
        score += 30
    
    # 2. 核心板块检查（40分）
    sections = {
        "今日工作": 0,
        "复盘": 0,
        "建议": 0,
        "明日": 0,
        "学习": 0,
    }
    
    for section in sections:
        if f"## {section}" in content or f"### {section}" in content:
            score += 8
            sections[section] = 1
        elif section in content:
            score += 4
            sections[section] = 0.5
    
    missing = [k for k, v in sections.items() if v == 0]
    if missing:
        issues.append(f"缺少板块: {', '.join(missing)}")
    
    # 3. 内容质量检查（30分）
    quality_indicators = [
        ("完成", 5, "有具体完成项"),
        ("修复", 5, "有修复/问题解决"),
        ("实现", 5, "有实现内容"),
        ("优化", 5, "有优化改进"),
        ("TODO", 2, "有计划安排"),
        ("问题", 3, "有问题分析"),
        ("学习", 3, "有学习内容"),
    ]
    
    quality_found = []
    for keyword, points, desc in quality_indicators:
        if keyword in content:
            score += points
            quality_found.append(desc)
    
    if not quality_found:
        issues.append("内容空洞，缺乏具体描述")
    
    # 星级评定
    if score >= 90:
        stars = "⭐⭐⭐"
    elif score >= 60:
        stars = "⭐⭐"
    elif score >= 30:
        stars = "⭐"
    else:
        stars = "❌"
    
    return {
        "score": min(score, max_score),
        "stars": stars,
        "char_count": char_count,
        "sections_found": [k for k, v in sections.items() if v > 0],
        "quality_found": quality_found,
        "issues": issues,
    }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 check_quality.py <报告文件路径> [--verbose|-v]")
        print("       python3 check_quality.py --check-only <报告路径>  # 只返回 exit code")
        sys.exit(1)
    
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    check_only = '--check-only' in sys.argv or '-c' in sys.argv
    
    # 解析报告路径（去掉 flag 参数）
    report_path = [a for a in sys.argv[1:] if not a.startswith('--') and not a.startswith('-')][0]
    
    result = check_report_quality(report_path)
    
    if not verbose and not check_only:
        print(f"\n📊 日报质量检查结果")
        print(f"{'=' * 40}")
        print(f"文件: {Path(report_path).name}")
        print(f"评分: {result['stars']} ({result['score']}/100)")
        print(f"字数: {result.get('char_count', 0)}")
        print(f"找到板块: {', '.join(result['sections_found']) or '无'}")
        
        if result['quality_found']:
            print(f"质量标识: {', '.join(result['quality_found'])}")
        
        if result['issues']:
            print(f"\n⚠️ 问题:")
            for issue in result['issues']:
                print(f"  - {issue}")
    
    # check-only 模式：只返回 exit code（0=合格，1=不合格）
    if check_only:
        sys.exit(0 if result['score'] >= 60 else 1)
    
    # 默认：返回 0（不被误判为错误）
    return 0

if __name__ == "__main__":
    sys.exit(main())
