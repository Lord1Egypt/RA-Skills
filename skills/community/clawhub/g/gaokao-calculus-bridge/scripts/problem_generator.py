#!/usr/bin/env python3
"""
情境化数学题目生成器
符合2026高考改革要求：科技前沿背景 + 建模能力考查
"""

import argparse
import json
import random
from datetime import datetime
from typing import Dict, List

# 真实世界情境库
REAL_WORLD_CONTEXTS = {
    "ai": {
        "name": "人工智能与优化",
        "cases": [
            {
                "title": "神经网络训练优化",
                "background": """在某深度学习模型的训练过程中，工程师使用梯度下降法优化损失函数。

已知损失函数 L(w) = w² - 4w + 5 表示模型预测误差与参数 w 的关系，其中 w 为模型权重。
训练采用梯度下降法更新权重：w_{n+1} = w_n - η·L'(w_n)，其中 η > 0 为学习率。

当前面临的问题是：学习率 η 的选择直接影响收敛速度和稳定性。过大的 η 导致震荡，过小的 η 收敛缓慢。""",
                "variables": ["w: 模型权重", "L(w): 损失函数", "η: 学习率", "∇L: 梯度"],
                "constraints": ["η > 0", "w ∈ ℝ", "收敛条件：|1-2η| < 1"],
                "model": "优化理论/微分方程",
                "math_topic": "导数应用/数列极限"
            },
            {
                "title": "强化学习中的探索-利用权衡",
                "background": """在推荐系统中，算法需要在"推荐用户可能喜欢的内容"(利用)与"探索新内容"(探索)之间取得平衡。

设 ε-贪心策略中，探索率 ε ∈ (0,1)。在每一步，算法以概率 ε 随机探索，以概率 1-ε 选择当前最优动作。
累积收益 R(t) 随时间变化，探索过多导致短期收益低但长期可能更优，利用过多可能陷入局部最优。""",
                "variables": ["ε: 探索率", "R(t): 累积收益", "p: 点击率估计", "t: 时间步"],
                "constraints": ["0 < ε < 1", "R(0) = 0", "p ∈ [0,1]"],
                "model": "概率论/最优化",
                "math_topic": "极值问题/概率分布"
            }
        ]
    },
    "carbon": {
        "name": "碳中和与气候",
        "cases": [
            {
                "title": "碳排放路径优化",
                "background": """某城市承诺在2060年前实现碳中和。当前年碳排放量为 E₀ = 1000万吨，计划每年减少 r% 的排放。

然而，减排并非线性过程：初期技术改造成本高，减排难度大；随着技术进步，单位减排成本下降。
实际减排模型为：dE/dt = -k·E·(1 - E/E_max)，其中 k 为技术系数，E_max 为理论最大减排潜力。""",
                "variables": ["E(t): t年碳排放量", "r: 年减排率", "k: 技术系数", "E_max: 最大减排潜力"],
                "constraints": ["E(0) = E₀", "E(t) ≥ 0", "E(2060) ≤ 0.1E₀"],
                "model": "指数衰减/逻辑斯蒂方程",
                "math_topic": "微分方程/定积分应用"
            }
        ]
    },
    "physics": {
        "name": "现代物理",
        "cases": [
            {
                "title": "量子计算中的叠加态演化",
                "background": """在量子比特的状态演化中，波函数 ψ(t) 随时间变化满足薛定谔方程：iℏ·dψ/dt = Hψ，
其中 H 为哈密顿算符，ℏ 为约化普朗克常数。

考虑一个两能级系统，哈密顿量 H = E₀·σ_z，其中 σ_z 为泡利矩阵。初始态为 |ψ(0)⟩ = α|0⟩ + β|1⟩，
|α|² + |β|² = 1。需要计算 t 时刻的态矢量以及测量得到 |0⟩ 态的概率。""",
                "variables": ["ψ(t): 波函数", "H: 哈密顿算符", "E: 能量本征值", "α,β: 叠加系数"],
                "constraints": ["|α|² + |β|² = 1", "ℏ > 0", "E₀ > 0"],
                "model": "复变函数/微分方程",
                "math_topic": "复数运算/常微分方程"
            }
        ]
    },
    "economics": {
        "name": "金融科技",
        "cases": [
            {
                "title": "期权定价与风险对冲",
                "background": """在金融衍生品定价中，Black-Scholes模型描述了欧式看涨期权价格 C(S,t) 的演化：
∂C/∂t + ½σ²S²·∂²C/∂S² + rS·∂C/∂S - rC = 0

其中 S 为标的资产价格，t 为时间，σ 为波动率，r 为无风险利率。
某投资者持有执行价为 K、到期日为 T 的看涨期权，需要计算当前期权理论价格及Delta对冲比率。""",
                "variables": ["C: 期权价格", "S: 标的资产价格", "σ: 波动率", "r: 无风险利率", "K: 执行价"],
                "constraints": ["S > 0", "σ > 0", "r ≥ 0", "t ≤ T"],
                "model": "偏微分方程/概率论",
                "math_topic": "偏微分方程/概率分布"
            }
        ]
    },
    "biology": {
        "name": "生物数学",
        "cases": [
            {
                "title": "流行病传播的SIR模型",
                "background": """在流行病学中，SIR模型将人群分为三类：易感者(S)、感染者(I)、康复者(R)。

微分方程组为：
dS/dt = -β·S·I/N
dI/dt = β·S·I/N - γ·I
dR/dt = γ·I

其中 N = S + I + R 为总人口，β 为传染率，γ 为康复率。基本再生数 R₀ = β/γ。
公共卫生部门需要预测疫情峰值时间并评估不同防控策略的效果。""",
                "variables": ["S: 易感者", "I: 感染者", "R: 康复者", "β: 传染率", "γ: 康复率", "R₀: 基本再生数"],
                "constraints": ["S,I,R ≥ 0", "S+I+R = N", "β,γ > 0"],
                "model": "常微分方程组/动力系统",
                "math_topic": "微分方程/稳定性分析"
            }
        ]
    }
}

def generate_problem(domain: str, difficulty: str, topic: str = None) -> Dict:
    """生成情境化数学题目"""

    if domain not in REAL_WORLD_CONTEXTS:
        domain = "ai"  # 默认领域

    case = random.choice(REAL_WORLD_CONTEXTS[domain]["cases"])

    # 根据难度调整
    if difficulty == "high_school":
        layers = 2
        complexity = "基础建模"
        hint_level = "详细提示"
    elif difficulty == "college":
        layers = 3
        complexity = "理论深化"
        hint_level = "关键提示"
    else:  # bridge
        layers = 3
        complexity = "衔接过渡"
        hint_level = "引导性提示"

    problem = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "domain": domain,
            "domain_name": REAL_WORLD_CONTEXTS[domain]["name"],
            "difficulty": difficulty,
            "complexity": complexity,
            "topic": topic or case["math_topic"],
            "hint_level": hint_level
        },
        "context": {
            "title": case["title"],
            "background": case["background"],
            "word_count": len(case["background"])
        },
        "information_layer": {
            "variables": case["variables"],
            "constraints": case["constraints"],
            "objective": "最优化/预测/分析/证明"
        },
        "questions": generate_question_layers(case, layers, difficulty),
        "modeling_guide": {
            "abstraction_path": f"{case['title']} → {case['model']} → {case['math_topic']}",
            "key_insight": "剥离物理/工程细节，关注量化关系与数学结构",
            "common_pitfalls": [
                "过度关注背景知识而忽视数学本质",
                "忽视隐含约束条件",
                "单位不统一导致计算错误",
                "混淆变量与常数"
            ]
        }
    }

    return problem

def generate_question_layers(case: Dict, layers: int, difficulty: str) -> List[Dict]:
    """生成分层问题"""
    questions = []

    if layers >= 1:
        q1 = {
            "level": 1,
            "type": "信息提取与理解",
            "question": f"根据背景描述，完成以下任务：\n" +
                       f"(a) 识别问题中的关键变量，并解释'{case['variables'][0]}'的实际意义；\n" +
                       f"(b) 列出所有约束条件；\n" +
                       f"(c) 明确本问题需要解决的数学目标。",
            "points": 20,
            "assessment_focus": "情境理解能力"
        }
        if difficulty == "high_school":
            q1["hints"] = ["圈画题干中的数学符号", "区分已知量和未知量", "明确问题问的是什么"]
        questions.append(q1)

    if layers >= 2:
        q2 = {
            "level": 2,
            "type": "数学建模",
            "question": f"将上述情境抽象为数学问题：\n" +
                       f"(a) 建立描述{case['variables'][0].split(':')[0]}变化的数学模型（方程/函数/关系式）；\n" +
                       f"(b) 说明你的建模假设；\n" +
                       f"(c) 确定求解该模型需要的数学工具。",
            "points": 40,
            "assessment_focus": "建模与抽象能力"
        }
        if difficulty in ["high_school", "bridge"]:
            q2["hints"] = [
                f"参考{case['math_topic']}相关知识",
                "先建立变量间的关系，再考虑约束",
                "可以画图辅助理解"
            ]
        questions.append(q2)

    if layers >= 3:
        q3 = {
            "level": 3,
            "type": "求解与拓展",
            "question": f"(a) 求解所建立的模型，给出解析解或数值解；\n" +
                       f"(b) 解释结果在现实情境中的含义；\n" +
                       f"(c) 讨论模型假设的合理性，提出至少一种改进方向。",
            "points": 40,
            "assessment_focus": "求解与批判思维"
        }
        if difficulty == "college":
            q3["extension"] = "(d) 对模型进行敏感性分析，讨论关键参数变化对结果的影响。"
        questions.append(q3)

    return questions

def format_markdown(problem: Dict) -> str:
    """格式化为Markdown输出"""
    md = f"""# {problem['context']['title']}

> **领域**：{problem['metadata']['domain_name']} | **难度**：{problem['metadata']['complexity']} | **数学主题**：{problem['metadata']['topic']}

---

## 【背景】（{problem['context']['word_count']}字）

{problem['context']['background']}

---

## 【信息提取层】

**关键变量**：
{chr(10).join(['- **' + v.split(':')[0] + '**：' + v.split(':')[1] for v in problem['information_layer']['variables']])}

**约束条件**：
{chr(10).join(['- ' + c for c in problem['information_layer']['constraints']])}

**问题目标**：{problem['information_layer']['objective']}

---

## 【数学建模指引】

**抽象路径**：`{problem['modeling_guide']['abstraction_path']}`

**核心洞察**：{problem['modeling_guide']['key_insight']}

**⚠️ 常见陷阱**：
{chr(10).join(['- ' + p for p in problem['modeling_guide']['common_pitfalls']])}

---

## 【问题链】（总分：{sum(q['points'] for q in problem['questions'])}分）
"""
    for q in problem['questions']:
        md += f"""
### ({q['level']}) {q['type']} [{q['points']}分]

{q['question']}
"""
        if 'hints' in q:
            md += f"""
💡 **提示**：{' → '.join(q['hints'])}
"""
        if 'extension' in q:
            md += f"""
🚀 **拓展**：{q['extension']}
"""
        md += f"""
*考查重点：{q['assessment_focus']}*

"""

    md += """---

## 【评价量规】

| 维度 | 优秀(90-100) | 良好(75-89) | 合格(60-74) | 待改进(<60) |
|------|-------------|------------|------------|------------|
| 情境理解 | 准确提取所有关键信息 | 提取主要信息，遗漏次要信息 | 提取部分信息，有误解 | 信息提取错误或缺失 |
| 模型构建 | 模型合理，假设明确 | 模型基本合理，假设较清楚 | 模型有缺陷，假设不清 | 模型错误或无建模过程 |
| 数学求解 | 过程严谨，结果正确 | 过程基本正确， minor错误 | 过程有缺陷，结果有误 | 无法完成求解 |
| 现实解释 | 深刻联系实际，有洞察 | 较好联系实际 | 解释牵强 | 无现实解释 |

---

*生成时间：{problem['metadata']['generated_at']}*
""".format(problem=problem)

    return md

def main():
    parser = argparse.ArgumentParser(
        description='生成符合2026高考改革要求的情境化数学题目',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 problem_generator.py --domain ai --difficulty bridge
  python3 problem_generator.py --domain carbon --difficulty college --output-format json
        """)

    parser.add_argument('--domain', 
                       choices=['ai', 'carbon', 'physics', 'economics', 'biology'], 
                       default='ai',
                       help='情境领域 (默认: ai)')
    parser.add_argument('--difficulty', 
                       choices=['high_school', 'college', 'bridge'], 
                       default='bridge',
                       help='难度级别 (默认: bridge)')
    parser.add_argument('--topic', 
                       type=str, 
                       help='指定数学主题')
    parser.add_argument('--output-format', 
                       choices=['markdown', 'json'], 
                       default='markdown',
                       help='输出格式 (默认: markdown)')
    parser.add_argument('--save', 
                       type=str,
                       metavar='FILE',
                       help='保存到文件')

    args = parser.parse_args()

    problem = generate_problem(args.domain, args.difficulty, args.topic)

    if args.output_format == 'json':
        output = json.dumps(problem, ensure_ascii=False, indent=2)
    else:
        output = format_markdown(problem)

    if args.save:
        with open(args.save, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✓ 已保存到: {args.save}")
    else:
        print(output)

if __name__ == "__main__":
    main()
