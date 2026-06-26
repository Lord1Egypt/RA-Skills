#!/usr/bin/env python3
"""
Skill 测试运行器
读取 evals.json，对每个测试用例执行检查，生成测试报告

用法：
python3 run_tests.py [--verbose] [--json]
"""

import json
import sys
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple

# 加载测试用例
EVALS_FILE = os.path.join(os.path.dirname(__file__), "..", "evals.json")


def load_evals() -> dict:
    with open(EVALS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def check_eval_pass(eval_item: dict, response: str) -> Tuple[bool, List[str]]:
    """
    检查测试用例是否通过
    
    返回: (是否通过, 未通过的关键词列表)
    """
    keywords = eval_item.get("keywords", [])
    missing_keywords = []
    
    response_lower = response.lower()
    
    for keyword in keywords:
        if keyword.lower() not in response_lower:
            missing_keywords.append(keyword)
    
    passed = len(missing_keywords) == 0
    return passed, missing_keywords


def run_cli_test(eval_item: dict) -> Tuple[str, bool]:
    """
    模拟 CLI 测试 - 用户输入 + 预期响应模式
    这里我们只做模式匹配，不真正调用 AI
    """
    prompt = eval_item["prompt"]
    expected = eval_item["expected_output"]
    category = eval_item["category"]
    eval_id = eval_item["id"]
    
    # 生成模拟响应（实际使用时，这里会调用 AI）
    # 这里我们假设 response 与 expected 一致（用于结构验证）
    mock_response = f"[模拟响应 - 实际使用时由 AI 生成]\n\n{expected}"
    
    return mock_response


def generate_test_report(evals_data: dict, results: List[dict]) -> str:
    """生成测试报告"""
    
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    
    report = f"""
================================================================================
                    Apollo 城投贸易风控智能体 - 测试报告
================================================================================

测试时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Skill 版本：{evals_data.get('version', 'unknown')}
测试用例数：{total}
通过：{passed} | 失败：{failed}
通过率：{passed/total*100:.1f}%

--------------------------------------------------------------------------------
                              测试结果详情
--------------------------------------------------------------------------------

"""
    
    for result in results:
        eval_item = result["eval"]
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        
        report += f"""
用例 #{result['id']} [{eval_item['category']}]
{status}
Prompt: {eval_item['prompt'][:60]}...
"""
        
        if not result["passed"]:
            report += f"  未命中关键词: {', '.join(result['missing'])}\n"
        
        report += "\n"
    
    report += f"""
================================================================================
                            测试结论
================================================================================

"""
    
    if passed == total:
        report += "🎉 所有测试用例通过！\n\n"
    else:
        report += f"⚠️  {failed} 个测试用例未通过，请检查对应用例。\n\n"
    
    # 统计各类别通过率
    by_category = {}
    for result in results:
        cat = result["eval"]["category"]
        if cat not in by_category:
            by_category[cat] = {"total": 0, "passed": 0}
        by_category[cat]["total"] += 1
        if result["passed"]:
            by_category[cat]["passed"] += 1
    
    report += "各类别通过率：\n"
    for cat, stats in by_category.items():
        rate = stats["passed"] / stats["total"] * 100
        report += f"  {cat}: {stats['passed']}/{stats['total']} ({rate:.0f}%)\n"
    
    return report


def main():
    print("🔍 Apollo 城投贸易风控智能体 - 测试运行器")
    print("=" * 50)
    
    # 加载测试用例
    evals_data = load_evals()
    evals_list = evals_data.get("evals", [])
    
    print(f"📋 加载了 {len(evals_list)} 个测试用例")
    print()
    
    # 读取 evaluation_guidelines
    guidelines = evals_data.get("evaluation_guidelines", {})
    print("评估标准：")
    print(f"  PASS: {guidelines.get('pass', 'N/A')}")
    print()
    
    # 运行测试
    results = []
    
    for eval_item in evals_list:
        eval_id = eval_item["id"]
        category = eval_item["category"]
        prompt = eval_item["prompt"]
        pass_criteria = eval_item.get("pass_criteria", "")
        
        print(f"[{eval_id}] {category}...", end=" ")
        
        # 模拟测试（实际使用时，这里会调用 AI）
        # 这里我们做一个简单的占位符测试
        response = f"[模拟输出 - 请在实际 AI 环境中运行此测试]"
        
        # 对于演示，我们标记所有为"待验证"
        passed = None
        missing = []
        
        results.append({
            "id": eval_id,
            "eval": eval_item,
            "passed": passed,
            "response": response,
            "missing": missing
        })
        
        print("⏳ 待验证")
    
    print()
    print("=" * 50)
    print("⚠️  注意：以上为模拟测试结果")
    print("    请在 AI 环境中实际运行测试用例进行验证")
    print()
    
    # 生成报告
    report = generate_test_report(evals_data, results)
    print(report)
    
    # 保存报告
    report_file = os.path.join(os.path.dirname(__file__), "..", "tests", "test_report.txt")
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"📄 报告已保存到: {report_file}")


if __name__ == "__main__":
    main()
