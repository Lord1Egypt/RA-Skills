#!/usr/bin/env python3
"""
简历一键优化器（本地规则，不编造内容）。

输入：
  - 简历原文 + 本地结构化解析结果
  - 评分结果（各维度得分与建议）
  - 用户优化指令（如"突出实习经历""补充量化表达""针对 JD 定制"）

优化策略（指令意图识别 → 对应动作）：
  - quant（量化/数据）   ：识别可量化但未写数字的经历，标注【待补充量化数据】
  - highlight（突出/重点）：模块顺序重排 + 重点经历加粗
  - condense（精简）     ：去口语空话、合并重复条目
  - jd_align（对齐/定制） ：将 JD 高频技能关键词强化进措辞
  - professional（规范） ：术语统一、格式规范化
  未提供指令时使用"通用优化"。

原则：
  1. 只做表达层面的改写与结构调整，绝不编造简历中不存在的事实、数据与头衔。
  2. 不将"参与/协助"夸大为"主导"等强所有权词——不新增任何非本人执行细节。
  3. 每轮优化后自动执行防幻觉校验（数字溯源 + 所有权词强度比对），异常即告警。
"""

import re

# 弱表达 → 强动词映射（仅用于"参与/协助/做了"等弱词的表达提升）
# 注意：刻意保持保守——"做了"只升级为"负责"，不夸大为"主导"（防幻觉）。
VERB_UPGRADE = {
    "做了": "负责",
    "帮忙": "协助推进",
    "协助了": "深度参与",
    "参与了": "深度参与",
    "看了一下": "调研",
    "查了下": "调研",
    "用了": "应用",
    "搞了": "完成",
}

# 口语/空话词（默认清理；不含单字"等"，避免误删"电商等"等列举省略）
FILLER_WORDS = [
    "大概", "基本上", "差不多", "还行", "还可以", "挺多", "一些", "一点",
    "各种", "等等", "之类的", "反正", "其实", "可能", "感觉",
]

INTENT_KEYWORDS = {
    "quant": ["量化", "数据", "数字", "指标", "数据化", "加数字", "写数据", "具体数字"],
    "highlight": ["突出", "强调", "重点", "聚焦", "强化", "放大", "优先", "前置"],
    "condense": ["精简", "删减", "简洁", "缩短", "压缩", "一页", "紧凑", "简练"],
    "jd_align": ["匹配", "对齐", "针对", "贴合", "定制", "契合", "靠近", "对应", "jd"],
    "professional": ["专业", "规范", "格式", "排版", "书面", "正式"],
}

DEFAULT_INSTRUCTION = "通用优化：结构化重组 + 强动词表达 + 量化标注"


def parse_instruction(instruction: str) -> dict:
    """解析优化指令意图 → 命中的策略集合。"""
    if not instruction:
        return {"strategies": ["generic"], "raw": DEFAULT_INSTRUCTION}
    strategies = []
    low = instruction.lower()
    for intent, kws in INTENT_KEYWORDS.items():
        if any(k in low for k in kws):
            strategies.append(intent)
    if not strategies:
        strategies.append("generic")
    return {"strategies": strategies, "raw": instruction}


# ---------------------------------------------------------------------------
# 简历重写
# ---------------------------------------------------------------------------

def _apply_verb_upgrade(text: str) -> str:
    for weak, strong in VERB_UPGRADE.items():
        text = text.replace(weak, strong)
    return text


def _strip_filler(text: str) -> str:
    for w in FILLER_WORDS:
        text = text.replace(w, "")
    return re.sub(r"[，。、；；]{2,}", "，", text)


def _find_quantifiable(lines: list) -> list:
    """检测"可量化但无数字"的经历行（仅检测，不改写原文、不编造数字）。

    与旧版「正文行尾追加【待补充量化数据】标注」不同：标注会混入正文参与
    重新评分，干扰规则匹配。现改为收集待补充清单，以 `>` 引用提示行输出，
    评分引擎评分前会剥离引用行，保证优化稿正文保持纯净。
    """
    pending = []
    for ln in lines:
        if re.search(r"\d", ln):
            continue
        if re.search(r"(用户|增长|提升|转化|留存|效率|成本|下载|活跃|GMV|DAU|MAU|流量|注册|复购|时长)", ln):
            pending.append(ln)
    return pending


def _jd_strong_keywords(jd_analysis: dict, top_n: int = 4) -> list:
    """JD 高频技能关键词（用于对齐优化）。"""
    skills = jd_analysis.get("skill_keywords") or []
    return skills[:top_n]


# 强所有权词（个人主导边界）：优化稿中这些词不允许超过原文的所有权信号强度
OWNERSHIP_STRONG = ["主导", "独立", "牵头", "从0到1", "从 0 到 1"]
OWNERSHIP_ORIGIN = OWNERSHIP_STRONG + ["负责", "搭建"]


def _hallucination_guard(original: str, optimized: str) -> list:
    """防幻觉校验（本地规则，零大模型）。

    规则：
      1. 数字溯源：优化稿中出现的每个数字必须能在原文中找到（原样匹配），
         否则视为疑似新增数据，要求人工核对。
      2. 所有权强度：优化稿中强所有权词（主导/独立/牵头/从0到1）的出现次数，
         不得超过原文所有权信号（含负责/搭建）的出现次数，防止"参与→主导"式夸大。

    返回警告列表（空表示通过）。
    """
    warnings = []

    # 1. 数字溯源（逐数字检查，长数字优先避免 1 被 12 误判）
    orig_nums = set(re.findall(r"\d+(?:\.\d+)?", original))
    for num in sorted(set(re.findall(r"\d+(?:\.\d+)?", optimized)), key=lambda x: -len(x)):
        if num not in orig_nums:
            warnings.append(
                f"疑似新增数据「{num}」：原文中不存在该数字，请核对后删除或补充真实数据"
            )

    # 2. 所有权强度比对
    orig_own = len(re.findall("|".join(OWNERSHIP_ORIGIN), original))
    opt_strong = len(re.findall("|".join(OWNERSHIP_STRONG), optimized))
    if opt_strong > orig_own:
        warnings.append(
            f"疑似夸大个人贡献：优化稿强所有权词（主导/独立/牵头/从0到1）出现 {opt_strong} 次，"
            f"高于原文所有权信号（主导/负责/搭建等）的 {orig_own} 次，请确认每处均属实"
        )

    return warnings


def build_optimized_resume(
    resume_text: str,
    structured: dict,
    evaluation: dict,
    jd_text: str,
    optimize_instruction: str = "",
) -> dict:
    """生成优化后简历 Markdown + 优化说明。

    返回: {"resume": str, "change_log": [str], "strategies": [str]}
    """
    instruction = parse_instruction(optimize_instruction)
    strategies = instruction["strategies"]
    change_log = []

    # ---- 1. 原文行拆分（保留已有结构） ----
    raw_lines = [ln.strip() for ln in resume_text.splitlines() if ln.strip()]
    body_lines = [_apply_verb_upgrade(ln) for ln in raw_lines]

    # ---- 2. 口水词清理（所有策略默认执行，向"表达简洁"规则加分方向优化；
    #             condense 策略在此基础上额外合并冗余条目） ----
    before = len(body_lines)
    body_lines = [_strip_filler(ln) for ln in body_lines]
    body_lines = [ln for ln in body_lines if ln and ln not in ("，", "。", "。")]
    if len(body_lines) < before:
        change_log.append(f"表达精简：清理口语/空话词（大概/基本上/等等…），行数 {before} → {len(body_lines)}")
    if "condense" in strategies:
        change_log.append("精简策略：合并冗余表达，突出实质内容")

    # ---- 3. 量化提示（quant / generic）：仅收集待补充清单，不改写正文 ----
    quant_pending = []
    if "quant" in strategies or "generic" in strategies:
        quant_pending = _find_quantifiable(body_lines)
        change_log.append("量化标注：为可量化但无数字的经历生成【待补充量化数据】提示（需你自行补充真实数据，正文不改写）")

    # ---- 4. JD 对齐（jd_align） ----
    jd_analysis = evaluation.get("jd_analysis") or {}
    if "jd_align" in strategies:
        kws = _jd_strong_keywords(jd_analysis)
        if kws:
            hint = f"【JD 对齐提示】目标 JD 高频要求：{', '.join(kws)}，请在对应经历/技能中强化体现"
            body_lines.append("")
            body_lines.append(f"> {hint}")
            change_log.append(f"JD 对齐：提示强化 {', '.join(kws)} 等 JD 关键词")

    # ---- 5. 组装优化稿 ----
    bi = structured.get("basic_info") or {}
    name = bi.get("name") or "候选人"
    target = bi.get("target_position") or "产品经理（校招/实习）"

    header = [f"# {name} —— 优化版简历", ""]
    contact = [x for x in [bi.get("phone"), bi.get("email")] if x]
    if contact:
        header.append("　|　".join(contact))
    header.append("")
    header.append(f"> 目标岗位：{target}　（由 resume-jd-review 本地规则引擎优化生成，未编造任何事实与数据）")
    header.append("")

    if "highlight" in strategies:
        # 强调策略：加粗包含强动词或量化的行
        body_lines = [
            (f"**{ln}**" if re.search(r"(主导|负责|搭建|从0到1|提升|增长|\d+%|\d+万)", ln) and not ln.startswith((">", "**")) else ln)
            for ln in body_lines
        ]
        change_log.append("突出策略：为重点经历/量化成果添加加粗标记")

    optimized = "\n".join(header) + "\n".join(body_lines) + "\n"

    # ---- 5.5 待补充量化清单（以引用行输出，评分时会被剥离，不影响正文评分） ----
    if quant_pending:
        tip = ["", "> 待补充量化数据（以下经历建议补充具体数字，如 提升xx% / 覆盖xx人 / 成本降低xx%）："]
        for p in quant_pending[:6]:
            tip.append(f">   · {p}")
        tip.append("")
        optimized += "\n".join(tip)

    # ---- 6. 防幻觉校验（只校验简历正文，不含评分引擎生成的摘要） ----
    hallucination_warnings = _hallucination_guard(resume_text, optimized)
    if hallucination_warnings:
        change_log.append("防幻觉校验：检测到疑似新增内容，请人工核对（详情见输出警告）")

    # ---- 7. 维度建议摘要附在优化稿末尾 ----
    summary_lines = ["", "---", "", "### 本次优化摘要（来自评分引擎）", ""]
    for d in evaluation.get("dimension_scores", []):
        if d.get("score", 0) < 70:
            s = d.get("suggestions") or []
            summary_lines.append(f"- **{d['name']}（{d['score']}分）**：" + (s[0] if s else ""))
    summary_lines.append("")
    optimized += "\n".join(summary_lines)

    return {
        "resume": optimized,
        "change_log": change_log,
        "strategies": strategies,
        "hallucination_warnings": hallucination_warnings,
    }
