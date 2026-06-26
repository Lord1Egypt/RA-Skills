#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工作流验证脚本 - 检查各阶段产出质量

用法：
    python workflow_validator.py [输出目录]
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print_success(f"{description}: {filepath} ({size/1024:.1f} KB)")
        return True
    else:
        print_error(f"{description}: {filepath} (缺失)")
        return False

def check_json_file(filepath, description):
    """检查 JSON 文件是否有效"""
    if not os.path.exists(filepath):
        print_error(f"{description}: {filepath} (缺失)")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print_success(f"{description}: {filepath} (有效 JSON)")
        return True, data
    except json.JSONDecodeError as e:
        print_error(f"{description}: {filepath} (JSON 无效：{e})")
        return False, None

def validate_stage_1(output_dir):
    """验证阶段 1 产出"""
    print(f"\n{Colors.BOLD}阶段 1: Research（深度研究）{Colors.ENDC}")
    
    checks = {
        "research_report.md": "研究报告",
        "literature_search_results.json": "文献搜索结果"
    }
    
    all_passed = True
    for filename, description in checks.items():
        filepath = os.path.join(output_dir, filename)
        if not check_file_exists(filepath, description):
            all_passed = False
    
    # 检查研究报告字数
    report_path = os.path.join(output_dir, "research_report.md")
    if os.path.exists(report_path):
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        word_count = len(content.split())
        if word_count >= 25000:
            print_success(f"研究报告字数：{word_count} (≥25000 ✓)")
        else:
            print_warning(f"研究报告字数：{word_count} (<25000，可能深度不足)")
    
    # 检查文献数量
    results_path = os.path.join(output_dir, "literature_search_results.json")
    if os.path.exists(results_path):
        valid, data = check_json_file(results_path, "文献搜索结果")
        if valid and data:
            lit_count = len(data.get("results", []))
            if lit_count >= 180:
                print_success(f"文献数量：{lit_count} (≥180 ✓)")
            else:
                print_warning(f"文献数量：{lit_count} (<180，可能检索不足)")
    
    return all_passed

def validate_stage_2(output_dir):
    """验证阶段 2 产出"""
    print(f"\n{Colors.BOLD}阶段 2: Write（学术写作）{Colors.ENDC}")
    
    checks = {
        "paper_draft.md": "论文初稿",
        "references_raw.txt": "参考文献列表"
    }
    
    all_passed = True
    for filename, description in checks.items():
        filepath = os.path.join(output_dir, filename)
        if not check_file_exists(filepath, description):
            all_passed = False
    
    # 检查论文初稿字数
    draft_path = os.path.join(output_dir, "paper_draft.md")
    if os.path.exists(draft_path):
        with open(draft_path, 'r', encoding='utf-8') as f:
            content = f.read()
        word_count = len(content.split())
        if word_count >= 15000:
            print_success(f"论文初稿字数：{word_count} (≥15000 ✓)")
        else:
            print_warning(f"论文初稿字数：{word_count} (<15000，可能内容不足)")
    
    # 检查论文结构
    if os.path.exists(draft_path):
        with open(draft_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        required_sections = ["摘要", "引言", "结论", "参考文献"]
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if not missing_sections:
            print_success("论文结构完整（摘要、引言、结论、参考文献）")
        else:
            print_warning(f"缺少章节：{', '.join(missing_sections)}")
    
    return all_passed

def validate_stage_3(output_dir):
    """验证阶段 3 产出"""
    print(f"\n{Colors.BOLD}阶段 3: Citation（引用格式化）{Colors.ENDC}")
    
    checks = {
        "references_formatted.txt": "格式化参考文献",
        "citation_validation_report.json": "格式验证报告"
    }
    
    all_passed = True
    for filename, description in checks.items():
        filepath = os.path.join(output_dir, filename)
        if not check_file_exists(filepath, description):
            all_passed = False
    
    # 检查引用格式验证
    report_path = os.path.join(output_dir, "citation_validation_report.json")
    if os.path.exists(report_path):
        valid, data = check_json_file(report_path, "格式验证报告")
        if valid and data:
            errors = data.get("errors", 0)
            if errors == 0:
                print_success("引用格式验证：无错误 ✓")
            else:
                print_warning(f"引用格式错误：{errors} 条")
    
    return all_passed

def validate_stage_4(output_dir):
    """验证阶段 4 产出"""
    print(f"\n{Colors.BOLD}阶段 4: Integrity Check（初稿诚信检查）{Colors.ENDC}")
    
    checks = {
        "integrity_check_report_stage4.json": "初稿检查报告",
        "paper_draft_revised.md": "修复后初稿"
    }
    
    all_passed = True
    for filename, description in checks.items():
        filepath = os.path.join(output_dir, filename)
        if not check_file_exists(filepath, description):
            all_passed = False
    
    # 检查诚信检查报告
    report_path = os.path.join(output_dir, "integrity_check_report_stage4.json")
    if os.path.exists(report_path):
        valid, data = check_json_file(report_path, "初稿检查报告")
        if valid and data:
            errors = data.get("errors", 0)
            warnings = data.get("warnings", 0)
            
            if errors == 0:
                print_success("诚信检查：无错误 ✓")
            else:
                print_error(f"诚信检查错误：{errors} 条（必须修复）")
            
            if warnings == 0:
                print_success("诚信检查：无需核实 ✓")
            else:
                print_warning(f"需要核实：{warnings} 条")
    
    return all_passed

def validate_stage_5(output_dir):
    """验证阶段 5 产出"""
    print(f"\n{Colors.BOLD}阶段 5: Review → Revise（多轮评审）{Colors.ENDC}")
    
    checks = {
        "review_reports_round1.json": "第 1 轮评审报告",
        "review_reports_round2.json": "第 2 轮评审报告",
        "review_reports_round3.json": "第 3 轮评审报告",
        "paper_final.md": "最终稿"
    }
    
    all_passed = True
    for filename, description in checks.items():
        filepath = os.path.join(output_dir, filename)
        if not check_file_exists(filepath, description):
            all_passed = False
    
    # 检查评审意见数量趋势
    for round_num in [1, 2, 3]:
        report_path = os.path.join(output_dir, f"review_reports_round{round_num}.json")
        if os.path.exists(report_path):
            valid, data = check_json_file(report_path, f"第{round_num}轮评审报告")
            if valid and data:
                opinions = len(data.get("opinions", []))
                if round_num == 1 and opinions >= 10:
                    print_success(f"第{round_num}轮评审意见：{opinions} 条（正常）")
                elif round_num == 2 and opinions <= 5:
                    print_success(f"第{round_num}轮评审意见：{opinions} 条（减少 ✓）")
                elif round_num == 3 and opinions == 0:
                    print_success(f"第{round_num}轮评审意见：{opinions} 条（通过 ✓）")
                else:
                    print_warning(f"第{round_num}轮评审意见：{opinions} 条")
    
    return all_passed

def validate_stage_6(output_dir):
    """验证阶段 6 产出"""
    print(f"\n{Colors.BOLD}阶段 6: Final Integrity Check（终稿验证）{Colors.ENDC}")
    
    checks = {
        "final_integrity_check_report.json": "终稿验证报告"
    }
    
    all_passed = True
    for filename, description in checks.items():
        filepath = os.path.join(output_dir, filename)
        if not check_file_exists(filepath, description):
            all_passed = False
    
    # 检查终稿验证结果
    report_path = os.path.join(output_dir, "final_integrity_check_report.json")
    if os.path.exists(report_path):
        valid, data = check_json_file(report_path, "终稿验证报告")
        if valid and data:
            status = data.get("status", "unknown")
            if status == "passed":
                print_success("终稿验证：通过 ✓")
            else:
                print_error(f"终稿验证：{status}（不建议投稿）")
    
    return all_passed

def validate_stage_7(output_dir):
    """验证阶段 7 产出"""
    print(f"\n{Colors.BOLD}阶段 7: Journal Format Output（期刊格式输出）{Colors.ENDC}")
    
    checks = {
        "submission_main.docx": "主文档",
        "submission_cover_letter.docx": "封面信",
        "submission_checklist.pdf": "投稿检查清单"
    }
    
    all_passed = True
    for filename, description in checks.items():
        filepath = os.path.join(output_dir, filename)
        if not check_file_exists(filepath, description):
            all_passed = False
    
    return all_passed

def generate_summary(output_dir, results):
    """生成验证总结"""
    print_header("验证总结")
    
    total_stages = len(results)
    passed_stages = sum(1 for r in results.values() if r)
    
    print(f"总阶段数：{total_stages}")
    print(f"通过阶段：{passed_stages}")
    print(f"未通过阶段：{total_stages - passed_stages}")
    
    if passed_stages == total_stages:
        print_success("\n🎉 所有阶段验证通过！可以准备投稿。")
    else:
        print_warning("\n⚠️ 部分阶段未通过，请检查并修复问题。")
    
    # 生成总结报告
    summary_path = os.path.join(output_dir, "validation_summary.json")
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_stages": total_stages,
        "passed_stages": passed_stages,
        "results": results
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print_success(f"验证总结已保存：{summary_path}")

def main():
    if len(sys.argv) < 2:
        print("用法：python workflow_validator.py [输出目录]")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    
    if not os.path.exists(output_dir):
        print_error(f"输出目录不存在：{output_dir}")
        sys.exit(1)
    
    print_header("学术论文写作工作流验证器 v1.0")
    print_info(f"验证目录：{output_dir}")
    
    results = {}
    
    # 验证各阶段
    results["stage1"] = validate_stage_1(output_dir)
    results["stage2"] = validate_stage_2(output_dir)
    results["stage3"] = validate_stage_3(output_dir)
    results["stage4"] = validate_stage_4(output_dir)
    results["stage5"] = validate_stage_5(output_dir)
    results["stage6"] = validate_stage_6(output_dir)
    results["stage7"] = validate_stage_7(output_dir)
    
    # 生成总结
    generate_summary(output_dir, results)

if __name__ == "__main__":
    main()
