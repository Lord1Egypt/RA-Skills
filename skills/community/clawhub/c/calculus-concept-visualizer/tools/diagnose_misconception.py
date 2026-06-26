#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认知诊断与误区识别系统
作者: 代国兴
功能: 分析学生回答，识别数学概念理解误区
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class Misconception:
    """误区定义"""
    id: str
    concept: str
    pattern: List[str]
    description: str
    diagnosis: str
    remedy: str
    counter_example: str
    severity: str  # "high", "medium", "low"

class MisconceptionDatabase:
    """常见误区数据库"""

    def __init__(self):
        self.db = self._load_misconceptions()

    def _load_misconceptions(self) -> Dict[str, List[Misconception]]:
        """加载预定义的误区模式"""
        return {
            "limit": [
                Misconception(
                    id="limit_equals_value",
                    concept="limit",
                    pattern=["等于", "就是", "直接代入", "把.*代入", "计算.*值"],
                    description="混淆极限值与函数值",
                    diagnosis="学生可能认为极限就是 f(a)，忽视了去心邻域的要求",
                    remedy="展示 f(a) 不存在但极限存在的例子（如可去间断点），强调极限描述的是'趋近'而非'等于'",
                    counter_example="f(x)=(x²-1)/(x-1) 在 x=1 处无定义，但极限为 2",
                    severity="high"
                ),
                Misconception(
                    id="epsilon_order",
                    concept="limit",
                    pattern=["ε 比 δ 小", "δ 依赖于 ε", "先找.*δ", "ε 和 δ 的关系"],
                    description="逻辑顺序颠倒",
                    diagnosis="未能理解 '先任意给定 ε，再寻找 δ' 的逻辑顺序",
                    remedy="使用游戏化类比：你挑战（ε），我应对（δ）。强调 ε 的任意性（对手）和 δ 的存在性（回应）",
                    counter_example="如果先固定 δ，再要求 ε，就无法保证精度",
                    severity="high"
                ),
                Misconception(
                    id="one_sided_confusion",
                    concept="limit",
                    pattern=["左右极限", "左边.*右边", "两侧", "方向"],
                    description="左右极限概念混淆",
                    diagnosis="未能区分左极限、右极限与双侧极限的关系",
                    remedy="分段函数可视化：分别绘制 x→a⁻ 和 x→a⁺ 的路径，展示不同收敛情况",
                    counter_example="f(x)=|x|/x 在 x=0 处左右极限分别为 -1 和 1",
                    severity="medium"
                ),
                Misconception(
                    id="infinity_misunderstanding",
                    concept="limit",
                    pattern=["无穷大.*极限", "1/0.*无穷", "∞ 是数"],
                    description="对无穷大的本质理解错误",
                    diagnosis="将 ∞ 视为一个具体的'很大'的数，而非趋势描述",
                    remedy="强调 ∞ 不是实数，而是描述无界增长的过程。对比：'趋于∞' vs '等于∞'",
                    counter_example="lim(x→0) 1/x² = +∞，但 1/x² 永远不会'等于'任何具体的数",
                    severity="medium"
                )
            ],
            "derivative": [
                Misconception(
                    id="derivative_slope_only",
                    concept="derivative",
                    pattern=["斜率", "切线斜率", "陡峭程度"],
                    description="仅理解为几何斜率，忽视变化率本质",
                    diagnosis="将导数等同于几何概念，未能理解其作为瞬时变化率的物理/经济意义",
                    remedy="多情境举例：速度（位置变化率）、边际成本（成本变化率）、温度变化率",
                    counter_example="s(t)=t² 的位移函数，v(2)=4 表示 t=2 时刻的瞬时速度",
                    severity="medium"
                ),
                Misconception(
                    id="derivative_not_exist_only_corner",
                    concept="derivative",
                    pattern=["尖点", "拐角", "不光滑"],
                    description="认为只有尖点才不可导",
                    diagnosis="忽视了其他不可导情况（如间断、垂直切线、震荡）",
                    remedy="分类展示不可导的四种情况：间断、尖点、垂直切线、无限震荡",
                    counter_example="Weierstrass 函数处处连续但处处不可导",
                    severity="high"
                ),
                Misconception(
                    id="chain_rule_confusion",
                    concept="derivative",
                    pattern=["链式法则", "复合函数", "层层求导"],
                    description="链式法则应用错误",
                    diagnosis="未能正确识别复合层次，或遗漏中间变量求导",
                    remedy="分层可视化：u=g(x) 作为中间层，明确 dy/dx = dy/du · du/dx 的链条",
                    counter_example="sin(x²) 的导数是 cos(x²)·2x，不是 cos(x²) 或 cos(2x)",
                    severity="high"
                )
            ],
            "integral": [
                Misconception(
                    id="integral_area_only",
                    concept="integral",
                    pattern=["面积", "曲边梯形", "图形大小"],
                    description="仅理解为几何面积",
                    diagnosis="将定积分等同于面积，忽视了代数和、物理意义等更广泛应用",
                    remedy="强调代数和（x轴下方为负）：位移 vs 路程。展示非几何应用（概率、功、质心）",
                    counter_example="∫[-π,π] sin(x)dx = 0，几何面积非零但代数和为零",
                    severity="medium"
                ),
                Misconception(
                    id="ftc_confusion",
                    concept="integral",
                    pattern=["微积分基本定理", "牛顿-莱布尼茨", "F(b)-F(a)"],
                    description="微积分基本定理理解不深入",
                    diagnosis="机械使用 F(b)-F(a)，不理解变上限积分与导数的互逆关系",
                    remedy="可视化 d/dx ∫[a,x] f(t)dt = f(x) 的过程，展示'积分后再求导'回到原函数",
                    counter_example="d/dx ∫[0,x] sin(t)dt = sin(x)，验证互逆性",
                    severity="high"
                )
            ],
            "continuity": [
                Misconception(
                    id="continuity_draw",
                    concept="continuity",
                    pattern=["一笔画", "连着的", "没有断", "能画出来"],
                    description="过度依赖几何直观",
                    diagnosis="用'一笔画'等不严谨描述替代 ε-δ 定义",
                    remedy="对比：直观连续 vs 严格连续。展示 Weierstrass 函数（处处连续处处不可导）打破'光滑'直觉",
                    counter_example="Weierstrass 函数 w(x)=Σaⁿcos(bⁿπx) 处处连续但无处可导",
                    severity="medium"
                ),
                Misconception(
                    id="continuous_implies_differentiable",
                    concept="continuity",
                    pattern=["连续.*可导", "连续则.*可导", "连续一定.*"],
                    description="认为连续必可导",
                    diagnosis="混淆了连续与可导的蕴含关系（可导⇒连续，但逆不成立）",
                    remedy="明确逻辑关系：可导 ⊂ 连续。展示连续但不可导的多种例子",
                    counter_example="f(x)=|x| 在 x=0 连续但不可导",
                    severity="high"
                )
            ]
        }

    def get_misconceptions(self, concept: str) -> List[Misconception]:
        """获取指定概念的误区列表"""
        return self.db.get(concept, [])

    def get_all(self) -> Dict[str, List[Misconception]]:
        """获取全部误区数据库"""
        return self.db

class MisconceptionDetector:
    """误区检测器"""

    def __init__(self):
        self.db = MisconceptionDatabase()

    def analyze(self, student_response: str, concept: str) -> Dict:
        """
        分析学生回答，检测潜在误区

        Args:
            student_response: 学生的回答文本
            concept: 目标概念（limit/derivative/integral/continuity）

        Returns:
            诊断报告
        """
        detected = []
        response_lower = student_response.lower()

        misconceptions = self.db.get_misconceptions(concept)

        for mc in misconceptions:
            # 多模式匹配
            match_score = self._calculate_match(response_lower, mc.pattern)
            if match_score > 0:
                detected.append({
                    "misconception": asdict(mc),
                    "confidence": match_score,
                    "matched_patterns": self._get_matched_patterns(response_lower, mc.pattern)
                })

        # 按置信度排序
        detected.sort(key=lambda x: x["confidence"], reverse=True)

        return {
            "input_analyzed": student_response,
            "concept": concept,
            "has_misconception": len(detected) > 0,
            "detected_count": len(detected),
            "detected": detected,
            "risk_level": self._calculate_risk_level(detected),
            "suggested_intervention": self._generate_intervention(detected),
            "follow_up_questions": self._generate_questions(detected, concept)
        }

    def _calculate_match(self, text: str, patterns: List[str]) -> float:
        """计算匹配分数"""
        score = 0.0
        for pattern in patterns:
            if re.search(pattern, text):
                score += 1.0
        return min(score / len(patterns) * 1.5, 1.0)  # 最高1.0

    def _get_matched_patterns(self, text: str, patterns: List[str]) -> List[str]:
        """获取匹配到的模式"""
        matched = []
        for pattern in patterns:
            if re.search(pattern, text):
                matched.append(pattern)
        return matched

    def _calculate_risk_level(self, detected: List[Dict]) -> str:
        """计算风险等级"""
        if not detected:
            return "low"

        high_count = sum(1 for d in detected if d["misconception"]["severity"] == "high")
        avg_confidence = sum(d["confidence"] for d in detected) / len(detected)

        if high_count >= 2 or avg_confidence > 0.8:
            return "high"
        elif high_count >= 1 or avg_confidence > 0.5:
            return "medium"
        return "low"

    def _generate_intervention(self, detected: List[Dict]) -> List[Dict]:
        """生成干预方案"""
        interventions = []
        for d in detected[:3]:  # 最多3个
            mc = d["misconception"]
            interventions.append({
                "target_misconception": mc["id"],
                "type": "counter_example",
                "priority": "immediate" if mc["severity"] == "high" else "normal",
                "description": mc["remedy"],
                "visualization": {
                    "type": "geogebra",
                    "concept": mc["id"],
                    "focus": "counter_example"
                },
                "discussion_questions": [
                    f"观察 {mc['counter_example']}，你认为极限/导数/积分是多少？",
                    "这个结果与你的直觉一致吗？如果不一致，问题出在哪里？"
                ]
            })
        return interventions

    def _generate_questions(self, detected: List[Dict], concept: str) -> List[Dict]:
        """生成跟进检测题"""
        if not detected:
            # 无误区，生成巩固题
            return [
                {"type": "conceptual", "difficulty": "medium", "purpose": "巩固理解"},
                {"type": "application", "difficulty": "medium", "purpose": "迁移应用"}
            ]

        questions = []
        for d in detected[:2]:
            mc = d["misconception"]
            questions.append({
                "type": "diagnostic",
                "target": mc["id"],
                "question": f"针对'{mc['description']}'的辨析题",
                "format": "multiple_choice",
                "options": [
                    f"A. 正确理解（针对{mc['id']}的正确表述）",
                    f"B. 常见误区（{mc['description']}）",
                    "C. 其他干扰项"
                ],
                "correct": "A",
                "explanation": mc["diagnosis"]
            })

        return questions

def diagnose_misconception(student_response: str, concept: str) -> str:
    """供 OpenClaw 调用的诊断入口"""
    detector = MisconceptionDetector()
    result = detector.analyze(student_response, concept)
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 测试
    test_response = "我觉得极限就是直接把 x=0 代入函数计算的值"
    print(diagnose_misconception(test_response, "limit"))
