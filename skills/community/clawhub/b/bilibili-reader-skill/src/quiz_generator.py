"""理解度测验生成模块

功能：
1. 基于 VideoSummary 生成选择题和简答题
2. 答案直接来自总结内容，保证准确性
3. 支持难度分级（easy / medium / hard）
"""

import json
from dataclasses import dataclass, field


@dataclass
class Quiz:
    """单道测验题"""
    question_cn: str
    options_cn: list[str] | None = None  # None = 简答题
    answer: str | None = None  # "A", "B", "C", "D" 或简答关键词
    source: str = ""   # 来源字段，如 "key_points_cn[2]"
    difficulty: str = "medium"  # easy / medium / hard
    type: str = "choice"  # choice / open


QUIZ_PROMPT_TEMPLATE = """基于以下视频总结，生成 {count} 道理解度测验题。

## 视频信息
标题：{title}
体裁：{genre}

## 核心要点
{key_points}

## 内容摘要
{summary}

## 洞察
{insights}

## 要求
1. 优先使用选择题（4个选项），必须只有1个正确答案
2. 答案必须直接来自上述总结内容，不得编造
3. 干扰项要有一定迷惑性，但明显违背原文的选项要排除
4. 每道题必须标注 source（来源字段，如 key_points[0]）
5. 难度比例：easy:medium:hard = 1:1:1
6. 只输出 JSON，不要有任何额外文字

## 输出格式（JSON数组）
[
  {{
    "question_cn": "题目内容（30-50字）",
    "options_cn": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
    "answer": "B",
    "source": "key_points[0]",
    "difficulty": "easy",
    "type": "choice"
  }},
  {{
    "question_cn": "简答题题目",
    "answer": "答案关键词",
    "source": "insights_cn",
    "difficulty": "hard",
    "type": "open"
  }}
]
"""


def _extract_json(text: str) -> str:
    """从 LLM 返回中提取 JSON"""
    if "```json" in text:
        return text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text.strip()


def generate_quizzes(
    title: str,
    genre: str,
    key_points: list[str],
    summary: str,
    insights: str,
    count: int = 3,
    llm_caller=None,
) -> list[Quiz]:
    """
    生成理解度测验题

    Args:
        title: 视频标题
        genre: 体裁标签
        key_points: 核心要点列表
        summary: 内容摘要
        insights: 洞察
        count: 生成题数
        llm_caller: LLM 调用函数

    Returns:
        Quiz 列表
    """
    if not llm_caller:
        return []

    key_points_text = "\n".join(
        f"{i}. {p}" for i, p in enumerate(key_points)
    )

    prompt = QUIZ_PROMPT_TEMPLATE.format(
        title=title,
        genre=genre,
        key_points=key_points_text or "无",
        summary=summary[:300] if summary else "无",
        insights=insights[:200] if insights else "无",
        count=count,
    )

    try:
        response = llm_caller(prompt)
        data = json.loads(_extract_json(response))
        return [_raw_to_quiz(q) for q in data]
    except (json.JSONDecodeError, TypeError):
        return []


def generate_quizzes_from_summary(
    summary,  # VideoSummary
    count: int = 3,
    llm_caller=None,
) -> list[Quiz]:
    """
    从 VideoSummary 直接生成测验题（便捷封装）
    """
    return generate_quizzes(
        title=summary.title_cn,
        genre=summary.genre,
        key_points=summary.key_points_cn,
        summary=summary.summary_cn,
        insights=summary.insights_cn,
        count=count,
        llm_caller=llm_caller,
    )


def _raw_to_quiz(raw: dict) -> Quiz:
    """将原始 dict 转为 Quiz 对象"""
    return Quiz(
        question_cn=raw.get("question_cn", ""),
        options_cn=raw.get("options_cn"),
        answer=raw.get("answer"),
        source=raw.get("source", ""),
        difficulty=raw.get("difficulty", "medium"),
        type=raw.get("type", "choice"),
    )


def quiz_to_template_dict(quiz: Quiz) -> dict:
    """将 Quiz 转为 PDF 模板可用的 dict"""
    return {
        "question_cn": quiz.question_cn,
        "options_cn": quiz.options_cn,
        "answer": quiz.answer,
        "source": quiz.source,
        "difficulty": quiz.difficulty,
        "type": quiz.type,
    }
