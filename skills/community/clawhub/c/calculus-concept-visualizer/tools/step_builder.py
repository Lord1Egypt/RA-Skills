#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分步推导动画构建器
作者: 代国兴
功能: 构建数学推导的分步展示序列
"""

import json
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Step:
    """单步定义"""
    id: int
    title: str
    content: str
    latex: str
    explanation: str
    highlight_concepts: List[str]
    visual_elements: List[Dict]

class StepBuilder:
    """构建分步推导序列"""

    def __init__(self):
        self.templates = {
            "epsilon_delta_proof": self._build_epsilon_delta_proof,
            "derivative_chain_rule": self._build_chain_rule,
            "ftc_proof": self._build_ftc_proof,
            "taylor_derivation": self._build_taylor_derivation
        }

    def build(self, derivation_type: str, params: Dict) -> Dict:
        """构建推导序列"""
        if derivation_type in self.templates:
            steps = self.templates[derivation_type](params)
            return {
                "type": "step_by_step_derivation",
                "title": self._get_title(derivation_type),
                "total_steps": len(steps),
                "estimated_time": f"{len(steps) * 3}分钟",
                "steps": [self._step_to_dict(s) for s in steps],
                "navigation": {
                    "can_skip": False,
                    "can_go_back": True,
                    "auto_advance": False
                }
            }
        return {"error": f"未知的推导类型: {derivation_type}"}

    def _get_title(self, derivation_type: str) -> str:
        titles = {
            "epsilon_delta_proof": "ε-δ 极限证明的严谨推导",
            "derivative_chain_rule": "链式法则的推导与应用",
            "ftc_proof": "微积分基本定理的证明",
            "taylor_derivation": "泰勒公式的推导过程"
        }
        return titles.get(derivation_type, "数学推导")

    def _build_epsilon_delta_proof(self, params: Dict) -> List[Step]:
        """构建 ε-δ 证明步骤"""
        function = params.get("function", "3x - 1")
        a = params.get("a", 2)
        L = params.get("L", 5)

        return [
            Step(
                id=1,
                title="明确目标",
                content=f"我们要证明: 对于任意给定的 ε > 0，存在一个 δ > 0，使得当 0 < |x - {a}| < δ 时，|f(x) - {L}| < ε",
                latex=f"\forall \varepsilon > 0, \exists \delta > 0, \text{{当}} 0 < |x - {a}| < \delta \text{{时}}, |f(x) - {L}| < \varepsilon",
                explanation="这是极限的严格定义。注意顺序：先给定 ε（任意性），再寻找 δ（存在性）",
                highlight_concepts=["epsilon_arbitrary", "delta_exists"],
                visual_elements=[{"type": "highlight", "target": "epsilon_slider"}]
            ),
            Step(
                id=2,
                title="分析表达式",
                content=f"计算 |f(x) - {L}|，将 f(x) = {function} 代入",
                latex=f"|f(x) - {L}| = |({function}) - {L}| = |3x - 6| = 3|x - 2|",
                explanation="化简目标表达式，寻找与 |x - a| 的关系。这是证明的关键步骤",
                highlight_concepts=["algebraic_manipulation", "target_simplification"],
                visual_elements=[{"type": "equation", "show_steps": True}]
            ),
            Step(
                id=3,
                title="建立关系",
                content="我们发现 |f(x) - L| = 3|x - 2|。要让 3|x - 2| < ε，只需 |x - 2| < ε/3",
                latex="3|x - 2| < \varepsilon \Leftrightarrow |x - 2| < \frac{\varepsilon}{3}",
                explanation="解出 |x - a| 的上界，这就是我们要找的 δ",
                highlight_concepts=["solve_for_delta"],
                visual_elements=[{"type": "arrow", "from": "epsilon", "to": "delta"}]
            ),
            Step(
                id=4,
                title="确定 δ",
                content="因此，我们取 δ = ε/3",
                latex="\delta = \frac{\varepsilon}{3}",
                explanation="对于任意给定的 ε，我们总能找到一个 δ = ε/3 满足条件",
                highlight_concepts=["delta_formula"],
                visual_elements=[{"type": "highlight", "target": "delta_value"}]
            ),
            Step(
                id=5,
                title="验证",
                content="验证：当 |x - 2| < δ = ε/3 时，|f(x) - 5| = 3|x - 2| < 3·(ε/3) = ε",
                latex="\text{当} |x - {a}| < \delta \text{{时}}, |f(x) - {L}| < \varepsilon",
                explanation="验证 δ 的选择确实满足 ε-δ 条件，证明完成",
                highlight_concepts=["verification", "proof_complete"],
                visual_elements=[{"type": "checkmark", "animation": True}]
            )
        ]

    def _build_chain_rule(self, params: Dict) -> List[Step]:
        """构建链式法则推导"""
        return [
            Step(
                id=1,
                title="设置复合函数",
                content="设 y = f(u)，u = g(x)，则 y = f(g(x))",
                latex="y = f(u), \quad u = g(x) \Rightarrow y = f(g(x))",
                explanation="明确复合层次，识别中间变量",
                highlight_concepts=["composition", "intermediate_variable"],
                visual_elements=[]
            ),
            Step(
                id=2,
                title="导数定义",
                content="根据导数定义，dy/dx = lim(Δx→0) Δy/Δx",
                latex="\frac{dy}{dx} = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta x}",
                explanation="从导数的基本定义出发",
                highlight_concepts=["derivative_definition"],
                visual_elements=[]
            ),
            Step(
                id=3,
                title="引入中间变量",
                content="将 Δy/Δx 拆分为 (Δy/Δu)·(Δu/Δx)",
                latex="\frac{\Delta y}{\Delta x} = \frac{\Delta y}{\Delta u} \cdot \frac{\Delta u}{\Delta x}",
                explanation="关键技巧：乘以 Δu/Δu（当 Δu ≠ 0）",
                highlight_concepts=["split_fraction"],
                visual_elements=[{"type": "fraction", "highlight": "cancellation"}]
            ),
            Step(
                id=4,
                title="取极限",
                content="当 Δx→0 时，Δu→0（由 g 的连续性），所以...",
                latex="\frac{dy}{dx} = \lim_{\Delta x \to 0} \frac{\Delta y}{\Delta u} \cdot \lim_{\Delta x \to 0} \frac{\Delta u}{\Delta x} = \frac{dy}{du} \cdot \frac{du}{dx}",
                explanation="利用极限的乘法法则和连续性",
                highlight_concepts=["limit_properties", "continuity"],
                visual_elements=[{"type": "highlight", "target": "chain"}]
            )
        ]

    def _build_ftc_proof(self, params: Dict) -> List[Step]:
        """构建微积分基本定理证明"""
        return [
            Step(
                id=1,
                title="定义变上限积分",
                content="设 F(x) = ∫[a,x] f(t)dt",
                latex="F(x) = \int_a^x f(t) \, dt",
                explanation="F(x) 表示从 a 到 x 的曲边梯形面积",
                highlight_concepts=["variable_upper_limit"],
                visual_elements=[]
            ),
            Step(
                id=2,
                title="导数定义",
                content="F'(x) = lim(h→0) [F(x+h) - F(x)] / h",
                latex="F'(x) = \lim_{h \to 0} \frac{F(x+h) - F(x)}{h}",
                explanation="从导数定义出发",
                highlight_concepts=["derivative_definition"],
                visual_elements=[]
            ),
            Step(
                id=3,
                title="积分差的几何意义",
                content="F(x+h) - F(x) = ∫[x,x+h] f(t)dt，表示从 x 到 x+h 的面积",
                latex="F(x+h) - F(x) = \int_x^{x+h} f(t) \, dt",
                explanation="积分的区间可加性",
                highlight_concepts=["integral_property"],
                visual_elements=[{"type": "area", "highlight": "strip"}]
            ),
            Step(
                id=4,
                title="积分中值定理",
                content="由积分中值定理，存在 ξ∈[x,x+h]，使得...",
                latex="\int_x^{x+h} f(t) \, dt = f(\xi) \cdot h",
                explanation="连续函数在闭区间上的平均值定理",
                highlight_concepts=["mean_value_theorem_integral"],
                visual_elements=[]
            ),
            Step(
                id=5,
                title="完成证明",
                content="当 h→0 时，ξ→x，所以 F'(x) = f(x)",
                latex="F'(x) = \lim_{h \to 0} \frac{f(\xi) \cdot h}{h} = \lim_{\xi \to x} f(\xi) = f(x)",
                explanation="微积分基本定理第一部分得证",
                highlight_concepts=["ftc_part1", "proof_complete"],
                visual_elements=[{"type": "checkmark"}]
            )
        ]

    def _build_taylor_derivation(self, params: Dict) -> List[Step]:
        """构建泰勒公式推导"""
        return [
            Step(
                id=1,
                title="假设多项式形式",
                content="假设 f(x) 可以用多项式逼近：P_n(x) = a_0 + a_1(x-a) + a_2(x-a)² + ...",
                latex="P_n(x) = \sum_{k=0}^n a_k (x-a)^k",
                explanation="用幂级数的形式逼近函数",
                highlight_concepts=["polynomial_approximation"],
                visual_elements=[]
            ),
            Step(
                id=2,
                title="确定系数 a_0",
                content="令 x = a，得 P_n(a) = a_0 = f(a)",
                latex="P_n(a) = a_0 = f(a)",
                explanation="代入特殊点确定常数项",
                highlight_concepts=["coefficient_a0"],
                visual_elements=[]
            ),
            Step(
                id=3,
                title="求导确定 a_1",
                content="P_n'(x) = a_1 + 2a_2(x-a) + ...，令 x=a 得 a_1 = f'(a)",
                latex="P_n'(a) = a_1 = f'(a)",
                explanation="一阶导数匹配",
                highlight_concepts=["coefficient_a1"],
                visual_elements=[]
            ),
            Step(
                id=4,
                title="高阶导数确定一般项",
                content="继续求导，发现规律：a_k = f⁽ᵏ⁾(a) / k!",
                latex="a_k = \frac{f^{(k)}(a)}{k!}",
                explanation="归纳得出一般系数公式",
                highlight_concepts=["general_coefficient"],
                visual_elements=[]
            ),
            Step(
                id=5,
                title="泰勒公式",
                content="得到泰勒展开式",
                latex="f(x) = \sum_{k=0}^n \frac{f^{(k)}(a)}{k!}(x-a)^k + R_n(x)",
                explanation="包含余项的完整泰勒公式",
                highlight_concepts=["taylor_formula", "remainder"],
                visual_elements=[]
            )
        ]

    def _step_to_dict(self, step: Step) -> Dict:
        """转换为字典"""
        return {
            "id": step.id,
            "title": step.title,
            "content": step.content,
            "latex": step.latex,
            "explanation": step.explanation,
            "highlight_concepts": step.highlight_concepts,
            "visual_elements": step.visual_elements,
            "interactive_check": True
        }

def step_builder(derivation_type: str, **params) -> str:
    """供 OpenClaw 调用的入口函数"""
    builder = StepBuilder()
    result = builder.build(derivation_type, params)
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 测试
    print(step_builder("epsilon_delta_proof", function="3x-1", a=2, L=5))
