#!/usr/bin/env python3
"""
精读笔记质量巡检脚本

检查项目：
1. 原文引用数量（≥3段）
2. 笔记字数下限（≥2000字）
3. 双链数量（≥2个）
4. 疑难标注（≥1个）

用法：
    python3 quality_check.py <note_file.md>
"""

import sys
import re
from pathlib import Path


def check_note(filepath: str) -> dict:
    """检查笔记质量"""
    path = Path(filepath)
    
    if not path.exists():
        return {"error": f"文件不存在: {filepath}"}
    
    content = path.read_text(encoding="utf-8")
    
    results = {
        "file": filepath,
        "passed": True,
        "checks": []
    }
    
    # 检查1：原文引用数量（≥3段）
    # 匹配 > 开头的引用块
    quote_pattern = r'^>\s+.+$'
    quotes = re.findall(quote_pattern, content, re.MULTILINE)
    quote_count = len(quotes)
    quote_passed = quote_count >= 3
    results["checks"].append({
        "name": "原文引用",
        "required": "≥3段",
        "actual": f"{quote_count}段",
        "passed": quote_passed
    })
    if not quote_passed:
        results["passed"] = False
    
    # 检查2：笔记字数下限（≥2000字）
    # 统计中文字符和英文单词
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    english_words = len(re.findall(r'[a-zA-Z]+', content))
    total_words = chinese_chars + english_words
    word_passed = total_words >= 2000
    results["checks"].append({
        "name": "笔记字数",
        "required": "≥2000字",
        "actual": f"{total_words}字",
        "passed": word_passed
    })
    if not word_passed:
        results["passed"] = False
    
    # 检查3：双链数量（≥2个）
    # 匹配 [[书名/章节]] 格式
    link_pattern = r'\[\[.+?\]\]'
    links = re.findall(link_pattern, content)
    link_count = len(links)
    link_passed = link_count >= 2
    results["checks"].append({
        "name": "跨文本关联",
        "required": "≥2个双链",
        "actual": f"{link_count}个",
        "passed": link_passed
    })
    if not link_passed:
        results["passed"] = False
    
    # 检查4：疑难标注（≥1个）
    # 匹配数字+问号 或 "问题"+"？" 的格式
    question_pattern = r'\d+\.\s*.+[？?]|问题.+[？?]'
    questions = re.findall(question_pattern, content)
    question_count = len(questions)
    question_passed = question_count >= 1
    results["checks"].append({
        "name": "疑难标注",
        "required": "≥1个问题",
        "actual": f"{question_count}个",
        "passed": question_passed
    })
    if not question_passed:
        results["passed"] = False
    
    return results


def print_report(results: dict):
    """打印检查报告"""
    print("\n" + "="*50)
    print(f"📝 精读笔记质量检查报告")
    print("="*50)
    print(f"文件: {results['file']}")
    print("-"*50)
    
    for check in results["checks"]:
        status = "✅" if check["passed"] else "❌"
        print(f"{status} {check['name']}: {check['actual']} (要求: {check['required']})")
    
    print("-"*50)
    if results["passed"]:
        print("✅ 所有检查通过！")
    else:
        print("❌ 存在不达标项，请补充完善。")
    print("="*50 + "\n")


def main():
    if len(sys.argv) < 2:
        print("用法: python3 quality_check.py <note_file.md>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    results = check_note(filepath)
    
    if "error" in results:
        print(f"❌ 错误: {results['error']}")
        sys.exit(1)
    
    print_report(results)
    
    # 返回退出码
    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
