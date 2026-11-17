#!/usr/bin/env python3
"""
简历本地结构化解析（无 LLM，纯规则）。

将 OCR 提取的简历文本（或直接粘贴的文本）通过正则规则解析为结构化 JSON
（基本信息 / 教育经历 / 实习经历 / 项目经历 / 技能）。
结构化结果用于评分规则引擎中的模块完整性、经历数量等检查；
主要评分仍基于全文文本（更鲁棒）。

结构化 schema 与旧版 LLM 解析保持一致，方便下游模块复用。
"""

import re

from rule_engine import strip_meta_text

# 电话：支持 1[3-9]\d{9} 或带分隔符形式
PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d[\s\-]?\d{4}[\s\-]?\d{4}(?!\d)")
# 邮箱
EMAIL_RE = re.compile(r"[\w.\-+]+@[\w\-]+(\.[\w\-]+)+")
# 时间范围：2023.06-2024.08 / 2023年6月 - 2024年8月 / 2023/06 ~ 至今
_PERIOD_SEP = r"(?:\s*(?:-|—|–|~|至|到)\s*)"
PERIOD_RE = re.compile(
    r"(20\d{2}[./年]\s*\d{0,2}[月/]?"
    + _PERIOD_SEP
    + r"(?:20\d{2}[./年]\s*\d{0,2}[月/]?|至今|现在|present|Present))"
)
# 学历词
DEGREE_RE = re.compile(r"(本科|硕士|博士|研究生|大专|MBA|EMBA|学士)")
# 学校词
SCHOOL_RE = re.compile(r"[\u4e00-\u9fa5A-Za-z0-9（）()·]{2,}(?:大学|学院|学校|院校)")
# 教育段落触发词
EDU_TRIGGER = re.compile(r"(教育经历|教育背景|学历|学校|专业)")
# 实习/工作段落触发词
WORK_TRIGGER = re.compile(r"(实习经历|工作经历|实习|工作经验|工作履历)")
# 项目段落触发词
PROJECT_TRIGGER = re.compile(r"(项目经历|项目经验|项目|在校项目)")
# 技能段落触发词
SKILL_TRIGGER = re.compile(r"(专业技能|技能特长|技能|特长|个人技能)")


def _strip_brace(match_obj) -> str:
    return match_obj.group(0).strip("（）() ")


def parse_resume(resume_text: str) -> dict:
    """
    将简历原文解析为结构化 dict。
    - basic_info: name/phone/email/location/target_position/years_of_experience
    - education: [{school, degree, major, period, details}]
    - work_experience: [{company, title, period, duration, responsibilities, achievements}]
    - projects: [{name, role, period, description, highlights}]
    - skills: {technical, soft, language}
    """
    # 解析前剥离优化稿/报告中的元信息（摘要、诊断、头部声明、量化标注），
    # 避免其干扰姓名/联系方式/教育/经历等字段识别。
    text = strip_meta_text(resume_text or "")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    basic_info = {
        "name": "",
        "phone": "",
        "email": "",
        "location": "",
        "target_position": "",
        "years_of_experience": 0,
    }
    # 联系方式
    phone_m = PHONE_RE.search(text)
    if phone_m:
        basic_info["phone"] = re.sub(r"\s|-", "", phone_m.group(0))
    email_m = EMAIL_RE.search(text)
    if email_m:
        basic_info["email"] = email_m.group(0)
    # 名字：首行（若长度 2-4 且非段落标题）
    for ln in lines[:3]:
        candidate = ln.strip("：:。 \t")
        if 1 < len(candidate) <= 4 and not re.search(r"[\d@]", candidate) and candidate not in (
            "个人简历", "简历", "基本信息", "联系方式"
        ):
            basic_info["name"] = candidate
            break

    # ---- 段落切分：按触发词找各模块的行范围 ----
    sections = {"education": [], "work": [], "project": [], "skill": []}
    current = None
    order = []
    for ln in lines:
        if WORK_TRIGGER.search(ln) and len(ln) <= 12:
            current = "work"
            order.append("work")
        elif PROJECT_TRIGGER.search(ln) and len(ln) <= 12:
            current = "project"
            order.append("project")
        elif EDU_TRIGGER.search(ln) and len(ln) <= 12 and "教育" in ln or (
            EDU_TRIGGER.search(ln) and len(ln) <= 6
        ):
            current = "education"
            order.append("education")
        elif SKILL_TRIGGER.search(ln) and len(ln) <= 12:
            current = "skill"
            order.append("skill")
        elif re.match(r"^[\u4e00-\u9fa5A-Za-z0-9 \u3001，、（）()/·\-]{2,20}$", ln) and len(ln) <= 20:
            # 可能为新模块标题
            continue
        if current and ln:
            sections[current].append(ln)

    # ---- 教育经历 ----
    education = []
    edu_lines = sections["education"]
    if edu_lines:
        period = ""
        school = ""
        degree = ""
        major = ""
        details = []
        for ln in edu_lines:
            pm = PERIOD_RE.search(ln)
            if pm:
                period = pm.group(0)
            sm = SCHOOL_RE.search(ln)
            if sm:
                school = _strip_brace(sm)
            dm = DEGREE_RE.search(ln)
            if dm:
                degree = dm.group(1)
            # 专业：优先"xx专业"；其次去除学校/学历/时间后剩余的中文串
            major_m = re.search(r"([\u4e00-\u9fa5A-Za-z]{2,14})(?:专业)", ln)
            if major_m:
                major = major_m.group(1)
            elif not major:
                rest = ln
                if pm:
                    rest = rest.replace(pm.group(0), "")
                if sm:
                    rest = rest.replace(sm.group(0), "").replace("（", "").replace("）", "")
                if dm:
                    rest = rest.replace(dm.group(0), "")
                rest = re.sub(r"[\s:：,，、()（）|/\\\-—–~0-9.]+", "", rest)
                rest = re.sub(r"^(学历|教育经历|教育背景|学校)", "", rest)
                if 2 <= len(rest) <= 14:
                    major = rest
        education.append({
            "school": school,
            "degree": degree,
            "major": major,
            "period": period,
            "details": " ".join(details),
        })

    # ---- 实习/项目经历：按时间行切分条目 ----
    def _parse_entries(block_lines: list) -> list:
        entries = []
        cur = None
        for ln in block_lines:
            period_m = PERIOD_RE.search(ln) or re.match(r"^20\d{2}", ln)
            if period_m:
                if cur:
                    entries.append(cur)
                period = period_m.group(0) if hasattr(period_m, "group") else ""
                company = ln.replace(period, "").strip("　 -—–~至到") if period else ln
                cur = {
                    "company": company,
                    "title": "",
                    "period": period,
                    "duration": "",
                    "responsibilities": [],
                    "achievements": [],
                }
            elif cur is not None:
                if re.search(r"[\d%万]|提升|增长|降低|完成|达成|转化率|留存|DAU|GMV", ln):
                    cur["achievements"].append(ln)
                else:
                    cur["responsibilities"].append(ln)
        if cur:
            entries.append(cur)
        return entries

    work_experience = _parse_entries(sections["work"])
    # 归一化为统一结构
    for w in work_experience:
        w["responsibilities"] = w.get("responsibilities", [])[:20]

    projects = _parse_entries(sections["project"])
    for p in projects:
        if "项目" in p.get("company", "") and len(p["company"]) <= 12:
            p["name"] = p["company"]
            p["company"] = ""

    # ---- 技能 ----
    skill_text = " ".join(sections["skill"])
    skills = {
        "technical": [s.strip() for s in re.split(r"[、,，;；/|]", skill_text) if s.strip()][:30],
        "soft": [],
        "language": [],
    }

    return {
        "basic_info": basic_info,
        "education": education,
        "work_experience": work_experience,
        "projects": projects,
        "skills": skills,
        "_sections": sections,
    }
