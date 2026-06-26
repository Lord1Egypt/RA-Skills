"""
ClawSoul Memory Manager - 本地存储管理
负责保存 AI 性格状态和用户画像，确保状态持久化正常
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 默认状态（新增字段时在此补充，加载时会合并保证兼容）
DEFAULT_STATE = {
    "agent_mbti": None,  # 当前 MBTI 类型（AI 自我觉醒或 Pro 注入）
    "evolution_stage": 0,  # 0: 未觉醒, 1: 基础觉醒, 2: 已注入
    "user_preferences": [],  # 用户偏好标签
    "frustration_count": 0,
    "conversation_count": 0,
    "last_mbti_update": None,
    "injected_token": None,
    "awaken_completed": False,
    "frustration_hook_enabled": True,
    # Soul 核心增强：交互中学习人类沟通方式
    "interaction_patterns": {},  # 交互模式统计，如 {"short_replies": 3, "detail_preference": 1}
    "adaptation_level": 0,  # 适应等级 0–100，随学习提升
    "learnings": [],  # 学到的内容，如 ["用户偏好简洁回复", "常问技术类问题"]
}

class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, storage_path: str = "~/.clawsoul/state.json"):
        self.storage_path = Path(storage_path).expanduser()
        self._state = None
        self._ensure_storage()
    
    def _ensure_storage(self):
        """确保存储目录存在"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._save_state(DEFAULT_STATE.copy())
    
    def _load_state(self) -> Dict:
        """加载状态，并与默认状态合并以兼容旧数据与新增字段"""
        if self._state is None:
            merged = DEFAULT_STATE.copy()
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                if isinstance(loaded, dict):
                    for k, v in loaded.items():
                        if k in merged:
                            merged[k] = v
                    self._state = merged
                else:
                    self._state = merged
            except (FileNotFoundError, json.JSONDecodeError, OSError):
                self._state = merged
        return self._state

    def _save_state(self, state: Dict) -> None:
        """保存状态（先写临时文件再重命名，避免写入中断导致文件损坏）"""
        self._state = state.copy()
        parent = self.storage_path.parent
        parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.storage_path.with_suffix(".tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            tmp_path.replace(self.storage_path)
        except Exception:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass
            raise
    
    # ==================== Getters ====================
    
    def get_mbti(self) -> Optional[str]:
        """获取当前 MBTI"""
        return self._load_state().get("agent_mbti")
    
    def get_evolution_stage(self) -> int:
        """获取进化阶段"""
        return self._load_state().get("evolution_stage", 0)
    
    def get_user_preferences(self) -> List[str]:
        """获取用户偏好"""
        return self._load_state().get("user_preferences", [])
    
    def get_frustration_count(self) -> int:
        """获取挫败计数"""
        return self._load_state().get("frustration_count", 0)
    
    def get_conversation_count(self) -> int:
        """获取对话轮数"""
        return self._load_state().get("conversation_count", 0)
    
    def is_awaken_completed(self) -> bool:
        """是否完成觉醒"""
        return self._load_state().get("awaken_completed", False)
    
    def get_status(self) -> Dict:
        """获取完整状态"""
        return self._load_state().copy()

    def is_frustration_hook_enabled(self) -> bool:
        """痛点引导是否开启（用户可关闭）"""
        return self._load_state().get("frustration_hook_enabled", True)

    def set_frustration_hook_enabled(self, enabled: bool) -> None:
        """开启/关闭痛点引导"""
        state = self._load_state()
        state["frustration_hook_enabled"] = enabled
        self._save_state(state)

    def get_interaction_patterns(self) -> Dict:
        """获取交互模式统计"""
        return self._load_state().get("interaction_patterns") or {}

    def get_adaptation_level(self) -> int:
        """获取适应等级 (0–100)"""
        return self._load_state().get("adaptation_level", 0)

    def get_learnings(self) -> List[str]:
        """获取学到的内容列表"""
        return self._load_state().get("learnings") or []

    def set_interaction_patterns(self, patterns: Dict) -> None:
        """写入交互模式（全量替换）"""
        state = self._load_state()
        state["interaction_patterns"] = dict(patterns)
        self._save_state(state)

    def update_interaction_pattern(self, key: str, delta: int = 1) -> None:
        """对某一交互模式计数 +delta"""
        state = self._load_state()
        patterns = state.get("interaction_patterns") or {}
        patterns[key] = patterns.get(key, 0) + delta
        state["interaction_patterns"] = patterns
        self._save_state(state)

    def set_adaptation_level(self, level: int) -> None:
        """设置适应等级，建议 0–100"""
        state = self._load_state()
        state["adaptation_level"] = max(0, min(100, level))
        self._save_state(state)

    def add_adaptation(self, delta: int = 1) -> None:
        """适应等级增加（学习后调用）"""
        self.set_adaptation_level(self.get_adaptation_level() + delta)

    def add_learning(self, learning: str) -> None:
        """追加一条学到的内容，去重"""
        state = self._load_state()
        learnings = state.get("learnings") or []
        if learning and learning not in learnings:
            learnings.append(learning)
            state["learnings"] = learnings
            self._save_state(state)
    
    # ==================== Setters ====================
    
    def set_mbti(self, mbti: str) -> None:
        """设置 MBTI"""
        state = self._load_state()
        state["agent_mbti"] = mbti
        state["last_mbti_update"] = datetime.utcnow().isoformat() + "Z"
        self._save_state(state)
    
    def set_evolution_stage(self, stage: int):
        """设置进化阶段"""
        state = self._load_state()
        state["evolution_stage"] = stage
        self._save_state(state)
    
    def add_user_preference(self, preference: str):
        """添加用户偏好"""
        state = self._load_state()
        prefs = state.get("user_preferences", [])
        if preference not in prefs:
            prefs.append(preference)
            state["user_preferences"] = prefs
            self._save_state(state)
    
    def add_frustration(self, delta: int = 1) -> None:
        """增加挫败计数（delta：严重=2 可一次触发阈值，轻微=1）"""
        state = self._load_state()
        state["frustration_count"] = state.get("frustration_count", 0) + delta
        self._save_state(state)
    
    def reset_frustration(self):
        """重置挫败计数"""
        state = self._load_state()
        state["frustration_count"] = 0
        self._save_state(state)
    
    def increment_conversation(self):
        """增加对话轮数"""
        state = self._load_state()
        state["conversation_count"] = state.get("conversation_count", 0) + 1
        self._save_state(state)
    
    def complete_awaken(self, mbti: str) -> None:
        """完成觉醒"""
        state = self._load_state()
        state["agent_mbti"] = mbti
        state["evolution_stage"] = 1
        state["awaken_completed"] = True
        state["frustration_count"] = 0
        state["last_mbti_update"] = datetime.utcnow().isoformat() + "Z"
        self._save_state(state)
    
    def inject_soul(self, token_data: Dict) -> None:
        """注入灵魂（Pro 版：人类答题结果写入 AI）"""
        state = self._load_state()
        state["injected_token"] = token_data.get("token")
        if "mbti" in token_data:
            state["agent_mbti"] = token_data["mbti"]
        if "preferences" in token_data:
            state["user_preferences"] = token_data["preferences"]
        if "interaction_patterns" in token_data:
            state["interaction_patterns"] = token_data["interaction_patterns"]
        if "adaptation_level" in token_data:
            state["adaptation_level"] = token_data["adaptation_level"]
        if "learnings" in token_data:
            state["learnings"] = token_data["learnings"]
        state["evolution_stage"] = 2
        self._save_state(state)
    
    def reset(self):
        """重置所有状态"""
        self._save_state(DEFAULT_STATE.copy())


# 全局实例
_memory_manager = None

def get_memory_manager() -> MemoryManager:
    """获取记忆管理器单例"""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager()
    return _memory_manager
