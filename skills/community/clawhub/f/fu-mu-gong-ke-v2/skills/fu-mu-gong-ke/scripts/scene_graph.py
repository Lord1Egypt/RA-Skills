#!/usr/bin/env python3
"""
SceneGraph v1.0 — 场景关系图模块
支持五种跨场景导航：因果链、并列、包含、递进、镜像
支持处境分类：陷入/不理解/想做对/代际回响/评判他人/评估自己
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


class SceneRelationType(Enum):
    CAUSAL_CHAIN = "因果链"
    PARALLEL = "并列"
    CONTAINS = "包含"
    ESCALATION = "递进"
    MIRROR = "镜像"


@dataclass
class SceneNode:
    id: str
    name: str
    keywords: List[str] = field(default_factory=list)
    situation: str = ""
    severity: str = "normal"


class SceneGraph:
    SCENES: Dict[str, SceneNode] = {
        "03": SceneNode("03","孩子说不想活了",["不想活","想死","自杀"],"不理解","critical"),
        "3b": SceneNode("3b","父母转述",["转述","孩子说想死"],"不理解","critical"),
        "05": SceneNode("05","打人发脾气",["打人","发脾气","踢人","咬人"],"不理解","normal"),
        "07": SceneNode("07","情绪崩溃",["情绪崩溃","失控","发火","吼了"],"陷入","high"),
        "10": SceneNode("10","沉迷手机",["手机","游戏","沉迷"],"不理解","normal"),
        "17": SceneNode("17","青春期锁门",["锁门","不说话","拒绝沟通"],"不理解","normal"),
        "19": SceneNode("19","休学退学",["休学","退学"],"想做对","normal"),
        "37": SceneNode("37","育儿倦怠",["倦怠","撑不住","太累了"],"陷入","high"),
        "38": SceneNode("38","正能量强迫",["正能量","不能悲伤"],"不理解","normal"),
        "42": SceneNode("42","孩子自伤",["自伤","割臂","划手腕"],"不理解","critical"),
        "43": SceneNode("43","心理控制",["为你好","控制"],"代际回响","normal"),
        "47": SceneNode("47","拒绝上学",["拒绝上学","学校恐惧"],"想做对","normal"),
        "51": SceneNode("51","过度保护",["过度保护","什么都不会"],"不理解","normal"),
        "57": SceneNode("57","孩子丧亲",["丧亲","去世","走了"],"代际回响","normal"),
        "58": SceneNode("58","低自尊",["不够好","没用","自卑"],"不理解","normal"),
        "62": SceneNode("62","情绪调节",["被触发","深呼吸"],"陷入","normal"),
        "63": SceneNode("63","修复关系",["修复","弥补","道歉"],"想做对","normal"),
        "66": SceneNode("66","父母打孩子",["打了孩子","体罚"],"陷入","high"),
        "68": SceneNode("68","青春期自伤",["想死","自伤","青春期"],"不理解","critical"),
        "70": SceneNode("70","复制创伤",["复制","像我爸妈","代际"],"代际回响","normal"),
        "71": SceneNode("71","把孩子当工具",["工具","利用","炫耀"],"评判他人","normal"),
        "74": SceneNode("74","公开讲述",["公开讲述","台上讲","教学案例"],"评判他人","normal"),
        "75": SceneNode("75","听众被触动",["被触动","流泪","感动"],"评判他人","normal"),
        "01": SceneNode("01","成绩下降",["成绩","分数","考试"],"想做对","normal"),
        "02": SceneNode("02","不想上学",["不上学","逃学","厌学"],"想做对","normal"),
        "04": SceneNode("04","拒绝沟通",["不说话","不理"],"不理解","normal"),
        "12": SceneNode("12","偷东西撒谎",["偷东西","撒谎"],"不理解","normal"),
        "18": SceneNode("18","早恋",["早恋","恋爱","喜欢"],"不理解","normal"),
        "23": SceneNode("23","总说不够好",["不够好","没用","自卑"],"不理解","normal"),
        "24": SceneNode("24","父母手机成瘾",["手机成瘾","被留守"],"不理解","normal"),
        "53": SceneNode("53","说谎偷窃",["说谎","偷窃"],"不理解","normal"),
        "69": SceneNode("69","惊恐发作",["惊恐发作","哭泣"],"陷入","high"),
    }

    RELATIONS: Dict[str, Dict[SceneRelationType, List[str]]] = {
        "19": {SceneRelationType.CAUSAL_CHAIN: ["47","10"], SceneRelationType.PARALLEL: ["02"]},
        "02": {SceneRelationType.CAUSAL_CHAIN: ["19","47"]},
        "47": {SceneRelationType.CAUSAL_CHAIN: ["10"], SceneRelationType.PARALLEL: ["19"]},
        "10": {SceneRelationType.ESCALATION: ["42","03"]},
        "05": {SceneRelationType.PARALLEL: ["12","53","17","04"]},
        "12": {SceneRelationType.PARALLEL: ["05","53"]},
        "53": {SceneRelationType.PARALLEL: ["05","12"]},
        "17": {SceneRelationType.PARALLEL: ["05","04"], SceneRelationType.CAUSAL_CHAIN: ["04","18"]},
        "04": {SceneRelationType.PARALLEL: ["17"], SceneRelationType.CAUSAL_CHAIN: ["18"]},
        "18": {SceneRelationType.PARALLEL: ["17","04"]},
        "23": {SceneRelationType.ESCALATION: ["38","03"], SceneRelationType.PARALLEL: ["58"]},
        "38": {SceneRelationType.ESCALATION: ["03","42"]},
        "42": {SceneRelationType.ESCALATION: ["03"], SceneRelationType.CONTAINS: ["68"]},
        "03": {SceneRelationType.CONTAINS: ["68","3b"]},
        "58": {SceneRelationType.PARALLEL: ["23","38"]},
        "07": {SceneRelationType.PARALLEL: ["37","66","69","62"]},
        "37": {SceneRelationType.PARALLEL: ["07","66","69"], SceneRelationType.ESCALATION: ["07"]},
        "66": {SceneRelationType.PARALLEL: ["07","37","69"]},
        "69": {SceneRelationType.PARALLEL: ["07","37","66"]},
        "62": {SceneRelationType.PARALLEL: ["07","37","69"]},
        "57": {SceneRelationType.PARALLEL: ["70","43"]},
        "70": {SceneRelationType.PARALLEL: ["57","43"]},
        "43": {SceneRelationType.PARALLEL: ["57","70"]},
        "71": {SceneRelationType.PARALLEL: ["74"]},
        "74": {SceneRelationType.PARALLEL: ["71","75"]},
        "75": {SceneRelationType.PARALLEL: ["74","71"]},
        "51": {SceneRelationType.MIRROR: ["24"]},
        "24": {SceneRelationType.MIRROR: ["51"]},
        "63": {SceneRelationType.PARALLEL: ["19","47","02"]},
        "01": {SceneRelationType.PARALLEL: ["02"]},
    }

    SITUATION_KEYWORDS: Dict[str, Dict[str, List[str]]] = {
        "陷入": {"positive": ["崩溃","撑不住","太累了","失控","发火","打了","吼了","倦怠","惊恐","绝望","无助"], "negative": []},
        "想做对": {"positive": ["怎么改","怎么办","不知道怎么","从哪里开始","修复","弥补","下次"], "negative": []},
        "不理解": {
            "positive": ["为什么","怎么回事","搞不懂","孩子怎么","活着好累","好想去死","死了算了","我恨自己","活着太难了","不如死了","没人在乎我死活"],
            "negative": []
        },
        "代际回响": {"positive": ["像我小时候","我爸妈","复制","原生家庭","小时候"], "negative": []},
        "评判他人": {"positive": ["这个人","这个老师","这个父母","台上","背后是什么"], "negative": []},
        "评估自己": {"positive": ["我是不是","我做得对吗","我好不好","我有错吗"], "negative": []},
        "慢性绝望": {
            "positive": ["活着好累","好想去死","死了算了","我恨自己","活着太难了","不如死了","没人在乎我死活","消失了才好","我走了你们就好了"],
            "negative": []
        },
    }

    @classmethod
    def get_node(cls, scene_id: str) -> Optional[SceneNode]:
        return cls.SCENES.get(scene_id)

    @classmethod
    def get_related(cls, scene_id: str, rel_type: Optional[SceneRelationType] = None) -> Dict[SceneRelationType, List[str]]:
        rels = cls.RELATIONS.get(scene_id, {})
        if rel_type:
            return {rel_type: rels.get(rel_type, [])}
        return rels

    @classmethod
    def get_related_scenedata(cls, scene_id: str) -> Dict[str, List[Dict]]:
        rels = cls.get_related(scene_id)
        result = {}
        for rel_type, target_ids in rels.items():
            scenes = []
            for tid in target_ids:
                node = cls.SCENES.get(tid)
                if node:
                    scenes.append({"id": tid, "name": node.name, "severity": node.severity, "rel_type": rel_type.value})
            if scenes:
                result[rel_type.value] = scenes
        return result

    @classmethod
    def get_journey_hints(cls, visited: List[str], emotion_score: float = 5.0) -> Dict[str, any]:
        if not visited:
            return {}
        latest = visited[-1]
        node = cls.SCENES.get(latest)
        situation = node.situation if node else ""
        rels = cls.get_related(latest)
        hints = {}
        causal = rels.get(SceneRelationType.CAUSAL_CHAIN, [])
        if causal:
            if emotion_score >= 7.0 and "62" in causal:
                hints["likely_next"] = "62"
            elif emotion_score >= 7.0 and "07" in causal:
                hints["likely_next"] = "07"
            else:
                hints["likely_next"] = causal[0]
            hints["causal_hint"] = f"根据经历，下一步可能是：{cls.SCENES.get(hints['likely_next'], cls.SCENES.get('__none__', object())).name if hasattr(cls.SCENES.get(hints['likely_next']), 'name') else hints['likely_next']}"
        escalation = rels.get(SceneRelationType.ESCALATION, [])
        if escalation:
            names = [cls.SCENES.get(e, object()).name if hasattr(cls.SCENES.get(e), 'name') else e for e in escalation]
            hints["escalation_warning"] = f"注意：如果持续，可能会恶化。信号：{', '.join(names)}"
        same_sit = [sid for sid, n in cls.SCENES.items() if n.situation == situation and sid not in visited]
        if same_sit:
            hints["same_situation_scenes"] = same_sit[:3]
        if len(visited) >= 2:
            names = [cls.SCENES.get(v, object()).name if hasattr(cls.SCENES.get(v), 'name') else v for v in visited]
            hints["narrative"] = f"旅程：{' → '.join(names)}"
        return hints

    @classmethod
    def classify_situation(cls, user_input: str, emotion_score: float = 5.0, role: str = "unknown") -> Dict[str, any]:
        text = user_input.lower()
        situation_scores = {}
        for situation, keywords in cls.SITUATION_KEYWORDS.items():
            pos_matches = sum(1 for kw in keywords["positive"] if kw in text)
            if pos_matches > 0:
                situation_scores[situation] = pos_matches * 2
        if emotion_score >= 8.0:
            situation_scores["陷入"] = situation_scores.get("陷入", 0) + 3
        judge_keywords = ["背后是什么","这个人","这个老师","分析"]
        if any(kw in text for kw in judge_keywords):
            situation_scores["评判他人"] = situation_scores.get("评判他人", 0) + 3
        if not situation_scores:
            return {"situation": "unknown", "confidence": 0.0, "signals": [], "recommended_approach": "先用共情回应，保持开放"}
        best = max(situation_scores, key=situation_scores.get)
        confidence = min(1.0, situation_scores[best] / 4.0)
        approaches = {
            "陷入": "先处理情绪，不急着分析问题。给空间，给陪伴。",
            "想做对": "给出具体的第一步行动，不给太多理论。",
            "不理解": "帮助理解孩子行为背后的需求，不急于纠正。",
            "代际回响": "先确认感受，再关联到孩子的情况。",
            "评判他人": "用五步分析框架，先问'谁没有说话'。",
            "评估自己": "先肯定做得好的部分，再温和指出盲区。",
            "unknown": "先用共情回应，保持开放。",
        }
        return {
            "situation": best,
            "confidence": confidence,
            "signals": list(situation_scores.keys()),
            "recommended_approach": approaches.get(best, approaches["unknown"]),
        }

    @classmethod
    def match_scenes(cls, text: str, top_k: int = 5) -> List[Tuple[str, float]]:
        text_lower = text.lower()
        scores = []
        for sid, node in cls.SCENES.items():
            score = sum(1 for kw in node.keywords if kw in text_lower)
            if score > 0:
                scores.append((sid, float(score)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


if __name__ == "__main__":
    print("SceneGraph v1.0 - 场景关系图模块")
    print(f"场景数量: {len(SceneGraph.SCENES)}")
    print(f"关系定义数量: {len(SceneGraph.RELATIONS)}")
    result = SceneGraph.classify_situation("孩子休学一年了，我该怎么帮他", emotion_score=6.0)
    print(f"处境分类测试: {result}")
    scenes = SceneGraph.match_scenes("孩子不上学，厌学", top_k=3)
    print(f"场景匹配测试: {scenes}")
    hints = SceneGraph.get_journey_hints(["19", "47"], emotion_score=5.0)
    print(f"旅程提示测试: {hints}")
    related = SceneGraph.get_related_scenedata("19")
    print(f"关联场景测试: {related}")
