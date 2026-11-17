#!/usr/bin/env python3
"""
规则评分引擎：简历 × JD 的多维评分，完全本地计算，不依赖任何大模型。

每个评分维度由若干条规则（rules）组成，每条规则根据简历全文文本、
本地结构化解析结果、JD 关键词分析，给出 0-100 分、命中证据与说明。
所有得分均可追溯到具体规则与命中内容，可完全复现。

支持的规则类型：
  - section_presence   模块完整性（结构化字段是否存在）
  - contact_presence   联系方式完整性（电话/邮箱）
  - keyword_density    关键词覆盖密度
  - product_flow       产品完整链路（调研→需求→方案→落地→验证）
  - experience_count   实习/项目经历数量
  - action_verb        强动词使用
  - star_structure     STAR 结构（行动-结果信号）
  - quantified         量化成果检测（正则匹配数字+指标）
  - jd_coverage        JD 技能关键词覆盖率
  - jd_responsibility  JD 职责点覆盖率
  - skill_presence     技能清单命中
  - expression_quality 逻辑表达质量（逻辑词 + 篇幅）
  - industry_match     实习/项目行业方向匹配（JD 行业提示 vs 简历行业词）
  - substance_work     实际性工作闭环（调研→PRD→评审→落地→复盘）
  - major_relevance    专业是否计算机相关
  - logic_elements     项目逻辑四要素（背景/产出/价值衡量/北极星指标）
  - roadmap_presence   核心价值与长期目标（roadmap）
  - redundancy_check   重复/累赘表达检测
  - english_ability    英语工作语言能力（跨境行业）
  - ai_exploration     AI 落地产品与提效证据
  - soft_quality       软性素养四要素（责任心/创造力/逻辑严谨/热爱）
"""

import re
from dataclasses import dataclass, field

# 优化稿/报告中的元信息分节标记（评分/解析前应截断，避免元信息污染）
META_SECTION_MARKERS = ["## 本轮优化后的三部分诊断", "### 本次优化摘要"]


def strip_meta_text(text: str) -> str:
    """剥离优化稿/报告中的元信息，仅保留简历正文。

    优化器会在正文之外追加头部声明、量化提示、优化摘要与三部分诊断等元信息。
    若将优化稿整体重新提交评分或结构化解析，这些元信息会干扰规则匹配
    （摘要/诊断中的分数数字、建议文本、padding 词重复、"专业"等触发词），
    导致"优化后反而低分"的假象。本函数在评分与解析前统一剥离：

      1. 「本次优化摘要」「本轮优化后的三部分诊断」分节及其之后的所有内容；
      2. Markdown 标题行（#）、引用行（>）、表格行（|）、分隔线（---）；
      3. 行内【...】标注（如【待补充量化数据】【JD 对齐提示】）与强调符。
    """
    for marker in META_SECTION_MARKERS:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith(("#", ">", "|")):
            continue
        if re.match(r"^[-*_=]{3,}\s*$", s):
            continue
        s = re.sub(r"【[^】]*】", "", s)
        s = s.replace("**", "").replace("`", "").strip()
        if s:
            out.append(s)
    return "\n".join(out)


@dataclass
class RuleResult:
    """单条规则的计算结果。"""
    score: float = 0.0
    evidence: list = field(default_factory=list)   # 命中的具体内容（用于报告可追溯）
    detail: str = ""                               # 规则说明
    weight: float = 1.0                            # 规则在维度内权重


# ---------------------------------------------------------------------------
# 通用打分工具
# ---------------------------------------------------------------------------

def _ratio_score(hits: int, target: int, min_required: int = 0) -> float:
    """命中数 → 0-100 分。
    - 低于 min_required：按比例给分但封顶 55（严重不足，提示先补基础）
    - 达到 target：100 分
    """
    if target <= 0:
        return 0.0
    if hits <= 0:
        return 0.0
    if min_required > 0 and hits < min_required:
        return round(min(55.0, hits / min_required * 55.0), 1)
    return round(min(100.0, hits / target * 100.0), 1)


def _cover_score(covered: int, total: int, target_ratio: float) -> float:
    """覆盖率 → 0-100 分。"""
    if total <= 0:
        return 0.0
    ratio = covered / total
    return round(min(100.0, ratio / target_ratio * 100.0), 1)


# ---------------------------------------------------------------------------
# 规则实现
# ---------------------------------------------------------------------------

def _kw_pool(text: str) -> set:
    """从全文提取用于关键词匹配的池（大小写归一化）。"""
    return {w.lower() for w in re.findall(r"[\u4e00-\u9fa5A-Za-z0-9+#.]+", text)}


def _keyword_hits(text: str, keywords: list) -> list:
    """返回命中的关键词列表（支持子串匹配，适配中文复合词）。"""
    text_l = text.lower()
    return [kw for kw in keywords if kw.lower() in text_l]


def rule_section_presence(rule, ctx) -> RuleResult:
    st = ctx.get("structured") or {}
    sections = rule.get("sections", [])
    present = [s for s in sections if st.get(s)]
    missing = [s for s in sections if s not in present]
    per = rule.get("per_missing", 25)
    score = max(0.0, 100.0 - len(missing) * per)
    r = RuleResult(
        score=score,
        evidence=[f"已覆盖模块：{', '.join(present) or '无'}"],
        detail="检查教育/实习/项目/技能等关键模块是否齐全",
    )
    if missing:
        r.evidence.append(f"缺失模块：{', '.join(missing)}")
    return r


def rule_contact_presence(rule, ctx) -> RuleResult:
    bi = ctx.get("structured") or {}
    bi = bi.get("basic_info") or {}
    fields = rule.get("fields", ["phone", "email"])
    present = [f for f in fields if bi.get(f)]
    missing = [f for f in fields if f not in present]
    per = rule.get("per_missing", 15)
    score = max(0.0, 100.0 - len(missing) * per)
    r = RuleResult(
        score=score,
        evidence=[f"已提供：{', '.join(present) or '无'}"],
        detail="检查电话/邮箱等联系方式是否完整",
    )
    if missing:
        r.evidence.append(f"缺失：{', '.join(missing)}")
    return r


def rule_keyword_density(rule, ctx) -> RuleResult:
    text = ctx["resume_text"]
    hits = _keyword_hits(text, rule.get("keywords", []))
    r = RuleResult(
        score=_ratio_score(len(hits), rule.get("target_hits", 5), rule.get("min_required", 0)),
        evidence=[f"命中 {len(hits)} 个：{', '.join(hits[:12]) or '无'}"],
        detail="关键能力词在简历中的覆盖情况",
    )
    return r


def rule_product_flow(rule, ctx) -> RuleResult:
    text = ctx["resume_text"]
    flow = rule.get("flow_keywords", {})
    stages_hit = []
    for stage, kws in flow.items():
        if any(k in text for k in kws):
            stages_hit.append(stage)
    required = rule.get("required_stages", 3)
    covered = len(stages_hit)
    score = _ratio_score(covered, 5, min_required=required)
    if covered >= required:
        score = round(min(100.0, covered / 5 * 100.0), 1)
    r = RuleResult(
        score=score,
        evidence=[f"已覆盖产品环节：{' → '.join(stages_hit) or '无'}（共 5 环节，至少需要 {required} 个）"],
        detail="检测简历是否体现完整产品链路（调研→需求→方案→落地→验证）",
    )
    return r


def rule_experience_count(rule, ctx) -> RuleResult:
    st = ctx.get("structured") or {}
    work = st.get("work_experience") or []
    proj = st.get("projects") or []
    total = len(work) + len(proj)
    min_expected = rule.get("min_expected", 2)
    score = _ratio_score(total, min_expected, min_required=1)
    r = RuleResult(
        score=score,
        evidence=[f"实习经历 {len(work)} 段、项目经历 {len(proj)} 段"],
        detail=f"校招简历建议至少 {min_expected} 段实习/项目经历",
    )
    return r


def rule_action_verb(rule, ctx) -> RuleResult:
    text = ctx["resume_text"]
    hits = _keyword_hits(text, rule.get("verbs", []))
    r = RuleResult(
        score=_ratio_score(len(hits), rule.get("target_hits", 8), rule.get("min_required", 0)),
        evidence=[f"命中强动词 {len(hits)} 个：{', '.join(hits[:12]) or '无'}"],
        detail="经历描述是否使用强动词（主导/负责/搭建/推动等），体现个人贡献",
    )
    return r


def rule_star_structure(rule, ctx) -> RuleResult:
    text = ctx["resume_text"]
    result_hits = _keyword_hits(text, rule.get("result_words", []))
    context_hits = _keyword_hits(text, rule.get("context_words", []))
    # STAR 信号：行动 + 结果同时存在才算有效
    star_signals = min(len(result_hits), len(context_hits)) + (1 if result_hits else 0)
    # 依据：有结果词但缺背景词视为部分 STAR
    if result_hits and not context_hits:
        score = 50.0
        detail = "有结果词但缺少背景/任务描述（如“负责”“针对”“期间”），STAR 结构不完整"
    elif result_hits and context_hits:
        score = 90.0
        detail = "同时具备行动与结果描述，具备 STAR 结构基础"
    else:
        score = 20.0
        detail = "未检测到明确的行动-结果描述，建议按 STAR 结构重写经历"
    r = RuleResult(
        score=score,
        evidence=[
            f"结果类信号：{', '.join(result_hits[:10]) or '无'}",
            f"背景/任务类信号：{', '.join(context_hits[:10]) or '无'}",
        ],
        detail=detail,
    )
    return r


def rule_quantified(rule, ctx) -> RuleResult:
    text = ctx["resume_text"]
    patterns = rule.get("patterns", [])
    seen = []
    for p in patterns:
        for m in re.finditer(p, text):
            val = m.group(0)
            if val not in seen:
                seen.append(val)
    min_expected = rule.get("min_expected", 3)
    r = RuleResult(
        score=_ratio_score(len(seen), min_expected, min_required=1),
        evidence=[f"检测到 {len(seen)} 处量化成果：{', '.join(seen[:12]) or '无'}"],
        detail=f"量化数据（百分比/用户量/时长/指标等）是数据驱动能力的最直接体现，建议至少 {min_expected} 处",
    )
    return r


def rule_jd_coverage(rule, ctx) -> RuleResult:
    text = ctx["resume_text"]
    jd = ctx.get("jd_analysis") or {}
    skills = jd.get("skill_keywords") or []
    hits = _keyword_hits(text, skills)
    r = RuleResult(
        score=_cover_score(len(hits), len(skills), rule.get("target_ratio", 0.6)),
        evidence=[
            f"JD 技能关键词 {len(skills)} 个，简历覆盖 {len(hits)} 个：{', '.join(hits[:12]) or '无'}",
        ],
        detail="简历是否覆盖 JD 中要求的技能关键词",
    )
    return r


def rule_jd_responsibility(rule, ctx) -> RuleResult:
    text = ctx["resume_text"]
    jd = ctx.get("jd_analysis") or {}
    resp = jd.get("responsibilities") or []
    if not resp:
        r = RuleResult(
            score=100.0,
            evidence=["JD 未提取到明确职责点，本规则不扣分"],
            detail="JD 职责点覆盖",
        )
        return r
    hits = []
    for item in resp:
        kw = item.get("keyword", "")
        if kw and kw in text:
            hits.append(kw)
    r = RuleResult(
        score=_cover_score(len(hits), len(resp), rule.get("target_ratio", 0.4)),
        evidence=[f"JD 职责点 {len(resp)} 个，简历覆盖 {len(hits)} 个：{', '.join(hits[:12]) or '无'}"],
        detail="简历是否覆盖 JD 中的核心职责点",
    )
    return r


def rule_skill_presence(rule, ctx) -> RuleResult:
    text = ctx["resume_text"]
    hits = _keyword_hits(text, rule.get("skills", []))
    r = RuleResult(
        score=_ratio_score(len(hits), rule.get("target_hits", 3), rule.get("min_required", 0)),
        evidence=[f"命中技能 {len(hits)} 个：{', '.join(hits[:12]) or '无'}"],
        detail="产品经理常用工具与技能覆盖情况（Axure/Figma/PRD/SQL 等）",
    )
    return r


def rule_expression_quality(rule, ctx) -> RuleResult:
    text = ctx["resume_text"]
    logic_hits = _keyword_hits(text, rule.get("logic_words", []))
    length = len(text)
    min_length = rule.get("min_length", 200)
    # 篇幅分 + 逻辑词分
    length_score = min(60.0, length / max(min_length, 1) * 60.0) if length > 0 else 0.0
    logic_score = _ratio_score(len(logic_hits), rule.get("target_hits", 5), 2)
    score = round(length_score * 0.5 + logic_score * 0.5, 1)
    r = RuleResult(
        score=score,
        evidence=[
            f"简历篇幅 {length} 字（建议 ≥{min_length} 字）",
            f"逻辑连接词命中 {len(logic_hits)} 个：{', '.join(logic_hits[:10]) or '无'}",
        ],
        detail="表达是否有条理、有重点、篇幅是否充实",
    )
    return r


def rule_industry_match(rule, ctx) -> RuleResult:
    """实习/项目行业方向匹配：JD 行业提示 vs 简历行业词。"""
    text = ctx["resume_text"]
    industries = rule.get("industries", [])
    jd = ctx.get("jd_analysis") or {}
    jd_hints = jd.get("industry_hints") or []
    # 简历自身命中行业词
    resume_hits = [ind for ind in industries if ind in text]
    # JD 行业提示与简历的匹配
    jd_cover = [h for h in jd_hints if h in text] if jd_hints else []
    score = 0.0
    if jd_hints:
        # 50% 权重来自 JD 行业覆盖，50% 来自简历行业丰富度
        cover_part = _cover_score(len(jd_cover), len(jd_hints), 1.0)
        resume_part = _ratio_score(len(resume_hits), 2, min_required=0)
        score = round(cover_part * 0.6 + resume_part * 0.4, 1)
    else:
        score = _ratio_score(len(resume_hits), 2, min_required=0)
    r = RuleResult(
        score=score,
        evidence=[
            f"JD 行业提示：{', '.join(jd_hints) or '无'}；简历命中行业：{', '.join(resume_hits[:10]) or '无'}",
            f"JD 行业覆盖 {len(jd_cover)}/{len(jd_hints) or 0}",
        ],
        detail="实习/项目经历的工作方向是否与 JD 行业（电商、游戏、金融、AI 等）一致",
    )
    return r


def rule_substance_work(rule, ctx) -> RuleResult:
    """实际性工作闭环：调研→产出PRD→评审→落地→复盘。"""
    text = ctx["resume_text"]
    flow = rule.get("flow_keywords", {})
    stages_hit = []
    for stage, kws in flow.items():
        if any(k in text for k in kws):
            stages_hit.append(stage)
    required = rule.get("required_stages", 3)
    covered = len(stages_hit)
    score = _ratio_score(covered, 5, min_required=required)
    if covered >= required:
        score = round(min(100.0, covered / 5 * 100.0), 1)
    r = RuleResult(
        score=score,
        evidence=[f"已覆盖实际性工作环节：{' → '.join(stages_hit) or '无'}（共 5 环节，至少需要 {required} 个）"],
        detail="实习是否做过完整调研→落地PRD→评审→上线→复盘等实际性工作（而非打杂）",
    )
    return r


def rule_major_relevance(rule, ctx) -> RuleResult:
    """专业是否计算机相关。"""
    st = ctx.get("structured") or {}
    edu = st.get("education") or []
    major = ""
    for e in edu:
        m = (e.get("major") or "").strip()
        if m:
            major = m
            break
    # 未解析到专业则从全文尝试
    text = ctx["resume_text"]
    if not major:
        mm = re.search(r"([\u4e00-\u9fa5A-Za-z]{2,12}?)(?:专业)", text)
        if mm:
            major = mm.group(1)
    related = rule.get("related", [])
    if not major:
        r = RuleResult(
            score=50.0,
            evidence=["未识别到专业信息（建议在简历中写明专业）"],
            detail="当前专业是否为计算机相关（计算机/软件/信息/电子/通信/自动化/AI 等）",
        )
        return r
    hit = [k for k in related if k in major]
    if hit:
        r = RuleResult(
            score=100.0,
            evidence=[f"专业「{major}」命中计算机相关关键词：{', '.join(hit)}"],
            detail="当前专业是否为计算机相关",
        )
    else:
        r = RuleResult(
            score=40.0,
            evidence=[f"专业「{major}」不在计算机相关词库（{', '.join(related[:8])}等）"],
            detail="当前专业是否为计算机相关（非相关专业需靠经历证明产品能力）",
        )
    return r


def rule_logic_elements(rule, ctx) -> RuleResult:
    """项目逻辑四要素：背景/产出/价值衡量/北极星指标。"""
    text = ctx["resume_text"]
    elements = rule.get("elements", {})
    hit_elements = []
    for elem, kws in elements.items():
        if any(k in text for k in kws):
            hit_elements.append(elem)
    min_need = rule.get("min_elements", 3)
    total = len(elements) or 1
    covered = len(hit_elements)
    score = round(covered / total * 100.0, 1) if covered > 0 else 0.0
    r = RuleResult(
        score=score,
        evidence=[
            f"已体现 {covered}/{total} 个要素：{', '.join(hit_elements) or '无'}",
            f"建议至少覆盖 {min_need} 个（尤其「背景-产出-价值衡量-北极星指标」）",
        ],
        detail="项目描述是否讲清背景（为什么做）、产出（做了什么）、价值衡量（怎么衡量）与北极星指标",
    )
    return r


def rule_roadmap_presence(rule, ctx) -> RuleResult:
    """核心价值与长期目标（roadmap）。"""
    text = ctx["resume_text"]
    hits = _keyword_hits(text, rule.get("keywords", []))
    score = 0.0 if not hits else min(100.0, 40.0 + len(hits) * 20.0)
    r = RuleResult(
        score=round(score, 1),
        evidence=[f"roadmap/长期目标相关词命中：{', '.join(hits[:10]) or '无'}"],
        detail="简历能否看到项目的核心价值与长期目标（roadmap/规划/里程碑）",
    )
    return r


def rule_redundancy_check(rule, ctx) -> RuleResult:
    """重复/累赘表达检测：填充词过度重复扣分。"""
    text = ctx["resume_text"]
    padding = rule.get("padding_words", [])
    max_repeats = rule.get("max_repeats", 4)
    min_length = rule.get("min_length", 120)
    if len(text) < min_length:
        r = RuleResult(
            score=60.0,
            evidence=[f"篇幅仅 {len(text)} 字，信息量不足，表达空间有限"],
            detail="简历描述是否重复、累赘、空洞（口水词/套话占比过高）",
        )
        return r
    counts = {w: text.count(w) for w in padding if text.count(w) >= 2}
    over = {w: c for w, c in counts.items() if c > max_repeats}
    if over:
        score = max(30.0, 100.0 - sum(c - max_repeats for c in over.values()) * 10)
        r = RuleResult(
            score=round(score, 1),
            evidence=[f"过度重复的口水词：{'；'.join(f'{w}×{c}' for w, c in over.items())}"],
            detail="简历描述是否重复、累赘、空洞（口水词/套话占比过高）",
        )
    else:
        r = RuleResult(
            score=100.0,
            evidence=[f"未发现过度重复的填充词（共出现 {'、'.join(f'{w}×{c}' for w, c in counts.items()) or '无'}）"],
            detail="简历描述是否重复、累赘、空洞（口水词/套话占比过高）",
        )
    return r


def rule_english_ability(rule, ctx) -> RuleResult:
    """英语工作语言能力（跨境行业硬性要求时权重放大）。"""
    text = ctx["resume_text"]
    jd_text = ctx.get("jd_text") or ""
    certs = rule.get("certs", [])
    cross_hint = rule.get("cross_border_hint", [])
    hit_certs = _keyword_hits(text, certs)
    is_cross = any(h in jd_text for h in cross_hint)
    if hit_certs:
        score = 100.0
        detail = "简历体现英语能力（证书/工作语言），可作为工作语言"
    elif is_cross:
        score = 30.0
        detail = "JD 为跨境/出海/国际业务方向，但简历未体现英语能力，建议补充 CET-4/6 或雅思托福成绩"
    else:
        score = 60.0
        detail = "岗位未强制要求英语，但建议补充英语能力以增强竞争力"
    r = RuleResult(
        score=float(score),
        evidence=[f"英语能力证据：{', '.join(hit_certs[:8]) or '无'}；JD 跨境提示：{'是' if is_cross else '否'}"],
        detail=detail,
    )
    return r


def rule_ai_exploration(rule, ctx) -> RuleResult:
    """AI 落地产品与提效证据。"""
    text = ctx["resume_text"]
    ai_kws = rule.get("ai_keywords", [])
    out_kws = rule.get("output_keywords", [])
    ai_hits = _keyword_hits(text, ai_kws)
    out_hits = [k for k in out_kws if k in text]
    if ai_hits and out_hits:
        score = 100.0
        detail = "同时具备 AI 应用 + 落地/提效证据，AI 探索能力强"
    elif ai_hits:
        score = 55.0
        detail = "提到 AI 相关技术/工具，但缺少落地、产出或提效证据，建议补充具体成果"
    elif out_hits:
        score = 40.0
        detail = "有产出/提效描述，但未体现 AI 能力，建议补充 AI 工具或大模型的实际应用"
    else:
        score = 15.0
        detail = "未体现 AI 探索与应用能力，建议补充 AI 工具/大模型/AIGC 的实际使用与产出"
    r = RuleResult(
        score=float(score),
        evidence=[
            f"AI 关键词命中：{', '.join(ai_hits[:10]) or '无'}",
            f"落地/提效词命中：{', '.join(out_hits[:10]) or '无'}",
        ],
        detail=detail,
    )
    return r


def rule_soft_quality(rule, ctx) -> RuleResult:
    """软性素养四要素：责任心/创造力/逻辑严谨/热爱。"""
    text = ctx["resume_text"]
    traits = rule.get("traits", {})
    hit_traits = []
    for trait, kws in traits.items():
        if any(k in text for k in kws):
            hit_traits.append(trait)
    min_need = rule.get("min_traits", 3)
    total = len(traits) or 1
    covered = len(hit_traits)
    score = round(covered / total * 100.0, 1) if covered > 0 else 0.0
    r = RuleResult(
        score=score,
        evidence=[
            f"已体现 {covered}/{total} 项素养：{', '.join(hit_traits) or '无'}",
            f"建议至少覆盖 {min_need} 项（责任心/创造力/逻辑严谨/热爱）",
        ],
        detail="软性素养四要素：责任心（不半途而废）、创造力、逻辑严谨（定量定性+规划）、热爱（持续体验产品）",
    )
    return r


RULE_REGISTRY = {
    "section_presence": rule_section_presence,
    "contact_presence": rule_contact_presence,
    "keyword_density": rule_keyword_density,
    "product_flow": rule_product_flow,
    "experience_count": rule_experience_count,
    "action_verb": rule_action_verb,
    "star_structure": rule_star_structure,
    "quantified": rule_quantified,
    "jd_coverage": rule_jd_coverage,
    "jd_responsibility": rule_jd_responsibility,
    "skill_presence": rule_skill_presence,
    "expression_quality": rule_expression_quality,
    "industry_match": rule_industry_match,
    "substance_work": rule_substance_work,
    "major_relevance": rule_major_relevance,
    "logic_elements": rule_logic_elements,
    "roadmap_presence": rule_roadmap_presence,
    "redundancy_check": rule_redundancy_check,
    "english_ability": rule_english_ability,
    "ai_exploration": rule_ai_exploration,
    "soft_quality": rule_soft_quality,
}


def run_rule(rule: dict, ctx: dict) -> RuleResult:
    """执行单条规则，未知规则类型返回 0 分。"""
    fn = RULE_REGISTRY.get(rule.get("type", ""))
    if fn is None:
        return RuleResult(0.0, ["未知规则类型，按 0 分处理"], f"规则 {rule.get('type')}")
    try:
        result = fn(rule, ctx)
    except Exception as exc:  # 规则异常不影响整体评分
        result = RuleResult(0.0, [f"规则执行异常：{exc}"], rule.get("label", "未命名规则"))
    result.weight = float(rule.get("weight", 1.0))
    return result
