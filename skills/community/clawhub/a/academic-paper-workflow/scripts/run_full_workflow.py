#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
学术论文写作工作流自动化执行脚本

用法：
    python run_full_workflow.py [研究主题] --journal [期刊名称] --depth [exhaustive|overview]

示例：
    python run_full_workflow.py "无人机智能目标识别技术" --journal "IEEE Transactions" --depth exhaustive
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_stage(stage_num, stage_name):
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}>>> 阶段 {stage_num}: {stage_name}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def save_checkpoint(stage, data, output_dir):
    """保存阶段检查点"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"checkpoint_stage{stage}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print_success(f"阶段 {stage} 检查点已保存：{filename}")
    return filepath

def load_checkpoint(stage, output_dir):
    """加载阶段检查点"""
    checkpoints = list(Path(output_dir).glob(f"checkpoint_stage{stage}_*.json"))
    if not checkpoints:
        return None
    
    latest = sorted(checkpoints)[-1]
    with open(latest, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_stage_1_research(topic, depth="exhaustive"):
    """阶段 1: 深度研究"""
    print_stage(1, "Research（深度研究）")
    
    print_info(f"研究主题：{topic}")
    print_info(f"研究深度：{depth}")
    
    # 提示用户启动技能
    print("\n请执行以下命令：")
    print(f"{Colors.BOLD}/academic-deep-research {topic}{Colors.ENDC}")
    
    print("\n技能会询问 3 个澄清问题，请回答：")
    print("1. 应用场景（军事/民用/混合）")
    print("2. 研究深度（概述/exhaustive）")
    print("3. 时间/地域/来源偏好")
    
    print("\n然后技能会生成研究计划，请审批：")
    print("- 检查 6 个主题是否覆盖完整")
    print("- 确认关键问题是否准确")
    print("- 批准或调整")
    
    print("\n审批后，技能会自动执行 2 轮研究（每主题）：")
    print("- 第 1 轮：全景扫描（≥20 条结果）")
    print("- 第 2 轮：深度挖掘（针对缺口）")
    
    print("\n完成后，保存输出到文件：")
    print("- research_report.md（研究报告）")
    print("- literature_search_results.json（文献搜索结果）")
    
    # 等待用户确认
    input(f"\n{Colors.WARNING}阶段 1 完成后，按回车继续...{Colors.ENDC}")
    
    return {
        "stage": 1,
        "topic": topic,
        "depth": depth,
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }

def run_stage_2_write(research_report_path):
    """阶段 2: 学术写作"""
    print_stage(2, "Write（学术写作）")
    
    print_info(f"研究报告：{research_report_path}")
    
    print("\n请执行以下命令：")
    print(f"{Colors.BOLD}/academic-writer 基于以下研究报告，撰写一篇 SCI 论文格式的文献综述{Colors.ENDC}")
    print("[粘贴研究报告内容]")
    
    print("\n技能会询问：")
    print("1. 论文类型（综述/实验/方法论）")
    print("2. 目标期刊")
    print("3. 章节要求")
    print("4. 图表数量")
    print("5. 参考文献目标数量")
    
    print("\n完成后，保存输出到文件：")
    print("- paper_draft.md（论文初稿）")
    print("- references_raw.txt（参考文献列表）")
    
    input(f"\n{Colors.WARNING}阶段 2 完成后，按回车继续...{Colors.ENDC}")
    
    return {
        "stage": 2,
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }

def run_stage_3_citation(references_path, format="APA 7th"):
    """阶段 3: 引用格式化"""
    print_stage(3, "Citation（引用格式化）")
    
    print_info(f"参考文献：{references_path}")
    print_info(f"目标格式：{format}")
    
    print("\n请执行以下命令：")
    print(f"{Colors.BOLD}/academic-citation 将参考文献转换为 {format} 格式{Colors.ENDC}")
    print("[粘贴参考文献列表]")
    
    print("\n技能会：")
    print("1. DOI 导入，自动补全元数据")
    print("2. 格式验证（作者、期刊、卷期、页码、DOI）")
    print("3. 批量格式化（90+ 篇）")
    
    print("\n完成后，保存输出到文件：")
    print("- references_formatted.txt（格式化后的参考文献）")
    print("- citation_validation_report.json（格式验证报告）")
    
    input(f"\n{Colors.WARNING}阶段 3 完成后，按回车继续...{Colors.ENDC}")
    
    return {
        "stage": 3,
        "format": format,
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }

def run_stage_4_integrity_check(draft_path):
    """阶段 4: 初稿诚信检查"""
    print_stage(4, "Integrity Check（初稿诚信检查）")
    
    print_info(f"论文初稿：{draft_path}")
    
    print("\n请执行以下命令：")
    print(f"{Colors.BOLD}/academic-integrity-checker [论文初稿内容]{Colors.ENDC}")
    
    print("\n技能会检测：")
    print("1. AI 幻觉（无事实依据的声称）")
    print("2. 虚假引用（不存在的文献）")
    print("3. 伪造内容（捏造的数据、结论）")
    print("4. 引用不匹配（引用与内容不符）")
    
    print("\n检查报告格式：")
    print("✅ 验证通过：X 条引用")
    print("⚠️ 需要核实：Y 条引用")
    print("❌ 发现错误：Z 条引用")
    
    print("\n⚠️ 重要：必须人工修复所有❌错误和⚠️模糊引用")
    
    print("\n完成后，保存输出到文件：")
    print("- integrity_check_report_stage4.json（检查报告）")
    print("- paper_draft_revised.md（修复后的初稿）")
    
    input(f"\n{Colors.WARNING}阶段 4 完成后，按回车继续...{Colors.ENDC}")
    
    return {
        "stage": 4,
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }

def run_stage_5_review(draft_path, max_rounds=3):
    """阶段 5: 多轮评审"""
    print_stage(5, "Review → Revise → Re-Review（多轮评审）")
    
    print_info(f"论文稿：{draft_path}")
    print_info(f"最大轮数：{max_rounds}")
    
    for round_num in range(1, max_rounds + 1):
        print(f"\n{Colors.BOLD}--- 第 {round_num} 轮评审 ---{Colors.ENDC}\n")
        
        print("请执行以下命令：")
        print(f"{Colors.BOLD}/review-revisor [论文稿内容]{Colors.ENDC}")
        
        print("\n技能会进行 5 视角评审：")
        print("1. 方法论专家（搜索策略、PRISMA、方法描述）")
        print("2. 领域专家（技术进展、对比分析）")
        print("3. 统计专家（指标、测试集、置信区间）")
        print("4. 写作专家（摘要、语言、逻辑）")
        print("5. 伦理专家（数据来源、隐私、利益冲突）")
        
        if round_num == 1:
            print("\n预计返回 15-20 条评审意见")
        elif round_num == 2:
            print("\n预计返回 3-5 条小意见")
        else:
            print("\n目标：0 评审意见")
        
        print("\n然后执行自动润色：")
        print(f"{Colors.BOLD}/academic-writer 基于以下评审意见修改论文：[粘贴评审意见]{Colors.ENDC}")
        
        if round_num < max_rounds:
            cont = input(f"\n{Colors.WARNING}第 {round_num} 轮完成后，是否继续下一轮？(y/n): {Colors.ENDC}")
            if cont.lower() != 'y':
                break
    
    print("\n完成后，保存输出到文件：")
    print("- review_reports_round{1,2,3}.json（各轮评审报告）")
    print("- paper_final.md（最终稿）")
    
    input(f"\n{Colors.WARNING}阶段 5 完成后，按回车继续...{Colors.ENDC}")
    
    return {
        "stage": 5,
        "rounds_completed": max_rounds,
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }

def run_stage_6_final_check(final_draft_path):
    """阶段 6: 终稿验证"""
    print_stage(6, "Final Integrity Check（终稿验证）")
    
    print_info(f"最终稿：{final_draft_path}")
    
    print("\n请执行以下命令：")
    print(f"{Colors.BOLD}/final-integrity-check [最终稿内容]{Colors.ENDC}")
    
    print("\n技能会验证：")
    print("✅ 所有引用是否均可追溯")
    print("✅ 数据是否与来源一致")
    print("✅ 图表是否都有正确标注")
    print("✅ 利益冲突声明是否完整")
    print("✅ 数据集来源声明是否规范")
    print("✅ 是否符合目标期刊基本要求")
    
    print("\n目标：所有验证项目通过")
    
    print("\n完成后，保存输出到文件：")
    print("- final_integrity_check_report.json（验证报告）")
    
    input(f"\n{Colors.WARNING}阶段 6 完成后，按回车继续...{Colors.ENDC}")
    
    return {
        "stage": 6,
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }

def run_stage_7_format_output(final_draft_path, journal):
    """阶段 7: 期刊格式输出"""
    print_stage(7, "Journal Format Output（期刊格式输出）")
    
    print_info(f"最终稿：{final_draft_path}")
    print_info(f"目标期刊：{journal}")
    
    print("\n请执行以下命令：")
    print(f"{Colors.BOLD}/journal-format-output [最终稿内容] --journal \"{journal}\"{Colors.ENDC}")
    
    print("\n技能会：")
    print("1. 加载期刊模板（Word/LaTeX）")
    print("2. 转换文档格式（字体、字号、行距、页边距）")
    print("3. 调整参考文献（按期刊要求重新格式化）")
    print("4. 重排图表位置（符合期刊规范）")
    print("5. 生成投稿文件（主文档、补充材料、封面信）")
    
    print("\n完成后，保存输出到文件：")
    print("- submission_main.docx（主文档）")
    print("- submission_supplementary.pdf（补充材料）")
    print("- submission_cover_letter.docx（封面信）")
    print("- submission_checklist.pdf（投稿检查清单）")
    
    input(f"\n{Colors.WARNING}阶段 7 完成后，按回车继续...{Colors.ENDC}")
    
    return {
        "stage": 7,
        "journal": journal,
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }

def main():
    parser = argparse.ArgumentParser(description="学术论文写作工作流自动化执行")
    parser.add_argument("topic", help="研究主题")
    parser.add_argument("--journal", default="IEEE Transactions", help="目标期刊")
    parser.add_argument("--depth", choices=["exhaustive", "overview"], default="exhaustive", help="研究深度")
    parser.add_argument("--output-dir", default="./workflow_output", help="输出目录")
    parser.add_argument("--resume-from", type=int, help="从指定阶段恢复")
    
    args = parser.parse_args()
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 打印工作流信息
    print_header("学术论文写作工作流 v1.0")
    print_info(f"研究主题：{args.topic}")
    print_info(f"目标期刊：{args.journal}")
    print_info(f"研究深度：{args.depth}")
    print_info(f"输出目录：{args.output_dir}")
    
    # 工作流执行
    checkpoints = {}
    
    try:
        # 阶段 1: 深度研究
        if not args.resume_from or args.resume_from <= 1:
            checkpoints["stage1"] = run_stage_1_research(args.topic, args.depth)
            save_checkpoint(1, checkpoints["stage1"], args.output_dir)
        
        # 阶段 2: 学术写作
        if not args.resume_from or args.resume_from <= 2:
            checkpoints["stage2"] = run_stage_2_write(os.path.join(args.output_dir, "research_report.md"))
            save_checkpoint(2, checkpoints["stage2"], args.output_dir)
        
        # 阶段 3: 引用格式化
        if not args.resume_from or args.resume_from <= 3:
            checkpoints["stage3"] = run_stage_3_citation(os.path.join(args.output_dir, "references_raw.txt"))
            save_checkpoint(3, checkpoints["stage3"], args.output_dir)
        
        # 阶段 4: 初稿诚信检查
        if not args.resume_from or args.resume_from <= 4:
            checkpoints["stage4"] = run_stage_4_integrity_check(os.path.join(args.output_dir, "paper_draft.md"))
            save_checkpoint(4, checkpoints["stage4"], args.output_dir)
        
        # 阶段 5: 多轮评审
        if not args.resume_from or args.resume_from <= 5:
            checkpoints["stage5"] = run_stage_5_review(os.path.join(args.output_dir, "paper_draft_revised.md"))
            save_checkpoint(5, checkpoints["stage5"], args.output_dir)
        
        # 阶段 6: 终稿验证
        if not args.resume_from or args.resume_from <= 6:
            checkpoints["stage6"] = run_stage_6_final_check(os.path.join(args.output_dir, "paper_final.md"))
            save_checkpoint(6, checkpoints["stage6"], args.output_dir)
        
        # 阶段 7: 期刊格式输出
        if not args.resume_from or args.resume_from <= 7:
            checkpoints["stage7"] = run_stage_7_format_output(os.path.join(args.output_dir, "paper_final.md"), args.journal)
            save_checkpoint(7, checkpoints["stage7"], args.output_dir)
        
        # 完成
        print_header("工作流执行完成！")
        print_success("所有阶段已完成")
        print_info(f"输出目录：{args.output_dir}")
        print("\n投稿前最终检查：")
        print("1. 人工检查所有文件")
        print("2. 确认格式符合期刊要求")
        print("3. 确认所有声明文件齐全")
        print("4. 准备投稿")
        
    except KeyboardInterrupt:
        print_error("\n工作流中断")
        print_info("可以使用 --resume-from 参数从指定阶段恢复")
        sys.exit(1)

if __name__ == "__main__":
    main()
