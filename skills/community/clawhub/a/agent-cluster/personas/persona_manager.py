"""
人设管理器 / Persona Manager

核心能力：
1. 动态人设切换：根据用户 query 自动匹配合适的 Agent 人设
2. 上下文注入：将人设注入到 system prompt
3. 多人设协同：支持主Agent（幕僚长）+ 专业Agent的多人设协作
4. 人设状态追踪：记录当前激活的人设、人设切换历史

对标 QClaw V2 人设系统的运行时注入能力。
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from personas.base import AgentPersona, PersonaType
from personas.chiefofstaff import CHIEF_OF_STAFF
from personas.geo_analyst import GEO_ANALYST
from personas.amazon_operator import AMAZON_OPERATOR
from personas.content_creator import CONTENT_CREATOR

logger = logging.getLogger(__name__)


@dataclass
class PersonaSwitchRecord:
    """人设切换记录"""
    timestamp: str
    from_persona: str
    to_persona: str
    trigger_query: str
    confidence: float


@dataclass
class PersonaContext:
    """
    运行时人设上下文。
    包含当前激活的人设栈（支持嵌套/临时切换），
    以及切换历史。
    """
    primary: AgentPersona
    stack: List[PersonaType] = field(default_factory=list)
    history: List[PersonaSwitchRecord] = field(default_factory=list)

    def active(self) -> AgentPersona:
        """返回当前激活的人设（栈顶优先）"""
        if self.stack:
            return REGISTRY.get(self.stack[-1])
        return self.primary

    def push(self, persona_type: PersonaType) -> None:
        """临时压入一个人设（用于嵌套任务）"""
        if not self.stack or self.stack[-1] != persona_type:
            self.stack.append(persona_type)
            logger.info(f"[PersonaContext] Push: {persona_type.value}")

    def pop(self) -> Optional[PersonaType]:
        """弹出栈顶人设，返回被弹出的人设类型"""
        if self.stack:
            popped = self.stack.pop()
            logger.info(f"[PersonaContext] Pop: {popped.value}")
            return popped
        return None


class PersonaRegistry:
    """
    人设注册表。
    管理所有已注册的人设，支持类型/名称检索。
    """

    def __init__(self) -> None:
        self._registry: Dict[PersonaType, AgentPersona] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        """注册默认人设集"""
        defaults = [
            CHIEF_OF_STAFF,
            GEO_ANALYST,
            AMAZON_OPERATOR,
            CONTENT_CREATOR,
        ]
        for persona in defaults:
            self.register(persona)

    def register(self, persona: AgentPersona) -> None:
        """注册一个人设"""
        self._registry[persona.persona_type] = persona
        logger.debug(f"[Registry] Registered: {persona.name} ({persona.persona_type.value})")

    def get(self, persona_type: PersonaType) -> AgentPersona:
        """根据类型获取人设"""
        persona = self._registry.get(persona_type)
        if persona is None:
            logger.warning(f"[Registry] Unknown type {persona_type.value}, fallback to CHIEF_OF_STAFF")
            return CHIEF_OF_STAFF
        return persona

    def get_by_name(self, name: str) -> Optional[AgentPersona]:
        """根据名称模糊匹配人设"""
        q = name.lower().strip()
        for persona in self._registry.values():
            if q in persona.name.lower() or q in persona.persona_type.value:
                return persona
        return None

    def list_all(self) -> List[AgentPersona]:
        """列出所有已注册人设"""
        return list(self._registry.values())

    def match(self, query: str, top_k: int = 2) -> List[Tuple[AgentPersona, float]]:
        """
        根据用户 query 匹配最合适的人设列表。
        返回 (persona, score) 列表，按 score 降序排列。
        """
        scored = [
            (persona, persona.matches_query(query))
            for persona in self._registry.values()
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def export_json(self) -> str:
        """导出所有注册人设为 JSON（不含 system_hints 敏感内容）"""
        safe_data = {
            p.persona_type.value: {
                "name": p.name,
                "expertise": p.expertise,
                "personality": p.personality,
            }
            for p in self._registry.values()
        }
        return json.dumps(safe_data, ensure_ascii=False, indent=2)


class PersonaManager:
    """
    人设管理器核心类。

    提供：
    - resolve(query): 根据 query 自动匹配合适的人设
    - activate(persona_type): 激活指定人设（同时记录历史）
    - get_system_prompt(): 获取当前人设对应的 system prompt
    - reset(): 重置为默认人设（幕僚长）
    - get_context(): 获取当前人设上下文
    """

    def __init__(self) -> None:
        self.registry = PersonaRegistry()
        self._context_stack: List[PersonaContext] = []
        # 默认激活幕僚长人设
        self._context_stack.append(
            PersonaContext(primary=CHIEF_OF_STAFF)
        )

    # ── 核心 API ────────────────────────────────────────────────

    def resolve(self, query: str) -> AgentPersona:
        """
        根据 query 自动解析并匹配合适的人设。
        如果最高匹配度低于阈值（0.2），保持当前人设。
        """
        matches = self.registry.match(query, top_k=1)
        if not matches:
            return self.active()

        best_persona, score = matches[0]
        current = self.active()

        if score >= 0.2 and best_persona.persona_type != current.persona_type:
            self._record_switch(current, best_persona, query, score)
            # 自动解析时同步更新 primary
            self._context_stack[-1].primary = best_persona
            logger.info(
                f"[PersonaManager] Auto-resolved to {best_persona.name} "
                f"(score={score:.2f}) for query: {query[:50]}..."
            )

        return best_persona

    def activate(
        self,
        persona_type: Optional[PersonaType] = None,
        persona_name: Optional[str] = None,
    ) -> AgentPersona:
        """
        手动激活指定人设。

        Args:
            persona_type: 通过枚举类型指定
            persona_name: 通过名称模糊匹配指定

        Returns:
            被激活的人设实例
        """
        if persona_type:
            persona = self.registry.get(persona_type)
        elif persona_name:
            persona = self.registry.get_by_name(persona_name)
            if persona is None:
                logger.warning(f"[PersonaManager] Name '{persona_name}' not found, keep current")
                return self.active()
        else:
            return self.active()

        current = self.active()
        if persona.persona_type != current.persona_type:
            self._record_switch(current, persona, "[manual]", 1.0)
            # 更新 primary，使人设真正生效
            self._context_stack[-1].primary = persona

        return persona

    def push_persona(self, persona_type: PersonaType) -> None:
        """
        临时压入人设（用于嵌套任务）。
        执行完成后需调用 pop_persona() 恢复。
        """
        ctx = self._context_stack[-1]
        ctx.push(persona_type)

    def pop_persona(self) -> Optional[PersonaType]:
        """弹出临时人设，恢复上一级人设"""
        ctx = self._context_stack[-1]
        return ctx.pop()

    def get_system_prompt(
        self,
        extra_instructions: Optional[List[str]] = None,
    ) -> str:
        """
        获取当前激活人设的完整 system prompt。
        可额外注入指令列表。
        """
        persona = self.active()
        prompt_parts = [persona.to_system_prompt()]

        if extra_instructions:
            prompt_parts.append("\n【额外指令】")
            prompt_parts.extend(f"- {inst}" for inst in extra_instructions)

        return "\n".join(prompt_parts)

    def get_user_intro(self) -> str:
        """获取当前人设的用户自我介绍"""
        return self.active().to_user_intro()

    def reset(self) -> None:
        """重置为默认人设（幕僚长）"""
        self._context_stack.clear()
        self._context_stack.append(PersonaContext(primary=CHIEF_OF_STAFF))
        logger.info("[PersonaManager] Reset to CHIEF_OF_STAFF")

    def active(self) -> AgentPersona:
        """获取当前激活的人设"""
        if self._context_stack:
            return self._context_stack[-1].active()
        return CHIEF_OF_STAFF

    def active_type(self) -> PersonaType:
        """获取当前激活的人设类型"""
        return self.active().persona_type

    def get_history(self) -> List[PersonaSwitchRecord]:
        """获取人设切换历史"""
        if self._context_stack:
            return self._context_stack[-1].history
        return []

    def get_registry_summary(self) -> str:
        """获取注册表摘要（调试用）"""
        return self.registry.export_json()

    # ── 内部方法 ───────────────────────────────────────────────

    def _record_switch(
        self,
        from_persona: AgentPersona,
        to_persona: AgentPersona,
        query: str,
        confidence: float,
    ) -> None:
        """记录一次人设切换"""
        record = PersonaSwitchRecord(
            timestamp=datetime.now().isoformat(),
            from_persona=from_persona.name,
            to_persona=to_persona.name,
            trigger_query=query[:100],
            confidence=confidence,
        )
        if self._context_stack:
            self._context_stack[-1].history.append(record)


# ── 全局单例 ────────────────────────────────────────────────────────────────

# Registry 仅初始化一次（无状态，可复用）
REGISTRY = PersonaRegistry()

# Manager 实例（带状态，建议在 Agent 生命周期内复用）
_manager: Optional[PersonaManager] = None


def get_manager() -> PersonaManager:
    """获取全局 PersonaManager 单例"""
    global _manager
    if _manager is None:
        _manager = PersonaManager()
    return _manager


def reset_manager() -> None:
    """重置全局 Manager（仅在测试/重启时使用）"""
    global _manager
    _manager = None
