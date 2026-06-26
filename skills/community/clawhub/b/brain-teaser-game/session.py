#!/usr/bin/env python3
"""
会话管理模块
管理游戏会话状态和历史记录
"""

import json
import os
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional, Set, List, Dict, Any
from pathlib import Path


# 数据存储目录
CACHE_DIR = Path.home() / ".cache" / "brain-teaser"
SESSIONS_DIR = CACHE_DIR / "sessions"
HISTORY_FILE = CACHE_DIR / "history.json"

# 历史记录最大条数
MAX_HISTORY_SIZE = 1000


@dataclass
class Question:
    """题目数据结构"""
    id: int
    question: str
    answer: str
    hint: str
    explain: str
    difficulty: int = 1
    source: str = "builtin"  # builtin 或 ai_generated


@dataclass
class Session:
    """游戏会话"""
    session_id: str
    language: str
    current_question: Optional[Question] = None
    hints_shown: int = 0
    questions_answered: int = 0
    correct_answers: int = 0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        if self.current_question:
            data['current_question'] = asdict(self.current_question)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        """从字典创建"""
        if data.get('current_question'):
            data['current_question'] = Question(**data['current_question'])
        return cls(**data)


class SessionManager:
    """会话管理器"""

    def __init__(self):
        self._ensure_dirs()

    def _ensure_dirs(self):
        """确保目录存在"""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    def create_session(self, language: str) -> Session:
        """
        创建新会话

        Args:
            language: 语言代码

        Returns:
            新会话对象
        """
        session_id = str(uuid.uuid4())[:8]
        session = Session(
            session_id=session_id,
            language=language
        )
        self._save_session(session)
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """
        获取会话

        Args:
            session_id: 会话ID

        Returns:
            会话对象或 None
        """
        session_file = SESSIONS_DIR / f"{session_id}.json"
        if not session_file.exists():
            return None

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Session.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return None

    def update_session(self, session: Session) -> None:
        """
        更新会话

        Args:
            session: 会话对象
        """
        session.updated_at = time.time()
        self._save_session(session)

    def _save_session(self, session: Session) -> None:
        """保存会话到文件"""
        session_file = SESSIONS_DIR / f"{session.session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)

    def delete_session(self, session_id: str) -> None:
        """删除会话"""
        session_file = SESSIONS_DIR / f"{session_id}.json"
        if session_file.exists():
            session_file.unlink()

    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """
        清理过期会话

        Args:
            max_age_hours: 最大保留时间（小时）

        Returns:
            清理的会话数量
        """
        cleaned = 0
        cutoff = time.time() - (max_age_hours * 3600)

        for session_file in SESSIONS_DIR.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if data.get('updated_at', 0) < cutoff:
                    session_file.unlink()
                    cleaned += 1
            except (json.JSONDecodeError, KeyError):
                session_file.unlink()
                cleaned += 1

        return cleaned


class HistoryManager:
    """历史记录管理器"""

    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        """确保历史文件存在"""
        if not HISTORY_FILE.exists():
            self._save_history({"zh": {"used_ids": [], "generated": []},
                               "en": {"used_ids": [], "generated": []},
                               "ja": {"used_ids": [], "generated": []}})

    def _load_history(self) -> Dict[str, Any]:
        """加载历史记录"""
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"zh": {"used_ids": [], "generated": []},
                    "en": {"used_ids": [], "generated": []},
                    "ja": {"used_ids": [], "generated": []}}

    def _save_history(self, data: Dict[str, Any]) -> None:
        """保存历史记录"""
        data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_used_ids(self, language: str) -> Set[int]:
        """获取已使用的题目ID"""
        history = self._load_history()
        lang_data = history.get(language, {"used_ids": []})
        return set(lang_data.get("used_ids", []))

    def mark_question_used(self, question_id: int, language: str) -> None:
        """标记题目已使用"""
        history = self._load_history()
        if language not in history:
            history[language] = {"used_ids": [], "generated": []}

        used_ids = set(history[language].get("used_ids", []))
        used_ids.add(question_id)
        history[language]["used_ids"] = list(used_ids)

        # 检查是否需要清理
        total_count = sum(len(h.get("used_ids", [])) for h in history.values() if isinstance(h, dict))
        if total_count > MAX_HISTORY_SIZE:
            self._cleanup_history(history)

        self._save_history(history)

    def get_unused_questions(self, language: str, questions: List[Question]) -> List[Question]:
        """获取未使用的题目"""
        used_ids = self.get_used_ids(language)
        return [q for q in questions if q.id not in used_ids]

    def add_generated_question(self, question: Question, language: str) -> None:
        """添加 AI 生成的题目到历史"""
        history = self._load_history()
        if language not in history:
            history[language] = {"used_ids": [], "generated": []}

        if "generated" not in history[language]:
            history[language]["generated"] = []

        history[language]["generated"].append(asdict(question))
        history[language]["used_ids"].append(question.id)

        self._save_history(history)

    def get_generated_questions(self, language: str) -> List[Question]:
        """获取 AI 生成的题目"""
        history = self._load_history()
        lang_data = history.get(language, {"generated": []})
        generated = lang_data.get("generated", [])
        return [Question(**q) for q in generated]

    def reset_history(self, language: Optional[str] = None) -> None:
        """
        重置历史记录

        Args:
            language: 指定语言则只重置该语言，None 则重置全部
        """
        if language:
            history = self._load_history()
            history[language] = {"used_ids": [], "generated": []}
            self._save_history(history)
        else:
            self._save_history({
                "zh": {"used_ids": [], "generated": []},
                "en": {"used_ids": [], "generated": []},
                "ja": {"used_ids": [], "generated": []}
            })

    def _cleanup_history(self, history: Dict[str, Any]) -> None:
        """清理历史记录，保留最近的记录"""
        # 简单策略：重置所有历史
        for lang in ["zh", "en", "ja"]:
            if lang in history:
                history[lang]["used_ids"] = []
                # 保留生成的题目


if __name__ == "__main__":
    # 测试会话管理
    print("=== 会话管理测试 ===")
    sm = SessionManager()

    # 创建会话
    session = sm.create_session("zh")
    print(f"创建会话: {session.session_id}")

    # 获取会话
    loaded = sm.get_session(session.session_id)
    print(f"加载会话: {loaded.session_id if loaded else 'None'}")

    # 更新会话
    session.questions_answered = 1
    sm.update_session(session)

    # 测试历史记录
    print("\n=== 历史记录测试 ===")
    hm = HistoryManager()

    # 重置历史
    hm.reset_history("zh")

    # 标记已使用
    hm.mark_question_used(1, "zh")
    hm.mark_question_used(2, "zh")

    used = hm.get_used_ids("zh")
    print(f"已使用ID: {used}")

    # 测试未使用筛选
    questions = [Question(id=i, question=f"Q{i}", answer="A", hint="H", explain="E") for i in range(1, 6)]
    unused = hm.get_unused_questions("zh", questions)
    print(f"未使用题目ID: {[q.id for q in unused]}")
