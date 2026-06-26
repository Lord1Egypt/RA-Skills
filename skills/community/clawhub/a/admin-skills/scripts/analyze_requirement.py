#!/usr/bin/env python3
"""
analyze_requirement.py — 后方业务需求智能解析脚本

功能：对用户输入的自然语言业务需求，进行结构化拆解，输出5W1H需求分析框架
用法：
  python3 analyze_requirement.py --input "需求描述文字"
  python3 analyze_requirement.py --file requirement.txt
  python3 analyze_requirement.py --interactive

说明：
  本脚本通过规则匹配，对需求进行初步分类和结构化。
  AI 应读取本脚本的分类规则，辅助需求解析判断。
"""

import argparse
import sys
import re
from datetime import datetime

# ─────────────────────────────────────────
# 需求分类规则
# ─────────────────────────────────────────

DOMAIN_KEYWORDS = {
    "招聘": ["招聘", "简历", "面试", "JD", "岗位发布", "HC", "headcount", "offer", "候选人", "人才"],
    "入职/离职": ["入职", "离职", "辞职", "辞退", "转正", "交接", "离职证明"],
    "绩效": ["绩效", "KPI", "OKR", "考核", "PIP", "晋升", "调薪", "末位"],
    "薪酬福利": ["薪酬", "工资", "社保", "公积金", "年终奖", "福利", "津贴", "调薪"],
    "考勤假期": ["考勤", "打卡", "请假", "年假", "病假", "调休", "迟到", "早退"],
    "制度建设": ["制度", "规章", "政策", "规定", "手册", "办法", "条例", "合规"],
    "行政管理": ["行政", "采购", "报销", "资产", "办公室", "供应商", "装修", "差旅"],
    "组织发展": ["组织架构", "部门", "岗位设计", "编制", "人员规划", "人效"],
    "员工关系": ["劳动合同", "员工关系", "仲裁", "纠纷", "投诉", "竞业"],
    "培训发展": ["培训", "学习", "发展", "课程", "认证", "能力提升"],
    "报告汇报": ["报告", "周报", "月报", "述职", "汇报", "总结", "复盘"],
    "文档生成": ["写一个", "起草", "生成", "制定", "帮我写", "模板"],
}

DELIVERABLE_KEYWORDS = {
    "制度文件": ["制度", "规定", "规范", "办法", "政策", "手册"],
    "流程设计": ["流程", "步骤", "节点", "审批", "SOP"],
    "通知公告": ["通知", "公告", "告知", "发布"],
    "合同文书": ["合同", "协议", "协议书", "承诺书"],
    "审批表单": ["表单", "申请表", "审批单", "登记表"],
    "分析报告": ["分析", "报告", "研究", "评估"],
    "汇报材料": ["汇报", "PPT", "述职", "年终"],
    "会议纪要": ["会议纪要", "纪要", "会议记录"],
    "方案计划": ["方案", "计划", "规划", "路线图"],
}

URGENCY_KEYWORDS = {
    "紧急": ["紧急", "急需", "今天", "明天", "马上", "立即", "ASAP", "尽快"],
    "正常": ["下周", "本月", "近期", "这周"],
    "长期": ["下个季度", "年底", "长期", "规划"],
}


def classify_domain(text: str) -> list:
    """识别业务域"""
    matched = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            matched.append(domain)
    return matched if matched else ["未分类"]


def classify_deliverable(text: str) -> str:
    """识别交付物类型"""
    for deliverable, keywords in DELIVERABLE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return deliverable
    return "待确认"


def classify_urgency(text: str) -> str:
    """识别紧急程度"""
    for urgency, keywords in URGENCY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return urgency
    return "正常"


def extract_key_info(text: str) -> dict:
    """提取关键信息"""
    result = {
        "原始需求": text,
        "业务域": classify_domain(text),
        "交付物类型": classify_deliverable(text),
        "紧急程度": classify_urgency(text),
        "分析时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    return result


def generate_questions(analysis: dict) -> list:
    """根据分析结果，生成需要向用户确认的问题"""
    questions = []
    
    domains = analysis["业务域"]
    deliverable = analysis["交付物类型"]
    
    # 通用问题
    questions.append("适用对象是全体员工、特定部门，还是管理层？")
    questions.append("公司目前规模大概是多少人？（帮助确定制度复杂度）")
    
    # 交付物相关问题
    if deliverable == "制度文件":
        questions.append("是否已有现行制度需要修订？还是全新制定？")
        questions.append("期望的格式：正式制度文本、简洁版说明，还是两者都要？")
    elif deliverable == "流程设计":
        questions.append("目前这个流程是否已有初步版本，还是从零开始设计？")
        questions.append("流程中涉及哪些角色/部门需要参与？")
    elif deliverable == "分析报告":
        questions.append("报告的最终受众是谁？（CEO/HR团队/董事会）")
        questions.append("是否有特定的数据或现状信息需要纳入分析？")
    elif deliverable == "合同文书":
        questions.append("是否需要法律审查？（建议涉及合同的文件都由律师复核）")
        questions.append("适用地区是哪里？（劳动法规存在地区差异）")
    
    # 域相关问题
    if "绩效" in domains:
        questions.append("公司目前使用的是 KPI、OKR 还是其他绩效体系？")
    if "薪酬福利" in domains:
        questions.append("是否涉及具体薪酬数字，还是只需要制度框架？")
    if "制度建设" in domains:
        questions.append("新制度是否需要经过员工公示或代表大会讨论流程？")
    
    return questions[:5]  # 最多返回5个问题，避免让用户感到繁琐


def format_analysis_output(analysis: dict, questions: list) -> str:
    """格式化输出"""
    output = []
    output.append("=" * 50)
    output.append("📋 需求解析结果")
    output.append("=" * 50)
    output.append(f"\n原始需求：{analysis['原始需求'][:100]}...")
    output.append(f"\n🏷️  识别业务域：{' / '.join(analysis['业务域'])}")
    output.append(f"📄  交付物类型：{analysis['交付物类型']}")
    output.append(f"⏰  紧急程度：{analysis['紧急程度']}")
    output.append(f"\n{'─' * 40}")
    output.append("❓ 建议确认以下信息（可跳过，AI 将基于通用假设生成）：")
    for i, q in enumerate(questions, 1):
        output.append(f"  {i}. {q}")
    output.append("\n" + "=" * 50)
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="后方业务需求结构化解析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--input", help="需求描述文字")
    parser.add_argument("--file", help="从文件读取需求描述")
    parser.add_argument("--interactive", action="store_true", help="交互模式")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出")

    args = parser.parse_args()

    # 获取输入
    if args.input:
        text = args.input
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.interactive:
        print("请输入您的业务需求（输入完毕后按两次回车）：")
        lines = []
        while True:
            line = input()
            if line == "":
                if lines:
                    break
            else:
                lines.append(line)
        text = "\n".join(lines)
    else:
        print("请通过 --input、--file 或 --interactive 提供需求描述")
        parser.print_help()
        sys.exit(1)

    # 分析
    analysis = extract_key_info(text)
    questions = generate_questions(analysis)

    # 输出
    if args.json:
        import json
        result = {**analysis, "建议确认问题": questions}
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_analysis_output(analysis, questions))


if __name__ == "__main__":
    main()
