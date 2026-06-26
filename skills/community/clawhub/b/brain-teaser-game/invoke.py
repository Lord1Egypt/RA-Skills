#!/usr/bin/env python3
"""
脑筋急转弯 Skill - 主程序入口

用法：
    python invoke.py start "来个脑筋急转弯"
    python invoke.py answer {session_id} "水"
    python invoke.py hint {session_id}
    python invoke.py reveal {session_id}
    python invoke.py next {session_id}
    python invoke.py reset-history
"""

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Optional, List

from language import detect_language, get_response_language, Language
from answer import check_answer, extract_answer
from session import Session, SessionManager, HistoryManager, Question
from ai_generator import AIQuestionGenerator


# 获取数据目录
DATA_DIR = Path(__file__).parent / "data"


def load_questions(language: str) -> List[Question]:
    """加载题库"""
    lang_file = DATA_DIR / f"{language}.json"

    if not lang_file.exists():
        # 回退到中文
        lang_file = DATA_DIR / "zh.json"

    with open(lang_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return [Question(**item) for item in data]


def get_random_question(language: str, session_manager: SessionManager, history_manager: HistoryManager) -> Optional[Question]:
    """
    获取随机题目（排除已使用的）

    Args:
        language: 语言代码
        session_manager: 会话管理器
        history_manager: 历史记录管理器

    Returns:
        题目或 None
    """
    # 加载题库
    questions = load_questions(language)

    # 获取未使用的题目
    unused = history_manager.get_unused_questions(language, questions)

    # 检查是否需要 AI 生成新题
    ai_generator = AIQuestionGenerator()
    if ai_generator.should_generate_new(len(unused), threshold=5):
        new_question = ai_generator.generate_question(language)
        if new_question:
            # 添加到历史记录
            history_manager.add_generated_question(new_question, language)
            return new_question

    # 如果没有未使用的题目，重置历史
    if not unused:
        history_manager.reset_history(language)
        unused = questions

    # 随机选择
    return random.choice(unused)


def format_response(session: Session, question: Optional[Question] = None, message: str = "", show_hint: bool = False, show_answer: bool = False) -> str:
    """
    格式化 Markdown 响应

    Args:
        session: 会话
        question: 当前题目
        message: 附加消息
        show_hint: 是否显示提示
        show_answer: 是否显示答案

    Returns:
        Markdown 格式的响应
    """
    # 语言相关的文本
    texts = {
        "zh": {
            "title": "## 🧠 脑筋急转弯",
            "question": "**题目**",
            "hint_label": "**提示**",
            "answer_label": "**答案**",
            "explain_label": "**解释**",
            "stats": "已答 {answered} 题，正确 {correct} 题",
            "actions": ["直接回答", "输入\"提示\"获取提示", "输入\"答案\"查看答案", "输入\"下一题\"换一题"],
            "session_info": "会话ID: `{session_id}`"
        },
        "en": {
            "title": "## 🧠 Brain Teaser",
            "question": "**Question**",
            "hint_label": "**Hint**",
            "answer_label": "**Answer**",
            "explain_label": "**Explanation**",
            "stats": "Answered: {answered}, Correct: {correct}",
            "actions": ["Answer directly", "Type 'hint' for a hint", "Type 'answer' to reveal", "Type 'next' for new question"],
            "session_info": "Session ID: `{session_id}`"
        },
        "ja": {
            "title": "## 🧠 なぞなぞ",
            "question": "**問題**",
            "hint_label": "**ヒント**",
            "answer_label": "**答え**",
            "explain_label": "**解説**",
            "stats": "{answered}問中{correct}問正解",
            "actions": ["直接答える", "「ヒント」と入力", "「答え」と入力", "「次」と入力"],
            "session_info": "セッションID: `{session_id}`"
        }
    }

    t = texts.get(session.language, texts["zh"])
    lines = []

    # 标题
    lines.append(t["title"])
    lines.append("")

    # 消息
    if message:
        lines.append(message)
        lines.append("")

    # 题目
    if question:
        lines.append(f"{t['question']}：{question.question}")
        lines.append("")

        # 提示
        if show_hint and question.hint:
            lines.append(f"{t['hint_label']}：{question.hint}")
            lines.append("")

        # 答案
        if show_answer:
            lines.append(f"{t['answer_label']}：{question.answer}")
            if question.explain:
                lines.append(f"{t['explain_label']}：{question.explain}")
            lines.append("")

    # 分隔线
    lines.append("---")

    # 操作提示（仅在未显示答案时）
    if not show_answer:
        actions_text = "\n".join([f"- {action}" for action in t["actions"]])
        lines.append(actions_text)

    # 统计信息
    if session.questions_answered > 0:
        stats = t["stats"].format(answered=session.questions_answered, correct=session.correct_answers)
        lines.append("")
        lines.append(f"*{stats}*")

    # 会话ID
    lines.append("")
    lines.append(t["session_info"].format(session_id=session.session_id))

    return "\n".join(lines)


def cmd_start(user_input: str) -> str:
    """
    开始新游戏

    Args:
        user_input: 用户输入

    Returns:
        Markdown 响应
    """
    # 检测语言
    language = detect_language(user_input)

    # 创建会话
    session_manager = SessionManager()
    history_manager = HistoryManager()

    session = session_manager.create_session(language)

    # 获取第一道题
    question = get_random_question(language, session_manager, history_manager)

    if not question:
        return "题库加载失败，请稍后重试。"

    # 更新会话
    session.current_question = question
    session_manager.update_session(session)

    # 标记题目已使用
    history_manager.mark_question_used(question.id, language)

    return format_response(session, question)


def cmd_answer(session_id: str, user_answer: str) -> str:
    """
    提交答案

    Args:
        session_id: 会话ID
        user_answer: 用户答案

    Returns:
        Markdown 响应
    """
    session_manager = SessionManager()
    history_manager = HistoryManager()

    session = session_manager.get_session(session_id)
    if not session:
        return "会话不存在或已过期，请重新开始游戏。"

    if not session.current_question:
        return "当前没有题目，请获取下一题。"

    # 检查答案
    is_correct, feedback = check_answer(
        user_answer,
        session.current_question.answer,
        session.language
    )

    # 更新统计
    session.questions_answered += 1
    if is_correct:
        session.correct_answers += 1

    session_manager.update_session(session)

    # 构建响应
    if is_correct:
        message = f"✅ {feedback}\n\n**{session.current_question.answer}**"
        if session.current_question.explain:
            message += f"\n\n{session.current_question.explain}"
    else:
        message = f"❌ {feedback}"

    return format_response(session, session.current_question, message, show_answer=is_correct)


def cmd_hint(session_id: str) -> str:
    """
    获取提示

    Args:
        session_id: 会话ID

    Returns:
        Markdown 响应
    """
    session_manager = SessionManager()

    session = session_manager.get_session(session_id)
    if not session:
        return "会话不存在或已过期，请重新开始游戏。"

    if not session.current_question:
        return "当前没有题目，请获取下一题。"

    # 更新提示计数
    session.hints_shown += 1
    session_manager.update_session(session)

    return format_response(session, session.current_question, show_hint=True)


def cmd_reveal(session_id: str) -> str:
    """
    查看答案

    Args:
        session_id: 会话ID

    Returns:
        Markdown 响应
    """
    session_manager = SessionManager()

    session = session_manager.get_session(session_id)
    if not session:
        return "会话不存在或已过期，请重新开始游戏。"

    if not session.current_question:
        return "当前没有题目，请获取下一题。"

    return format_response(session, session.current_question, show_answer=True)


def cmd_next(session_id: str) -> str:
    """
    下一题

    Args:
        session_id: 会话ID

    Returns:
        Markdown 响应
    """
    session_manager = SessionManager()
    history_manager = HistoryManager()

    session = session_manager.get_session(session_id)
    if not session:
        return "会话不存在或已过期，请重新开始游戏。"

    # 获取新题目
    question = get_random_question(session.language, session_manager, history_manager)

    if not question:
        return "题库加载失败，请稍后重试。"

    # 更新会话
    session.current_question = question
    session.hints_shown = 0
    session_manager.update_session(session)

    # 标记题目已使用
    history_manager.mark_question_used(question.id, session.language)

    # 语言相关的消息
    messages = {
        "zh": "📝 下一题来了！",
        "en": "📝 Here's the next one!",
        "ja": "📝 次の問題です！"
    }
    message = messages.get(session.language, messages["zh"])

    return format_response(session, question, message)


def cmd_reset_history(language: Optional[str] = None) -> str:
    """
    重置历史记录

    Args:
        language: 指定语言或 None（全部重置）

    Returns:
        响应消息
    """
    history_manager = HistoryManager()
    history_manager.reset_history(language)

    if language:
        return f"已重置 {language} 语言的历史记录，所有题目都可以重新出现了！"
    else:
        return "已重置所有历史记录，所有题目都可以重新出现了！"


def cmd_status(session_id: Optional[str] = None) -> str:
    """
    显示状态

    Args:
        session_id: 会话ID（可选）

    Returns:
        状态信息
    """
    history_manager = HistoryManager()

    lines = ["## 📊 游戏状态", ""]

    # 各语言历史记录
    for lang in ["zh", "en", "ja"]:
        used_ids = history_manager.get_used_ids(lang)
        lines.append(f"- **{lang.upper()}**: 已使用 {len(used_ids)} 题")

    # 当前会话
    if session_id:
        session_manager = SessionManager()
        session = session_manager.get_session(session_id)
        if session:
            lines.append("")
            lines.append(f"**当前会话**: `{session.session_id}`")
            lines.append(f"- 语言: {session.language}")
            lines.append(f"- 已答题数: {session.questions_answered}")
            lines.append(f"- 正确数: {session.correct_answers}")

    return "\n".join(lines)


def detect_intent(text: str, language: str) -> str:
    """
    检测用户意图

    Args:
        text: 用户输入
        language: 语言代码

    Returns:
        意图: "hint", "reveal", "next", "answer"
    """
    text_lower = text.lower().strip()

    # 中文关键词
    zh_hints = ["提示", "给个提示", "提示一下", "什么提示"]
    zh_reveal = ["答案", "查看答案", "告诉我答案", "公布答案", "是什么"]
    zh_next = ["下一题", "下一道", "换题", "换一题", "再来一题", "下一个"]

    # 英文关键词
    en_hints = ["hint", "give me a hint", "clue"]
    en_reveal = ["answer", "reveal", "show answer", "what's the answer", "solution"]
    en_next = ["next", "next question", "another", "new one"]

    # 日文关键词
    ja_hints = ["ヒント", "ヒントを", "ヒントください"]
    ja_reveal = ["答え", "正解", "答えを教えて", "答えは"]
    ja_next = ["次", "次の問題", "次の質問", "次の"]

    if language == "zh":
        if any(kw in text_lower for kw in zh_hints):
            return "hint"
        if any(kw in text_lower for kw in zh_reveal):
            return "reveal"
        if any(kw in text_lower for kw in zh_next):
            return "next"
    elif language == "en":
        if any(kw in text_lower for kw in en_hints):
            return "hint"
        if any(kw in text_lower for kw in en_reveal):
            return "reveal"
        if any(kw in text_lower for kw in en_next):
            return "next"
    elif language == "ja":
        if any(kw in text_lower for kw in ja_hints):
            return "hint"
        if any(kw in text_lower for kw in ja_reveal):
            return "reveal"
        if any(kw in text_lower for kw in ja_next):
            return "next"

    return "answer"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="脑筋急转弯 Skill")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # start 命令
    start_parser = subparsers.add_parser("start", help="开始新游戏")
    start_parser.add_argument("input", nargs="*", help="用户输入")

    # answer 命令
    answer_parser = subparsers.add_parser("answer", help="提交答案")
    answer_parser.add_argument("session_id", help="会话ID")
    answer_parser.add_argument("answer", nargs="*", help="答案")

    # hint 命令
    hint_parser = subparsers.add_parser("hint", help="获取提示")
    hint_parser.add_argument("session_id", help="会话ID")

    # reveal 命令
    reveal_parser = subparsers.add_parser("reveal", help="查看答案")
    reveal_parser.add_argument("session_id", help="会话ID")

    # next 命令
    next_parser = subparsers.add_parser("next", help="下一题")
    next_parser.add_argument("session_id", help="会话ID")

    # reset-history 命令
    reset_parser = subparsers.add_parser("reset-history", help="重置历史记录")
    reset_parser.add_argument("--lang", help="指定语言")

    # status 命令
    status_parser = subparsers.add_parser("status", help="查看状态")
    status_parser.add_argument("session_id", nargs="?", help="会话ID（可选）")

    # interactive 命令（交互模式）
    interactive_parser = subparsers.add_parser("interactive", help="交互模式")
    interactive_parser.add_argument("session_id", help="会话ID")
    interactive_parser.add_argument("input", nargs="*", help="用户输入")

    args = parser.parse_args()

    if args.command == "start":
        user_input = " ".join(args.input) if args.input else "脑筋急转弯"
        print(cmd_start(user_input))

    elif args.command == "answer":
        answer_text = " ".join(args.answer) if args.answer else ""
        print(cmd_answer(args.session_id, answer_text))

    elif args.command == "hint":
        print(cmd_hint(args.session_id))

    elif args.command == "reveal":
        print(cmd_reveal(args.session_id))

    elif args.command == "next":
        print(cmd_next(args.session_id))

    elif args.command == "reset-history":
        print(cmd_reset_history(args.lang))

    elif args.command == "status":
        print(cmd_status(args.session_id))

    elif args.command == "interactive":
        # 交互模式：自动检测意图
        session_manager = SessionManager()
        session = session_manager.get_session(args.session_id)

        if not session:
            print("会话不存在或已过期，请重新开始游戏。")
            return

        user_input = " ".join(args.input) if args.input else ""
        intent = detect_intent(user_input, session.language)

        if intent == "hint":
            print(cmd_hint(args.session_id))
        elif intent == "reveal":
            print(cmd_reveal(args.session_id))
        elif intent == "next":
            print(cmd_next(args.session_id))
        else:
            print(cmd_answer(args.session_id, user_input))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
