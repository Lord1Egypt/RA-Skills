#!/usr/bin/env python3
"""
模拟面试题生成器（本地规则，针对校招/实习 · 互联网产品经理）。

基于目标 JD + 候选人（优化后）简历，生成覆盖 7 大类的模拟面试问题：
  一、自我介绍与产品认知
  二、需求分析与产品设计
  三、数据思维与数据分析
  四、项目与实习经历深挖（基于简历动态生成）
  五、行为面试（STAR）
  六、开放设计题
  七、反问环节

题目 = 产品经理题库模板（config/interview_templates.json）+ JD 定制填充 + 简历项目深挖。
"""

import json
import os
import re

from evaluator import analyze_jd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "config", "interview_templates.json")


def load_templates() -> dict:
    """加载面试题库模板配置。"""
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _jd_context(jd_text: str, jd_analysis: dict) -> dict:
    """从 JD 提取用于题目定制的上下文。"""
    industry = (jd_analysis.get("industry_hints") or [])
    # 目标用户：JD 中"面向/针对/服务"后置词
    audience = ""
    m = re.search(r"(面向|针对|服务|服务于|目标用户|用户群体)[\s:：]*([\u4e00-\u9fa5A-Za-z0-9]{2,12})", jd_text)
    if m:
        audience = m.group(2)
    return {
        "jd_industry": industry[0] if industry else "互联网",
        "jd_company": "该企业",
        "jd_audience": audience or "目标用户",
        "jd_position": "产品经理（校招/实习）",
    }


def _project_questions(structured: dict) -> list:
    """针对简历中的每个实习/项目生成深挖问题。"""
    questions = []
    entries = []
    for w in (structured.get("work_experience") or []):
        company = w.get("company") or "这段实习"
        period = w.get("period") or ""
        entries.append((f"{company} {period}".strip(), w))
    for p in (structured.get("projects") or []):
        name = p.get("name") or p.get("company") or "这个项目"
        entries.append((f"{name}".strip(), p))

    for title, item in entries[:4]:
        questions.append(f"- **问题**：请详细介绍【{title}】这段经历：你在其中担任什么角色、负责什么、最终产出是什么？")
        questions.append("- 考察要点：核实经历真实性、个人贡献边界、是否有完整思考")
        questions.append(f"- **问题**：在【{title}】中，你遇到的最大困难是什么？具体怎么解决的？")
        questions.append("- 考察要点：解决问题能力、复盘能力、抗压能力")
        achievements = item.get("achievements") or []
        has_number = any(re.search(r"\d", a) for a in achievements) or any(
            re.search(r"\d", r) for r in (item.get("responsibilities") or [])
        )
        if has_number:
            questions.append(f"- **问题**：在【{title}】中提到的数据（如量化成果）具体是怎么计算/统计的？口径是什么？")
            questions.append("- 考察要点：数据真实性、对数据的理解深度")
        else:
            questions.append(f"- **问题**：【{title}】的最终效果如何衡量？如果当时有数据，大概是什么量级？")
            questions.append("- 考察要点：数据意识、结果导向")
    return questions


def generate_interview_questions(
    optimized_resume: str,
    jd_text: str,
    structured: dict,
) -> str:
    """生成模拟面试问题 Markdown。"""
    tpl = load_templates()
    jd_analysis = analyze_jd(jd_text)
    ctx = _jd_context(jd_text, jd_analysis)
    categories = tpl.get("categories", [])

    blocks = []
    for cat in categories:
        name = cat["name"]
        blocks.append(f"## {name}")
        blocks.append("")
        templates = cat.get("templates", [])
        if cat.get("dynamic"):
            # 动态分类：基于简历项目深挖
            proj_qs = _project_questions(structured)
            if not proj_qs:
                blocks.append("- **问题**：请介绍一段你最值得讲的产品/项目经历，说明你的角色与产出。")
                blocks.append("- 考察要点：经历真实性、个人贡献、思考深度")
            else:
                for q in proj_qs:
                    blocks.append(q)
        else:
            for i, t in enumerate(templates[: cat.get("count", 5)], 1):
                q = t.format(**ctx)
                blocks.append(f"- **问题**：{q}")
                blocks.append(f"- 考察要点：{_ka_for(cat['id'], q)}")
        blocks.append("")

    # 附录：JD 高频要求提醒
    kws = jd_analysis.get("skill_keywords") or []
    if kws:
        blocks.append("## 附：JD 高频考察点")
        blocks.append("")
        blocks.append(f"> 面试官大概率围绕这些能力提问，请提前准备案例：**{', '.join(kws[:8])}**")
        blocks.append("")

    return "\n".join(blocks)


def _ka_for(cat_id: str, question: str) -> str:
    """为模板问题补充考察要点（本地规则）。"""
    ka_map = {
        "self_intro": "表达能力、产品热情、自我认知与岗位匹配度",
        "requirement_analysis": "需求判断、优先级思维、流程完整性、场景化思考",
        "data_analysis": "数据思维、指标理解、分析框架与实验方法",
        "behavioral_star": "行为深度、复盘能力、团队协作与抗压能力",
        "case_design": "结构化思维、估算能力、产品 sense 与可行性",
        "reverse_qa": "求职动机、对岗位/团队的理解与主动性",
    }
    return ka_map.get(cat_id, "与产品经理岗位胜任力相关")
