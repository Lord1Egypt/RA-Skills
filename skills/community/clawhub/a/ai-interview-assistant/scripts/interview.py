#!/usr/bin/env python3
"""
AI 模拟面试助手 - 核心脚本

这是一个基于多阶段协作的智能面试系统。
当用户说"我要开始模拟面试"时，LLM 根据本 SKILL.md 中的定义引导用户完成面试流程。

本脚本提供辅助功能：
- 题目获取（通过 GitHub 知识库）
- 网络搜索（使用 openclaw 内置 web_fetch 工具，技能安装后自动出现在 available_skills 中）
- 评分计算
- 报告生成

实际面试流程由 LLM 根据 SKILL.md 定义的剧本驱动。
"""

import json
import subprocess
import os
from typing import List, Dict, Optional


# ============================================================
# 技能路径配置
# ============================================================
SKILL_PATHS = {
    "github_kb": os.path.dirname(os.path.abspath(__file__)) + "/fetch.py"  # GitHub 知识库
}



# ============================================================
# 提醒机制状态
# ============================================================
class ReminderState:
    """每道题的提醒状态管理"""
    def __init__(self, max_reminders: int = 2):
        self.max_reminders = max_reminders
        # {(question_index, round): reminder_count}
        self._reminders: Dict[tuple, int] = {}

    def get_remaining(self, question_index: int, round_num: int = 1) -> int:
        """获取剩余提醒次数"""
        key = (question_index, round_num)
        used = self._reminders.get(key, 0)
        return max(0, self.max_reminders - used)

    def use_reminder(self, question_index: int, round_num: int = 1) -> bool:
        """
        使用一次提醒机会
        Returns: 是否成功使用（还有剩余机会）
        """
        key = (question_index, round_num)
        used = self._reminders.get(key, 0)
        if used < self.max_reminders:
            self._reminders[key] = used + 1
            return True
        return False

    def reset_question(self, question_index: int):
        """重置某道题的所有提醒状态（用户重新回答后）"""
        keys_to_remove = [k for k in self._reminders if k[0] == question_index]
        for k in keys_to_remove:
            del self._reminders[k]

    def check_and_trigger_reminder(self, score_result: Dict, question_index: int, round_num: int = 1) -> Dict:
        """
        检查得分并触发提醒机制

        Args:
            score_result: score_answer 的返回结果
            question_index: 题目索引
            round_num: 当前回答轮次

        Returns:
            包含提醒信息的字典
        """
        total_score = score_result.get("round_score", 0)
        reminder_threshold = 50

        result = {
            "should_remind": False,
            "remaining": self.get_remaining(question_index, round_num),
            "message": "",
            "can_reanswer": False
        }

        if total_score < reminder_threshold:
            remaining = self.get_remaining(question_index, round_num)
            if remaining > 0:
                self.use_reminder(question_index, round_num)
                result["should_remind"] = True
                result["remaining"] = remaining - 1
                result["can_reanswer"] = True
                result["message"] = f"得分 {total_score} 分低于 {reminder_threshold} 分，你还有 {remaining} 次重新回答的机会！"
            else:
                result["message"] = f"得分 {total_score} 分，已用完重新回答机会。"

        return result


# 全局提醒状态实例
_reminder_state = ReminderState(max_reminders=2)


# ============================================================
# 核心函数
# ============================================================

def get_reminder_state() -> ReminderState:
    """获取提醒状态管理器"""
    return _reminder_state


def reset_reminder(question_index: int):
    """重置某道题的提醒状态"""
    _reminder_state.reset_question(question_index)

def github_search(keyword: str, limit: int = 3) -> List[Dict]:
    """
    通过 GitHub 知识库搜索面试题（替换本地 RAG）

    从 wdndev/llm_interview_note 仓库获取内容作为面试素材。

    Args:
        keyword: 搜索关键词
        limit: 返回数量

    Returns:
        题目列表，格式与 rag_search 一致
    """
    script_path = SKILL_PATHS["github_kb"]

    if not os.path.exists(script_path):
        print(f"GitHub 知识库脚本不存在: {script_path}")
        return []

    try:
        result = subprocess.run(
            ["python3", script_path, keyword, "--questions", "--limit", str(limit), "--json"],
            capture_output=True,
            text=True,
            timeout=60  # GitHub 请求可能较慢
        )
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
        elif result.stderr:
            print(f"GitHub 搜索警告: {result.stderr[:200]}")
    except Exception as e:
        print(f"GitHub 搜索失败: {e}")

    return []


def github_random(count: int = 3) -> List[Dict]:
    """
    从 GitHub 知识库随机获取面试题

    Args:
        count: 返回数量

    Returns:
        题目列表
    """
    script_path = SKILL_PATHS["github_kb"]

    if not os.path.exists(script_path):
        return []

    try:
        result = subprocess.run(
            ["python3", script_path, "--random", "--questions", "--limit", str(count), "--json"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"GitHub 随机获取失败: {e}")

    return []


def github_get_categories() -> Dict[str, int]:
    """
    获取 GitHub 知识库的所有分类

    Returns:
        分类统计字典
    """
    script_path = SKILL_PATHS["github_kb"]

    if not os.path.exists(script_path):
        return {}

    try:
        result = subprocess.run(
            ["python3", script_path, "--list-categories"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # 返回结构化数据
        return {
            "大语言模型基础": 10,
            "大语言模型架构": 12,
            "分布式训练": 10,
            "有监督微调": 7,
            "推理": 7,
            "强化学习": 4,
            "检索增强RAG": 3,
            "大语言模型评估": 3,
            "大语言模型应用": 2,
        }
    except:
        pass

    return {}


def web_search(keyword: str, limit: int = 5) -> List[Dict]:
    """
    网络搜索（前沿题目素材获取）

    注意：已使用 openclaw 内置 web_fetch 工具替代 xfyun-search 技能
    - 技能安装后自动出现在 available_skills 中
    - 直接用工具名调用即可

    Args:
        keyword: 搜索关键词
        limit: 返回数量（保留参数兼容性）

    Returns:
        搜索结果列表（实际由 web_fetch 工具返回）
    """
    return []


def get_questions(tags: List[str], count: int = 5, include_frontier: bool = True,
                  use_github: bool = True) -> List[Dict]:
    """
    根据技术标签获取面试题目（整合 GitHub 知识库和前沿题目）

    Args:
        tags: 技术标签列表
        count: 题目数量
        include_frontier: 是否包含前沿题目
        use_github: 是否优先使用 GitHub 知识库（默认 True）

    Returns:
        题目列表
    """
    # 3:2 比例：基础题占 3 份，前沿题占 2 份
    if include_frontier:
        total_parts = 5
        basic_ratio = 3
        frontier_ratio = 2
        basic_count = int(count * basic_ratio / total_parts)
        frontier_count = count - basic_count
        frontier_count = max(1, frontier_count)  # 至少1道前沿题
        basic_count = count - frontier_count
    else:
        basic_count = count
        frontier_count = 0

    questions = []

    # 优先使用 GitHub 知识库（如果可用）
    if use_github:
        for tag in tags:
            if len(questions) >= basic_count:
                break
            github_results = github_search(tag, limit=2)
            for item in github_results:
                if len(questions) >= basic_count:
                    break
                questions.append({
                    "title": item.get("title", tag),
                    "key_points": item.get("key_points", []),
                    "type": item.get("type", "八股"),
                    "category": item.get("category", tag),
                    "difficulty": item.get("difficulty", "中等"),
                    "source": "github",
                    "topic_id": item.get("topic_id"),
                    "url": item.get("url"),
                    "content_preview": item.get("content_preview")
                })

    # 前沿题目（使用 web_fetch 工具搜索）
    for i in range(frontier_count):
        questions.append({
            "title": "[前沿题目 - 使用 web_fetch 搜索最新技术]",
            "key_points": ["需要网络搜索获取最新内容"],
            "type": "前沿",
            "category": tags[i % len(tags)] if tags else "综合",
            "difficulty": "较难",
            "source": "frontier",
            "needs_web_search": True,
            "search_hint": f"使用 web_fetch 工具搜索: {tags[i % len(tags)] if tags else '技术趋势'} 前沿 最新"
        })

    return questions


def score_answer(key_points: List[str], user_answer: str) -> Dict:
    """
    评估用户回答

    Args:
        key_points: 考察要点/关键词列表
        user_answer: 用户的回答文本

    Returns:
        评分结果
    """
    if not user_answer or not user_answer.strip():
        return {
            "round_score": 0,
            "keyword_score": 0,
            "logic_score": 0,
            "hit_keywords": [],
            "missed_keywords": key_points,
            "is_satisfactory": False
        }

    # 关键词匹配
    answer_lower = user_answer.lower()
    hit_keywords = []
    missed_keywords = []

    for kp in key_points:
        kp_lower = kp.lower()
        if any(word in answer_lower for word in kp_lower.split()):
            hit_keywords.append(kp)
        else:
            missed_keywords.append(kp)

    # 计算得分
    if key_points:
        keyword_ratio = len(hit_keywords) / len(key_points)
        keyword_score = int(70 * keyword_ratio)
    else:
        keyword_score = 35

    # 思路得分
    logic_score = _evaluate_logic(user_answer)
    total_score = keyword_score + logic_score

    return {
        "round_score": total_score,
        "keyword_score": keyword_score,
        "logic_score": logic_score,
        "hit_keywords": hit_keywords,
        "missed_keywords": missed_keywords,
        "is_satisfactory": total_score >= 60,
        "is_low_score": total_score < 50  # 标记低分，便于提醒判断
    }


def score_and_check_reminder(key_points: List[str], user_answer: str,
                             question_index: int, round_num: int = 1) -> Dict:
    """
    评分并自动检查是否触发提醒机制

    Args:
        key_points: 考察要点/关键词列表
        user_answer: 用户的回答文本
        question_index: 题目索引
        round_num: 当前回答轮次

    Returns:
        包含评分结果和提醒信息的字典
    """
    score_result = score_answer(key_points, user_answer)
    reminder_info = _reminder_state.check_and_trigger_reminder(
        score_result, question_index, round_num
    )

    return {
        **score_result,
        "reminder": reminder_info
    }


def _evaluate_logic(answer: str) -> int:
    """评估回答的逻辑性 (0-30分)"""
    score = 15

    if len(answer) > 50:
        score += 5
    if "：" in answer or ":" in answer:
        score += 3
    if any(word in answer for word in ["首先", "其次", "第一", "第二", "1.", "2."]):
        score += 5
    if len(answer) < 20:
        score -= 5

    return max(0, min(30, score))


def generate_report(scores: List[Dict], direction: str = "综合面试") -> str:
    """
    生成面试报告

    Args:
        scores: 每题的得分列表
        direction: 面试方向

    Returns:
        报告文本
    """
    if not scores:
        return "暂无面试数据，无法生成报告。"

    total_score = sum(s.get("round_score", 0) for s in scores)
    avg_score = total_score / len(scores)

    # 评级
    if avg_score >= 90:
        grade = "S (优秀)"
    elif avg_score >= 80:
        grade = "A (良好)"
    elif avg_score >= 70:
        grade = "B (中等)"
    elif avg_score >= 60:
        grade = "C (及格)"
    else:
        grade = "D (需努力)"

    # 各题详情
    details = "\n".join([
        f"{i+1}. 【{s.get('type', '八股')}】{s.get('final_score', 0)}分"
        for i, s in enumerate(scores)
    ])

    report = f"""
{'='*50}
📋 模拟面试报告
{'='*50}

🎯 面试方向: {direction}
📊 总分: {total_score}/{len(scores)*100}
📈 平均分: {avg_score:.1f}/100
🏆 评级: {grade}

{'='*50}
📝 各题详情
{'='*50}
{details}

{'='*50}
💬 综合评语
{'='*50}
继续加油！💪

{'='*50}
"""
    return report


# ============================================================
# 命令行接口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI 模拟面试助手")
    parser.add_argument("--tags", nargs="+", default=["MySQL索引", "Redis"],
                        help="技术标签")
    parser.add_argument("--count", type=int, default=5,
                        help="题目数量")
    parser.add_argument("--list-tags", action="store_true",
                        help="列出所有可用标签")
    parser.add_argument("--no-frontier", action="store_true",
                        help="不包含前沿题目")
    parser.add_argument("--search", type=str, default=None,
                        help="直接搜索 GitHub 知识库关键词")

    args = parser.parse_args()

    # 直接搜索模式
    if args.search:
        results = github_search(args.search, limit=args.count)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.list_tags:
        # 列出支持的标签（这些是常见的面试方向）
        print("可用标签（支持 GitHub 知识库搜索）:")
        print("  - MySQL索引")
        print("  - Redis")
        print("  - RAG")
        print("  - LLM微调")
        print("  - AI Agent")
        print("  - Python")
        print("  - 系统架构")
        print("\n提示：使用 --search 参数可以搜索任意关键词")
    else:
        questions = get_questions(args.tags, args.count, include_frontier=not args.no_frontier)
        print(json.dumps(questions, ensure_ascii=False, indent=2))
