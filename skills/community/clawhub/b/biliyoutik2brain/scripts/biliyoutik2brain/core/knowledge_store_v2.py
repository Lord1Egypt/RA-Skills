"""
BiliYouTik2Brain — 双层知识存储 (v4.0)

两层知识体系：
  - UP 主层：个人知识（口头禅、术语偏好、纠错词典、说话风格）
  - 领域层：跨 UP 主共享知识（领域术语、常见概念、知识图谱、错误模式）

两层独立存储，可交叉引用。
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════
#  数据模型
# ═══════════════════════════════════════════════════════════

@dataclass
class SpeakerKnowledge:
    """UP 主个人知识"""
    speaker_id: str
    name: str
    platforms: List[str] = field(default_factory=list)
    video_count: int = 0
    total_duration_min: float = 0.0

    # 说话特征
    catchphrases: List[str] = field(default_factory=list)    # 口头禅
    preferred_terms: List[str] = field(default_factory=list)  # 常用术语
    speaking_style: str = ""                                  # 说话风格描述

    # 纠错词典（该 UP 主专属）
    corrections: Dict[str, str] = field(default_factory=dict)

    # 视频历史
    videos: List[Dict] = field(default_factory=list)

    # 元信息
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> Dict:
        return {
            "speaker_id": self.speaker_id,
            "name": self.name,
            "platforms": self.platforms,
            "video_count": self.video_count,
            "total_duration_min": self.total_duration_min,
            "catchphrases": self.catchphrases,
            "preferred_terms": self.preferred_terms,
            "speaking_style": self.speaking_style,
            "corrections": self.corrections,
            "videos": self.videos[-20:],  # 只保留最近 20 条
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class DomainKnowledge:
    """领域共享知识"""
    domain_id: str  # 如 "trading", "tech", "education"
    name: str

    # 领域术语
    terms: List[Dict] = field(default_factory=list)  # [{term, description, frequency}]

    # 常见概念
    concepts: List[Dict] = field(default_factory=list)  # [{concept, description, related_terms}]

    # 错误模式（该领域常见的转录错误）
    error_patterns: List[Dict] = field(default_factory=list)  # [{wrong, correct, context}]

    # 贡献者（哪些 UP 主贡献了知识）
    contributors: List[str] = field(default_factory=list)

    # 元信息
    created_at: str = ""
    updated_at: str = ""
    video_count: int = 0

    def to_dict(self) -> Dict:
        return {
            "domain_id": self.domain_id,
            "name": self.name,
            "terms": self.terms[:50],  # 最多 50 个术语
            "concepts": self.concepts[:30],
            "error_patterns": self.error_patterns[:30],
            "contributors": self.contributors,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "video_count": self.video_count,
        }


# ═══════════════════════════════════════════════════════════
#  存储路径
# ═══════════════════════════════════════════════════════════

_KNOWLEDGE_BASE = os.path.expanduser("~/.biliyoutik2brain/knowledge")
_SPEAKERS_DIR = os.path.join(_KNOWLEDGE_BASE, "speakers")
_DOMAINS_DIR = os.path.join(_KNOWLEDGE_BASE, "domains")

os.makedirs(_SPEAKERS_DIR, exist_ok=True)
os.makedirs(_DOMAINS_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════
#  UP 主层操作
# ═══════════════════════════════════════════════════════════

def get_speaker_knowledge(speaker_id: str) -> Optional[SpeakerKnowledge]:
    """获取 UP 主知识"""
    path = os.path.join(_SPEAKERS_DIR, f"{speaker_id}.json")
    if not os.path.exists(path):
        return None

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return SpeakerKnowledge(**data)


def save_speaker_knowledge(knowledge: SpeakerKnowledge):
    """保存 UP 主知识"""
    knowledge.updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
    if not knowledge.created_at:
        knowledge.created_at = knowledge.updated_at

    path = os.path.join(_SPEAKERS_DIR, f"{knowledge.speaker_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(knowledge.to_dict(), f, ensure_ascii=False, indent=2)


def update_speaker_after_video(
    speaker_id: str,
    name: str,
    platform: str,
    video_title: str,
    video_id: str,
    duration_min: float,
    analysis: Dict,
    corrections: List[Dict] = None,
):
    """处理完一个视频后更新 UP 主知识"""
    knowledge = get_speaker_knowledge(speaker_id)
    if not knowledge:
        knowledge = SpeakerKnowledge(
            speaker_id=speaker_id,
            name=name,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

    knowledge.name = name
    if platform and platform not in knowledge.platforms:
        knowledge.platforms.append(platform)
    knowledge.video_count += 1
    knowledge.total_duration_min += duration_min

    # 记录视频
    knowledge.videos.append({
        "title": video_title,
        "video_id": video_id,
        "platform": platform,
        "duration_min": duration_min,
        "processed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    })

    # 从分析中提取术语和口头禅
    if analysis:
        keywords = analysis.get("keywords", [])
        for kw in keywords:
            if kw not in knowledge.preferred_terms:
                knowledge.preferred_terms.append(kw)

    # 从纠错中学习
    if corrections:
        for corr in corrections:
            wrong = corr.get("wrong", "")
            correct = corr.get("correct", "")
            if wrong and correct and wrong not in knowledge.corrections:
                knowledge.corrections[wrong] = correct

    save_speaker_knowledge(knowledge)


# ═══════════════════════════════════════════════════════════
#  领域层操作
# ═══════════════════════════════════════════════════════════

def get_domain_knowledge(domain_id: str) -> Optional[DomainKnowledge]:
    """获取领域知识"""
    path = os.path.join(_DOMAINS_DIR, f"{domain_id}.json")
    if not os.path.exists(path):
        return None

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return DomainKnowledge(**data)


def save_domain_knowledge(knowledge: DomainKnowledge):
    """保存领域知识"""
    knowledge.updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
    if not knowledge.created_at:
        knowledge.created_at = knowledge.updated_at

    path = os.path.join(_DOMAINS_DIR, f"{knowledge.domain_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(knowledge.to_dict(), f, ensure_ascii=False, indent=2)


def update_domain_after_video(
    domain_id: str,
    domain_name: str,
    speaker_id: str,
    analysis: Dict,
    corrections: List[Dict] = None,
):
    """处理完一个视频后更新领域知识"""
    knowledge = get_domain_knowledge(domain_id)
    if not knowledge:
        knowledge = DomainKnowledge(
            domain_id=domain_id,
            name=domain_name,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

    knowledge.name = domain_name
    knowledge.video_count += 1

    # 添加贡献者
    if speaker_id not in knowledge.contributors:
        knowledge.contributors.append(speaker_id)

    # 提取术语
    if analysis:
        keywords = analysis.get("keywords", [])
        topics = analysis.get("topics", [])

        for kw in keywords:
            existing = [t for t in knowledge.terms if t.get("term") == kw]
            if existing:
                existing[0]["frequency"] = existing[0].get("frequency", 0) + 1
            else:
                knowledge.terms.append({"term": kw, "description": "", "frequency": 1})

        for topic in topics:
            topic_name = topic if isinstance(topic, str) else topic.get("topic", "")
            existing = [c for c in knowledge.concepts if c.get("concept") == topic_name]
            if not existing and topic_name:
                knowledge.concepts.append({
                    "concept": topic_name,
                    "description": topic.get("description", "") if isinstance(topic, dict) else "",
                    "related_terms": [],
                })

    # 学习错误模式
    if corrections:
        for corr in corrections:
            wrong = corr.get("wrong", "")
            correct = corr.get("correct", "")
            context = corr.get("context", "")
            if wrong and correct:
                existing = [e for e in knowledge.error_patterns if e.get("wrong") == wrong]
                if existing:
                    existing[0]["frequency"] = existing[0].get("frequency", 0) + 1
                else:
                    knowledge.error_patterns.append({
                        "wrong": wrong,
                        "correct": correct,
                        "context": context,
                        "frequency": 1,
                    })

    save_domain_knowledge(knowledge)


# ═══════════════════════════════════════════════════════════
#  查询接口
# ═══════════════════════════════════════════════════════════

def get_corrections_for_context(speaker_id: str, domain_id: str = "") -> Dict[str, str]:
    """获取上下文相关的纠错词典（合并 UP 主层 + 领域层）"""
    corrections = {}

    # UP 主层
    speaker = get_speaker_knowledge(speaker_id)
    if speaker:
        corrections.update(speaker.corrections)

    # 领域层
    if domain_id:
        domain = get_domain_knowledge(domain_id)
        if domain:
            for pattern in domain.error_patterns:
                if pattern.get("frequency", 0) >= 2:  # 至少出现 2 次才加入
                    corrections[pattern["wrong"]] = pattern["correct"]

    return corrections


def list_speakers() -> List[Dict]:
    """列出所有 UP 主"""
    speakers = []
    for f in os.listdir(_SPEAKERS_DIR):
        if f.endswith(".json"):
            path = os.path.join(_SPEAKERS_DIR, f)
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
                speakers.append({
                    "id": data.get("speaker_id", ""),
                    "name": data.get("name", ""),
                    "video_count": data.get("video_count", 0),
                    "platforms": data.get("platforms", []),
                })
    return sorted(speakers, key=lambda s: s["video_count"], reverse=True)


def list_domains() -> List[Dict]:
    """列出所有领域"""
    domains = []
    for f in os.listdir(_DOMAINS_DIR):
        if f.endswith(".json"):
            path = os.path.join(_DOMAINS_DIR, f)
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
                domains.append({
                    "id": data.get("domain_id", ""),
                    "name": data.get("name", ""),
                    "video_count": data.get("video_count", 0),
                    "term_count": len(data.get("terms", [])),
                    "contributors": data.get("contributors", []),
                })
    return sorted(domains, key=lambda d: d["video_count"], reverse=True)
