#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渐进式检测题生成器
作者: 代国兴
功能: 生成识别→应用→迁移三个层次的检测题
"""

import json
import random
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class QuizTemplate:
    """题目模板"""
    concept: str
    level: str  # "recognition", "application", "transfer"
    template: str
    variables: Dict
    correct_answer: str
    distractors: List[str]
    explanation: str

class QuizGenerator:
    """检测题生成器"""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, List[QuizTemplate]]:
        """加载题目模板库"""
        return {
            "limit": [
                # 识别层
                QuizTemplate(
                    concept="limit",
                    level="recognition",
                    template="下列关于 lim(x→a) f(x) = L 的描述，正确的是：",
                    variables={},
                    correct_answer="∀ε>0, ∃δ>0, 当 0<|x-a|<δ 时，|f(x)-L|<ε",
                    distractors=[
                        "∀δ>0, ∃ε>0, 当 |f(x)-L|<ε 时，0<|x-a|<δ",
                        "∃ε>0, ∀δ>0, 当 0<|x-a|<δ 时，|f(x)-L|<ε",
                        "∀ε>0, ∃δ>0, 当 |x-a|<δ 时，|f(x)-L|<ε（缺少去心条件）"
                    ],
                    explanation="ε-δ 定义的核心是：ε 的任意性在前，δ 的存在性在后，且去心邻域 0<|x-a| 是关键"
                ),
                # 应用层
                QuizTemplate(
                    concept="limit",
                    level="application",
                    template="用 ε-δ 定义证明 lim(x→{a}) ({function}) = {limit}",
                    variables={
                        "a": 2,
                        "function": "3x-1",
                        "limit": 5
                    },
                    correct_answer="对于任意 ε>0，取 δ=ε/3，当 0<|x-2|<δ 时，|(3x-1)-5|=3|x-2|<3·(ε/3)=ε",
                    distractors=[
                        "直接代入 x=2 得到 5",
                        "取 δ=ε，则 |3x-6|<ε 不成立",
                        "认为需要限制 ε<1"
                    ],
                    explanation="线性函数的证明直接解出 |x-a| 与 |f(x)-L| 的关系"
                ),
                # 迁移层
                QuizTemplate(
                    concept="limit",
                    level="transfer",
                    template="函数 f(x) 在 x=a 处无定义，是否意味着 lim(x→a) f(x) 不存在？",
                    variables={},
                    correct_answer="否。极限存在与否与函数在该点是否有定义无关",
                    distractors=[
                        "是。函数无定义则极限必不存在",
                        "无法确定，需要更多信息",
                        "只有当函数在该点连续时才存在极限"
                    ],
                    explanation="极限关注的是去心邻域内的趋势，而非该点的函数值。可去间断点就是典型反例"
                )
            ],
            "derivative": [
                QuizTemplate(
                    concept="derivative",
                    level="recognition",
                    template="导数 f'(a) 的几何意义是：",
                    variables={},
                    correct_answer="函数图像在点 (a, f(a)) 处切线的斜率",
                    distractors=[
                        "函数图像在点 (a, f(a)) 处割线的斜率",
                        "函数在 x=a 处的函数值",
                        "函数图像在 x=a 处的曲率"
                    ],
                    explanation="导数是割线斜率的极限，当 Δx→0 时割线变为切线"
                ),
                QuizTemplate(
                    concept="derivative",
                    level="application",
                    template="用导数定义求 f(x)={function} 在 x={a} 处的导数",
                    variables={
                        "function": "x²+2x",
                        "a": 1
                    },
                    correct_answer="f'(1) = lim(h→0) [(1+h)²+2(1+h)-3]/h = lim(h→0) [h²+4h]/h = 4",
                    distractors=[
                        "直接求导公式得 2x+2，代入 x=1 得 4（虽结果对但跳过了定义）",
                        "计算 f(1)=3 作为导数",
                        "认为 h=0 时分母为零，极限不存在"
                    ],
                    explanation="导数定义的核心是差商的极限，需展示完整的代数化简过程"
                ),
                QuizTemplate(
                    concept="derivative",
                    level="transfer",
                    template="若函数 f(x) 在 x=a 处可导，则下列哪个结论必然成立？",
                    variables={},
                    correct_answer="f(x) 在 x=a 处连续",
                    distractors=[
                        "f(x) 在 x=a 的某邻域内可导",
                        "f'(x) 在 x=a 处连续",
                        "f(x) 在 x=a 处二阶可导"
                    ],
                    explanation="可导必连续，但连续不一定可导，可导也不一定在邻域内可导"
                )
            ],
            "integral": [
                QuizTemplate(
                    concept="integral",
                    level="recognition",
                    template="定积分 ∫[a,b] f(x)dx 的几何意义是：",
                    variables={},
                    correct_answer="由曲线 y=f(x)、x轴及直线 x=a、x=b 围成的曲边梯形面积的代数和",
                    distractors=[
                        "曲边梯形的几何面积（绝对值之和）",
                        "函数在 [a,b] 上的平均值",
                        "曲线 y=f(x) 在 [a,b] 上的弧长"
                    ],
                    explanation="定积分是代数和，x轴下方区域取负值，与几何面积不同"
                ),
                QuizTemplate(
                    concept="integral",
                    level="application",
                    template="用黎曼和定义计算 ∫[0,1] x² dx",
                    variables={},
                    correct_answer="lim(n→∞) Σ(i=1 to n) (i/n)² · (1/n) = lim(n→∞) [n(n+1)(2n+1)]/(6n³) = 1/3",
                    distractors=[
                        "直接代入上下限得 1²-0²=1",
                        "认为黎曼和与积分值只是近似关系",
                        "取左端点与右端点结果不同"
                    ],
                    explanation="黎曼和的极限就是定积分的定义，需展示求和公式的应用"
                ),
                QuizTemplate(
                    concept="integral",
                    level="transfer",
                    template="设 F(x) = ∫[0,x] f(t)dt，其中 f(t) 连续，则 F'(x) = ?",
                    variables={},
                    correct_answer="f(x)",
                    distractors=[
                        "F(x)·f(x)",
                        "f(x) - f(0)",
                        "∫[0,x] f'(t)dt"
                    ],
                    explanation="微积分基本定理第一部分：变上限积分的导数等于被积函数在上限处的值"
                )
            ]
        }

    def generate_quiz(self, concept: str, difficulty: float = 0.5) -> List[Dict]:
        """
        生成渐进式检测题组

        Args:
            concept: 概念名称
            difficulty: 难度系数 (0-1)

        Returns:
            3道题目 [识别题, 应用题, 迁移题]
        """
        templates = self.templates.get(concept, [])

        # 按层次分组
        by_level = {
            "recognition": [t for t in templates if t.level == "recognition"],
            "application": [t for t in templates if t.level == "application"],
            "transfer": [t for t in templates if t.level == "transfer"]
        }

        quiz_set = []

        # 每层次随机选一题
        for level in ["recognition", "application", "transfer"]:
            if by_level[level]:
                template = random.choice(by_level[level])
                question = self._render_template(template)
                quiz_set.append(question)

        return quiz_set

    def _render_template(self, template: QuizTemplate) -> Dict:
        """渲染题目模板"""
        # 替换变量
        text = template.template
        for var, val in template.variables.items():
            text = text.replace(f"{{{var}}}", str(val))

        # 打乱选项
        all_options = [template.correct_answer] + template.distractors
        random.shuffle(all_options)
        correct_index = all_options.index(template.correct_answer)

        return {
            "concept": template.concept,
            "level": template.level,
            "level_description": {
                "recognition": "概念识别（记忆+理解）",
                "application": "直接应用（计算+证明）",
                "transfer": "迁移创新（辨析+综合）"
            }[template.level],
            "question": text,
            "type": "multiple_choice",
            "options": all_options,
            "correct_index": correct_index,
            "correct_answer": template.correct_answer,
            "explanation": template.explanation,
            "scoring": {
                "recognition": 30,
                "application": 40,
                "transfer": 30
            }[template.level]
        }

def generate_quiz(concept: str, difficulty: float = 0.5) -> str:
    """供 OpenClaw 调用的入口函数"""
    generator = QuizGenerator()
    quiz_set = generator.generate_quiz(concept, difficulty)
    return json.dumps({
        "quiz_set": quiz_set,
        "total_score": 100,
        "time_estimate": "15-20分钟",
        "instruction": "请按顺序完成3道题目，完成后将给出诊断报告"
    }, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 测试
    print(generate_quiz("limit", 0.6))
