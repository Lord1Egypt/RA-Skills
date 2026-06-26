#!/usr/bin/env python3
"""
Judge Prompts — 评测者提示词模板库

提供多种预制 Rubric 和 Judge Prompt 模板，适用于不同任务类型。
使用时：导入 JUDGE_PROMPTS_BUILDERS，传入 task/solutions/rubric 即可。
"""

from typing import List, Dict, Any, Callable


# ═══════════════════════════════════════════════════════════════════════════════
# GENERIC RUBRIC
# ═══════════════════════════════════════════════════════════════════════════════

GENERIC_RUBRIC = [
    "准确性（答案是否正确）",
    "完整性（是否覆盖所有要点）",
    "表达质量（语言是否流畅、清晰）",
    "创意/深度（是否有独到见解）",
]


# ═══════════════════════════════════════════════════════════════════════════════
# TASK-SPECIFIC RUBRICS
# ═══════════════════════════════════════════════════════════════════════════════

RUBRIC_TEMPLATES: Dict[str, List[str]] = {
    "creative_writing": [
        "主题契合度（是否紧扣主题）",
        "文学质量（修辞、意象、节奏感）",
        "原创性（是否有独特视角）",
        "情感共鸣（是否引发读者情感反应）",
        "语言精准性（遣词造句是否准确优美）",
    ],
    "code_generation": [
        "正确性（代码能否正确运行）",
        "可读性（命名、注释、结构是否清晰）",
        "效率（时间/空间复杂度是否合理）",
        "安全性（是否有注入等风险）",
        "完整性（是否处理边界情况）",
    ],
    "logical_reasoning": [
        "答案准确性（最终答案是否正确）",
        "推理过程（推理步骤是否严谨）",
        "解释清晰度（是否易于理解）",
        "简洁性（解法是否简洁优雅）",
    ],
    "knowledge_qa": [
        "事实准确性（信息是否正确）",
        "完整性（是否覆盖问题的各个方面）",
        "来源可靠性（是否引用可信来源）",
        "表达清晰度（回答是否条理分明）",
    ],
    "multi_step_task": [
        "任务完成度（是否完成了所有子任务）",
        "质量深度（分析是否有深度）",
        "结构组织（逻辑是否清晰）",
        "可执行性（建议是否实际可行）",
        "创意价值（是否有独特见解）",
    ],
    "general": GENERIC_RUBRIC,
}


# ═══════════════════════════════════════════════════════════════════════════════
# JUDGE PROMPT BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_judge_prompt(
    task: str,
    solution_1: str,
    solution_2: str,
    rubric: List[str],
    task_type: str = "general",
) -> str:
    """
    构建完整的 Judge 评测 Prompt。

    参数：
        task: 用户任务描述
        solution_1: 方案1内容（匿名）
        solution_2: 方案2内容（匿名）
        rubric: 评分维度列表
        task_type: 任务类型（影响输出格式）

    返回：完整的 Judge Prompt 字符串
    """
    rubric_display = "\n".join(
        f"  {i+1}. {dim}（满分10分）"
        for i, dim in enumerate(rubric)
    )
    rubric_detail = "\n".join(
        f"方案1-{dim}: X/10（简短说明）\n方案2-{dim}: X/10（简短说明）"
        for dim in rubric
    )

    return f"""你是一位严格公正的 AI 评测专家。请对以下两个匿名方案进行盲评——
你不知道方案1来自哪个参赛者，也不知道方案2来自哪个参赛者。
你的评判应该专业、客观、有理有据。

【评测任务】
{task}

【评分维度】（每项满分 10 分）
{rubric_display}

【方案1内容】
{solution_1}

【方案2内容】
{solution_2}

【输出要求】严格按以下格式输出，不要有任何其他内容：

[SCORES]
{rubric_detail}
[/SCORES]
[TOTAL_A]{len(rubric)}项得分之和[/TOTAL_A]
[TOTAL_B]{len(rubric)}项得分之和[/TOTAL_B]
[WINNER]方案1 或 方案2 或 平局[/WINNER]
[COMMENT]总体评语（150字以内，简要说明胜出原因或平局理由）[/COMMENT]"""


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT PARSER
# ═══════════════════════════════════════════════════════════════════════════════

def parse_judge_response(
    text: str,
    rubric: List[str],
) -> Dict[str, Any]:
    """
    解析 Judge 的回复，提取分数、胜者和评语。

    参数：
        text: Judge 的原始输出
        rubric: 评分维度列表

    返回：
        {
            "scores_a": {dim: score, ...},
            "scores_b": {dim: score, ...},
            "total_a": float,
            "total_b": float,
            "winner": "solution_1" | "solution_2" | "tie",
            "comment": str,
        }
    """
    result = {
        "scores_a": {},
        "scores_b": {},
        "total_a": 0.0,
        "total_b": 0.0,
        "winner": "tie",
        "comment": "",
    }

    # Parse each rubric dimension
    import re
    lines = text.split("\n")

    for i, dim in enumerate(rubric):
        # Match lines like "方案1-准确性: 8/10（理由）" or "方案1-准确性: 8/10"
        dim_short = dim.split("（")[0].strip()  # "准确性（答案是否正确）" → "准确性"
        for line in lines:
            stripped = line.strip()
            # Check for solution 1
            if f"方案1" in stripped and dim_short in stripped:
                m = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", stripped)
                if m:
                    result["scores_a"][dim] = float(m.group(1))
            # Check for solution 2
            if f"方案2" in stripped and dim_short in stripped:
                m = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", stripped)
                if m:
                    result["scores_b"][dim] = float(m.group(1))

    # Parse totals
    ta_match = re.search(r"\[TOTAL_A\](.*?)\[/TOTAL_A\]", text, re.DOTALL)
    if ta_match:
        try:
            result["total_a"] = float(ta_match.group(1).strip())
        except ValueError:
            result["total_a"] = sum(result["scores_a"].values())

    tb_match = re.search(r"\[TOTAL_B\](.*?)\[/TOTAL_B\]", text, re.DOTALL)
    if tb_match:
        try:
            result["total_b"] = float(tb_match.group(1).strip())
        except ValueError:
            result["total_b"] = sum(result["scores_b"].values())

    # Fallback: calculate from individual scores if totals missing
    if result["total_a"] == 0:
        result["total_a"] = sum(result["scores_a"].values())
    if result["total_b"] == 0:
        result["total_b"] = sum(result["scores_b"].values())

    # Parse winner
    w_match = re.search(r"\[WINNER\](.*?)\[/WINNER\]", text, re.DOTALL)
    if w_match:
        winner_raw = w_match.group(1).strip()
        if "方案1" in winner_raw:
            result["winner"] = "solution_1"
        elif "方案2" in winner_raw:
            result["winner"] = "solution_2"
        else:
            result["winner"] = "tie"

    # Parse comment
    c_match = re.search(r"\[COMMENT\](.*?)\[/COMMENT\]", text, re.DOTALL)
    if c_match:
        result["comment"] = c_match.group(1).strip()

    return result


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK API
# ═══════════════════════════════════════════════════════════════════════════════

def get_default_rubric(task_type: str = "general") -> List[str]:
    """获取指定任务类型的默认评分维度。"""
    return RUBRIC_TEMPLATES.get(task_type, GENERIC_RUBRIC)


# Example usage:
if __name__ == "__main__":
    rubric = get_default_rubric("creative_writing")
    prompt = build_judge_prompt(
        task="写一首关于春天的七言绝句",
        solution_1="春风又绿江南岸，明月何时照我还",
        solution_2="千里莺啼绿映红，水村山郭酒旗风",
        rubric=rubric,
    )
    print("=== Judge Prompt 示例 ===")
    print(prompt)
    print("\n=== 解析测试 ===")
    sample_response = """
[SCORES]
方案1-主题契合度: 9/10（紧扣春天主题）
方案1-文学质量: 8/10
方案2-主题契合度: 8/10
方案2-文学质量: 9/10
[/SCORES]
[TOTAL_A]35[/TOTAL_A]
[TOTAL_B]36[/TOTAL_B]
[WINNER]方案2[/WINNER]
[COMMENT]两首均佳，方案2意象更丰富。[/COMMENT]
"""
    result = parse_judge_response(sample_response, rubric)
    print(result)
