#!/usr/bin/env python3
"""
generate_doc.py — HR 文档生成脚本

功能：根据文档类型和参数，生成标准格式的 HR/行政文档（Markdown格式）
用法：
  python3 generate_doc.py --type <doc_type> --output <filename> [--params key=value ...]

支持的文档类型（--type 参数）：
  notice          全员通知
  holiday         放假通知
  meeting         会议纪要
  weekly          部门周报
  pip             绩效改进计划（PIP）
  offboarding     离职确认函
  policy          制度文件框架
  requirement     需求分析报告
"""

import argparse
import json
import os
from datetime import datetime


def get_current_date():
    return datetime.now().strftime("%Y年%m月%d日")


TEMPLATES = {
    "notice": """# 关于{subject}的通知

各部门、全体员工：

{purpose}

## 一、主要内容

{main_content}

## 二、执行要求

{requirements}

## 三、联系方式

如有疑问，请联系{contact}。

特此通知。

{department}  
{date}
""",

    "holiday": """# {holiday}放假通知

全体员工：

根据国家法定节假日安排，结合公司实际情况，现将{holiday}放假安排通知如下：

## 一、放假时间

{start_date} 至 {end_date}，共 {days} 天。

## 二、调休安排

{makeup_work}

## 三、值班安排

放假期间，{duty_dept}安排专人值班，联系方式：{duty_contact}。

## 四、温馨提示

- 请各部门在放假前做好工作交接
- {tips}

祝大家节日快乐！

{company_name} 行政部  
{date}
""",

    "meeting": """# 会议纪要

| 项目 | 内容 |
|------|------|
| 会议名称 | {meeting_name} |
| 会议时间 | {meeting_time} |
| 会议地点 | {location} |
| 主持人 | {host} |
| 参会人员 | {attendees} |
| 记录人 | {recorder} |

---

## 一、会议议题

{agenda}

---

## 二、讨论记录

{discussion}

---

## 三、行动项（Action Items）

| 编号 | 行动事项 | 责任人 | 完成时间 | 状态 |
|-----|---------|--------|---------|------|
{action_items}

---

## 四、下次会议

时间：{next_meeting}

---
*本纪要由{recorder}整理，如有异议请在24小时内反馈。*
""",

    "pip": """# 绩效改进计划（PIP）

| 项目 | 内容 |
|------|------|
| 员工姓名 | {employee_name} |
| 岗位 | {position} |
| 直属上级 | {manager} |
| 启动日期 | {start_date} |
| 改进周期 | {duration}（{start_date} 至 {end_date}） |

---

## 一、改进背景

{background}

> 注：以上内容基于具体事实，请避免主观评价。

---

## 二、改进目标

| 改进维度 | 具体指标 | 衡量标准 | 完成时间 |
|---------|---------|---------|---------|
{improvement_goals}

---

## 三、公司支持措施

{support_measures}

---

## 四、检查节点

{check_points}

---

## 五、后果说明

若PIP期结束后仍未达到改进目标，公司将依据劳动合同及相关法律规定，对岗位安排作出调整。

---

## 六、签字确认

> 员工确认（签字代表收到并了解本计划，不代表同意全部内容）

| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| 员工 | {employee_name} | ________ | ________ |
| 直属上级 | {manager} | ________ | ________ |
| HR 见证 | ________ | ________ | ________ |
""",

    "requirement": """# 需求分析报告

| 项目 | 内容 |
|------|------|
| 需求名称 | {requirement_name} |
| 提出人 | {requester} |
| 分析人 | {analyst} |
| 日期 | {date} |

---

## 一、需求背景与现状

{background}

---

## 二、核心问题定义

> {problem_statement}

---

## 三、目标与预期成果

- **短期目标**（1-3个月）：{short_term_goal}
- **中期目标**（3-6个月）：{mid_term_goal}
- **成功标准**：{success_criteria}

---

## 四、方案选项

### 方案A：{option_a_name}

- 核心思路：{option_a_idea}
- 优点：{option_a_pros}
- 缺点/风险：{option_a_cons}
- 所需资源：{option_a_resources}

### 方案B：{option_b_name}

- 核心思路：{option_b_idea}
- 优点：{option_b_pros}
- 缺点/风险：{option_b_cons}
- 所需资源：{option_b_resources}

---

## 五、推荐方案

**推荐：{recommended_option}**

理由：{recommendation_reason}

---

## 六、实施路径

| 阶段 | 关键任务 | 负责人 | 时间节点 |
|------|---------|--------|---------|
{implementation_plan}

---

## 七、风险与应对

| 风险 | 发生概率 | 影响程度 | 应对策略 |
|------|---------|---------|---------|
{risks}

---

## 八、资源需求

{resources}
""",
}


def generate_document(doc_type: str, params: dict, output_file: str = None):
    """生成文档并输出"""
    if doc_type not in TEMPLATES:
        print(f"❌ 不支持的文档类型: {doc_type}")
        print(f"   支持的类型: {', '.join(TEMPLATES.keys())}")
        return False

    # 自动填充日期
    if "date" not in params:
        params["date"] = get_current_date()

    template = TEMPLATES[doc_type]
    
    try:
        # 替换模板中的占位符
        doc_content = template.format_map(params)
    except KeyError as e:
        # 若参数不足，标记缺失字段
        missing_key = str(e).strip("'")
        print(f"⚠️  缺少参数: {missing_key}，使用占位符替代")
        params[missing_key] = f"[请填写：{missing_key}]"
        doc_content = template.format_map(params)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(doc_content)
        print(f"✅ 文档已生成：{output_file}")
    else:
        print(doc_content)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="HR 文档生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--type", required=True, help="文档类型")
    parser.add_argument("--output", help="输出文件路径（不填则打印到控制台）")
    parser.add_argument("--params", nargs="*", help="文档参数，格式：key=value")
    parser.add_argument("--list", action="store_true", help="列出所有支持的文档类型")

    args = parser.parse_args()

    if args.list:
        print("支持的文档类型：")
        for t in TEMPLATES.keys():
            print(f"  - {t}")
        return

    # 解析参数
    params = {}
    if args.params:
        for param in args.params:
            if "=" in param:
                key, value = param.split("=", 1)
                params[key.strip()] = value.strip()

    generate_document(args.type, params, args.output)


if __name__ == "__main__":
    main()
