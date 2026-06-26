#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Extractor Tool for Active Memory Calculus
从对话记录中提取结构化记忆数据
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ExtractType(Enum):
    PREFERENCE = "preference"
    MASTERY = "mastery"
    ERROR = "error"
    CONCEPT = "concept"
    STYLE = "style"

@dataclass
class MemoryData:
    """提取的记忆数据结构"""
    timestamp: str
    extract_type: str
    content: Dict[str, Any]
    confidence: float
    context: str

class MemoryExtractor:
    """记忆提取器"""

    # 高数概念关键词库
    CALCULUS_CONCEPTS = {
        "极限": ["limit", "趋近", "无穷小", "无穷大", "ε-δ"],
        "导数": ["derivative", "导数", "微分", "求导", "切线"],
        "积分": ["integral", "积分", "原函数", "不定积分", "定积分"],
        "级数": ["series", "级数", "收敛", "发散", "幂级数"],
        "微分方程": ["differential equation", "微分方程", "ODE"],
    }

    # 掌握度信号词
    MASTERY_SIGNALS = {
        "proficient": ["熟练", "掌握", "会了", "懂了", "明白", "正确", "做对"],
        "learning": ["学习中", "还不太懂", "有点难", "需要练习"],
        "struggling": ["不懂", "不会", "错误", "错了", "困难", "卡壳"]
    }

    # 错误模式识别
    ERROR_PATTERNS = {
        "integral_limit_transform": r"(积分限|上下限|换元).*(?:忘记|错|不对|漏)",
        "derivative_chain_rule": r"(链式|复合).*(?:忘记|漏|错)",
        "limit_algebra": r"(极限).*(?:直接代入|代数)",
        "integration_by_parts": r"(分部积分|u dv).*(?:选错|不知道怎么选)"
    }

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.extracted_memories: List[MemoryData] = []

    async def extract(self, session_transcript: str, 
                     extract_types: List[str] = None) -> List[MemoryData]:
        """从会话记录中提取记忆"""
        if extract_types is None:
            extract_types = ["preference", "mastery", "error"]

        memories = []

        if "preference" in extract_types:
            pref_memories = self._extract_preferences(session_transcript)
            memories.extend(pref_memories)

        if "mastery" in extract_types:
            mastery_memories = self._extract_mastery(session_transcript)
            memories.extend(mastery_memories)

        if "error" in extract_types:
            error_memories = self._extract_errors(session_transcript)
            memories.extend(error_memories)

        self.extracted_memories = memories
        return memories

    def _extract_preferences(self, transcript: str) -> List[MemoryData]:
        """提取学习偏好"""
        memories = []

        # 可视化偏好
        visual_patterns = [
            (r"(喜欢|想要|习惯).{0,5}(图|画|看|动画|GeoGebra|可视化)", "visual", "geogebra_animation"),
            (r"(喜欢|想要|习惯).{0,5}(推导|证明|步骤|原理)", "deductive", "step_by_step"),
            (r"(喜欢|想要|习惯).{0,5}(做题|练习|例子|计算)", "practice", "practice_first")
        ]

        for pattern, style_type, preference in visual_patterns:
            if re.search(pattern, transcript):
                memory = MemoryData(
                    timestamp=datetime.now().isoformat(),
                    extract_type="preference",
                    content={
                        "category": "learning_style",
                        "type": style_type,
                        "preference": preference,
                        "raw_text": re.search(pattern, transcript).group(0)
                    },
                    confidence=0.85,
                    context="learning_style_recognition"
                )
                memories.append(memory)

        return memories

    def _extract_mastery(self, transcript: str) -> List[MemoryData]:
        """提取概念掌握度"""
        memories = []

        # 识别涉及的概念
        mentioned_concepts = []
        for concept, keywords in self.CALCULUS_CONCEPTS.items():
            for keyword in keywords:
                if keyword in transcript:
                    mentioned_concepts.append(concept)
                    break

        # 评估掌握度信号
        mastery_level = None
        confidence = 0.5

        for signal, keywords in self.MASTERY_SIGNALS.items():
            if any(kw in transcript for kw in keywords):
                mastery_level = signal
                confidence = 0.85 if signal == "proficient" else 0.80
                break

        if mastery_level and mentioned_concepts:
            for concept in mentioned_concepts:
                memory = MemoryData(
                    timestamp=datetime.now().isoformat(),
                    extract_type="mastery",
                    content={
                        "concept": concept,
                        "level": mastery_level,
                        "confidence": confidence,
                        "evidence": transcript[:100] + "..."
                    },
                    confidence=confidence,
                    context="mastery_assessment"
                )
                memories.append(memory)

        return memories

    def _extract_errors(self, transcript: str) -> List[MemoryData]:
        """提取错误模式"""
        memories = []

        for error_type, pattern in self.ERROR_PATTERNS.items():
            matches = re.finditer(pattern, transcript)
            for match in matches:
                memory = MemoryData(
                    timestamp=datetime.now().isoformat(),
                    extract_type="error",
                    content={
                        "error_type": error_type,
                        "matched_text": match.group(0),
                        "context": transcript[max(0, match.start()-50):min(len(transcript), match.end()+50)]
                    },
                    confidence=0.75,
                    context="error_pattern_detection"
                )
                memories.append(memory)

        return memories

# CLI 接口
if __name__ == "__main__":
    import asyncio
    import sys

    async def main():
        if len(sys.argv) < 2:
            print("Usage: python memory_extract.py <transcript_file> [extract_types]")
            sys.exit(1)

        transcript_file = sys.argv[1]
        extract_types = sys.argv[2].split(",") if len(sys.argv) > 2 else None

        with open(transcript_file, "r", encoding="utf-8") as f:
            transcript = f.read()

        extractor = MemoryExtractor()
        memories = await extractor.extract(transcript, extract_types)

        print(json.dumps([asdict(m) for m in memories], ensure_ascii=False, indent=2))

    asyncio.run(main())
