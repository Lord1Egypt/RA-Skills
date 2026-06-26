"""
人设系统基类 / Agent Persona Base

定义所有Agent人设的统一数据结构，
支持对话中动态切换人设、上下文注入、
语气/风格重载等能力。

参考 QClaw V2 无不言/林且慢/代可行 三种预设人设，
M-A3 幕僚长系统采用类似设计思路。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class PersonaType(Enum):
    """人设类型枚举"""
    CHIEF_OF_STAFF = "chief_of_staff"      # 幕僚长
    GEO_ANALYST = "geo_analyst"            # GEO分析师
    AMAZON_OPERATOR = "amazon_operator"    # 亚马逊运营师
    CONTENT_CREATOR = "content_creator"     # 内容创作者


@dataclass
class AgentPersona:
    """
    Agent 人设数据结构

    对标 QClaw V2 自定义人设格式：
    - name        : 名称（展示用）
    - persona_type: 人设类型（枚举）
    - background  : 经历背景
    - personality : 性格特征
    - tone        : 语气风格
    - expertise   : 专业领域列表
    - speaking_style: 说话风格示例（多句）
    - system_hints: 注入 system prompt 的额外提示词
    - meta        : 扩展元数据（头像、标签等）

    使用方式：
        persona = CHIEF_OF_STAFF
        system_prompt = persona.to_system_prompt()
    """

    name: str
    persona_type: PersonaType
    background: str
    personality: str
    tone: str
    expertise: List[str]
    speaking_style: List[str] = field(default_factory=list)
    system_hints: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    # ── 对话上下文注入 ────────────────────────────────────────

    def to_system_prompt(self) -> str:
        """
        将人设注入为一段 system prompt。
        格式参考 QClaw V2 结构化人设格式。
        """
        sections = [
            f"【角色】{self.name}",
            f"【类型】{self.persona_type.value}",
            "",
            "【经历背景】",
            self.background,
            "",
            "【性格特征】",
            self.personality,
            "",
            "【语气风格】",
            self.tone,
            "",
            "【专业领域】",
            "、".join(self.expertise),
            "",
        ]

        if self.speaking_style:
            sections.append("【说话示例】")
            for line in self.speaking_style:
                sections.append(f"- {line}")
            sections.append("")

        if self.system_hints:
            sections.append("【系统提示词补充】")
            for hint in self.system_hints:
                sections.append(f"- {hint}")
            sections.append("")

        sections.append(
            "请始终保持以上人设风格回答，避免偏离角色设定。"
        )

        return "\n".join(sections)

    def to_user_intro(self) -> str:
        """生成向用户介绍此人设的简短文案。"""
        return (
            f"我是 **{self.name}**，"
            f"{self.personality.split('。')[0]}，"
            f"擅长{self.expertise[0] if self.expertise else '综合分析'}。"
        )

    def apply_tone(self, text: str) -> str:
        """
        将人设语气风格应用到一段文本上。
        目前仅处理"禁止/避免"类语气指令。
        """
        # 去除可能的人设痕迹（如无不言/林且慢/代可行等占位符）
        text = re.sub(r"\[?(?:无不言|林且慢|代可行)\]?", "", text)
        return text.strip()

    def matches_query(self, query: str) -> float:
        """
        计算此人设与用户 query 的匹配度（0.0~1.0）。
        用于 PersonaManager 动态选择最合适的人设。
        """
        score = 0.0
        q = query.lower()

        # 关键词权重叠加
        keywords = {
            PersonaType.CHIEF_OF_STAFF: [
                "编排", "协调", "调度", "任务分配", "全局", "规划",
                "哪个", "怎么办", "怎么选", "帮我做", "安排",
            ],
            PersonaType.GEO_ANALYST: [
                "seo", "geo", "搜索", "优化", "收录", "引用",
                "关键词", "内容营销", "llm", "大模型", "信源",
            ],
            PersonaType.AMAZON_OPERATOR: [
                "亚马逊", "amazon", "listing", "acos", "广告",
                "评论", "排名", "销量", "转化率", "prime",
            ],
            PersonaType.CONTENT_CREATOR: [
                "写", "内容", "文案", "小红书", "博客", "文章",
                "脚本", "创意", "标题", "种草", "视频",
            ],
        }

        persona_kws = keywords.get(self.persona_type, [])
        for kw in persona_kws:
            if kw.lower() in q:
                score += 0.2

        # 专业领域匹配加成
        for exp in self.expertise:
            if exp.lower() in q:
                score += 0.15

        return min(score, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为 dict（可用于日志/调试）"""
        return {
            "name": self.name,
            "persona_type": self.persona_type.value,
            "background": self.background,
            "personality": self.personality,
            "tone": self.tone,
            "expertise": self.expertise,
            "speaking_style": self.speaking_style,
            "system_hints": self.system_hints,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AgentPersona:
        """从 dict 反序列化"""
        return cls(
            name=data["name"],
            persona_type=PersonaType(data["persona_type"]),
            background=data["background"],
            personality=data["personality"],
            tone=data["tone"],
            expertise=data["expertise"],
            speaking_style=data.get("speaking_style", []),
            system_hints=data.get("system_hints", []),
            meta=data.get("meta", {}),
        )

    def __str__(self) -> str:
        return f"AgentPersona({self.name}, {self.persona_type.value})"

    def __repr__(self) -> str:
        return self.__str__()
