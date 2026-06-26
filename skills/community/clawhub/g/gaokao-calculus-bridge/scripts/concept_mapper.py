#!/usr/bin/env python3
"""
高中-大学数学概念映射器
实现知识衔接与断层识别
"""

import argparse
import json
from typing import Dict, List, Tuple

# 概念映射数据库
CONCEPT_MAPPINGS = {
    "导数": {
        "college_concept": "微分学",
        "high_school": {
            "核心内容": ["导数定义", "求导法则", "导数应用(极值、单调性)"],
            "典型题型": ["切线方程", "函数单调性讨论", "极值最值问题", "不等式证明"],
            "认知特点": "几何直观为主，代数运算为辅，强调应用套路"
        },
        "college": {
            "理论深化": ["ε-δ语言", "微分中值定理", "泰勒展开", "多元微分"],
            "应用场景": ["优化理论", "物理场论", "经济学边际分析", "误差估计"],
            "认知要求": "严格逻辑证明，抽象思维，多变量推广"
        },
        "gaps": [
            "从'会求导'到'理解导数本质'的跳跃",
            "缺乏极限严格定义基础",
            "单变量到多变量的思维拓展困难",
            "应用从'套题型'到'建模型'的转变"
        ],
        "bridge_exercises": [
            {
                "title": "用定义证明导数",
                "content": "用极限定义证明 f(x)=x² 在 x=1 处的导数为2"
            },
            {
                "title": "中值定理应用",
                "content": "证明：若f在[a,b]连续，(a,b)可导，且f(a)=f(b)，则存在c使f'(c)=0"
            },
            {
                "title": "泰勒展开初探",
                "content": "用导数信息近似函数：在x=0附近用二次多项式近似e^x"
            }
        ]
    },
    "积分": {
        "college_concept": "积分学",
        "high_school": {
            "核心内容": ["不定积分", "定积分", "微积分基本定理", "简单应用"],
            "典型题型": ["面积计算", "体积计算", "物理做功", "变速运动"],
            "认知特点": "算法化操作，强调计算技巧，应用相对简单"
        },
        "college": {
            "理论深化": ["黎曼积分理论", "反常积分", "含参积分", "勒贝格积分思想"],
            "应用场景": ["概率论期望", "物理场积分", "信号处理", "微分方程"],
            "认知要求": "理解积分本质(累积/平均)，处理复杂区域，理论严谨性"
        },
        "gaps": [
            "从'计算积分'到'理解积分思想'",
            "多重积分的区域描述与变量替换",
            "线面积分的几何直观建立",
            "积分与微分方程的联系"
        ],
        "bridge_exercises": [
            {
                "title": "积分定义理解",
                "content": "用黎曼和近似计算∫₀¹ x² dx，观察n→∞时的收敛"
            },
            {
                "title": "物理应用深化",
                "content": "计算变密度细杆的质心，理解积分作为加权平均"
            }
        ]
    },
    "向量": {
        "college_concept": "线性代数",
        "high_school": {
            "核心内容": ["平面向量", "空间向量", "向量运算", "几何应用"],
            "典型题型": ["证明平行垂直", "求夹角", "立体几何证明"],
            "认知特点": "几何直观，坐标运算，服务于立体几何"
        },
        "college": {
            "理论深化": ["向量空间", "线性变换", "矩阵代数", "特征值理论"],
            "应用场景": ["计算机图形学", "量子力学", "数据分析", "机器学习"],
            "认知要求": "抽象代数结构，n维推广，线性映射思维"
        },
        "gaps": [
            "从几何向量到抽象向量的转变",
            "矩阵作为线性变换的理解",
            "高维空间的几何直观缺失",
            "代数与几何的统一视角"
        ],
        "bridge_exercises": [
            {
                "title": "抽象向量空间",
                "content": "证明所有次数≤2的多项式构成向量空间，找出基和维数"
            },
            {
                "title": "矩阵作为变换",
                "content": "几何解释：矩阵 [[2,0],[0,0.5]] 对单位圆的作用"
            }
        ]
    },
    "数列": {
        "college_concept": "级数理论",
        "high_school": {
            "核心内容": ["等差等比数列", "通项与求和", "数学归纳法", "简单递推"],
            "典型题型": ["求通项公式", "求和技巧", "归纳证明", "应用题"],
            "认知特点": "模式识别，公式套用，离散思维"
        },
        "college": {
            "理论深化": ["无穷级数收敛性", "幂级数", "傅里叶级数", "生成函数"],
            "应用场景": ["函数逼近", "微分方程求解", "组合计数", "信号分析"],
            "认知要求": "极限思维，函数视角，解析工具"
        },
        "gaps": [
            "从有限到无限的思维跳跃",
            "收敛性判断的严格性",
            "级数作为函数的表示",
            "解析方法(生成函数等)的引入"
        ],
        "bridge_exercises": [
            {
                "title": "调和级数发散",
                "content": "证明 1 + 1/2 + 1/3 + ... 发散，理解'项趋于0'不保证收敛"
            }
        ]
    },
    "概率": {
        "college_concept": "概率论与数理统计",
        "high_school": {
            "核心内容": ["古典概型", "几何概型", "条件概率", "随机变量初步"],
            "典型题型": ["计数问题", "期望计算", "简单分布", "统计图表"],
            "认知特点": "具体情境，计算为主，直观理解"
        },
        "college": {
            "理论深化": ["公理化概率", "随机过程", "大数定律", "中心极限定理"],
            "应用场景": ["统计推断", "金融工程", "信息论", "机器学习"],
            "认知要求": "测度论基础，渐近理论，统计思维"
        },
        "gaps": [
            "从古典概型到一般概率空间的抽象",
            "随机变量作为可测函数的理解",
            "大样本与渐近理论",
            "统计推断的逻辑(频率派/贝叶斯)"
        ],
        "bridge_exercises": [
            {
                "title": "概率公理化",
                "content": "理解σ-代数与概率测度，证明基本性质"
            }
        ]
    }
}

def generate_mapping(hs_concept: str, college_concept: str = None) -> Dict:
    """生成概念映射报告"""

    if hs_concept not in CONCEPT_MAPPINGS:
        return {
            "error": f"暂不支持'{hs_concept}'的映射，支持的概念：{list(CONCEPT_MAPPINGS.keys())}"
        }

    mapping = CONCEPT_MAPPINGS[hs_concept]
    target = college_concept or mapping["college_concept"]

    report = {
        "mapping_info": {
            "from": hs_concept,
            "to": target,
            "relation": "知识深化与拓展"
        },
        "high_school_foundation": mapping["high_school"],
        "college_extension": mapping["college"],
        "cognitive_gaps": mapping["gaps"],
        "bridge_exercises": mapping["bridge_exercises"],
        "learning_path": generate_learning_path(hs_concept, mapping),
        "warning_signs": generate_warning_signs(mapping["gaps"])
    }

    return report

def generate_learning_path(concept: str, mapping: Dict) -> List[Dict]:
    """生成学习路径建议"""
    return [
        {
            "stage": 1,
            "name": "基础回顾",
            "duration": "1周",
            "tasks": [f"复习高中{concept}核心内容", "完成5道高考真题"],
            "goal": "巩固计算能力与基本应用"
        },
        {
            "stage": 2,
            "name": "理论深化",
            "duration": "2周",
            "tasks": ["学习严格定义与定理证明", "理解概念本质"],
            "goal": "建立理论框架"
        },
        {
            "stage": 3,
            "name": "应用拓展",
            "duration": "2周",
            "tasks": mapping["college"]["应用场景"][:3],
            "goal": "跨学科建模能力"
        },
        {
            "stage": 4,
            "name": "综合实践",
            "duration": "1周",
            "tasks": ["完成一个真实项目", "撰写学习反思"],
            "goal": "素养内化"
        }
    ]

def generate_warning_signs(gaps: List[str]) -> List[Dict]:
    """生成预警信号"""
    signs = []
    for gap in gaps:
        signs.append({
            "symptom": f"在学习过程中感到'{gap}'",
            "cause": "高中-大学认知断层",
            "solution": "使用本Skill的桥接练习，寻求概念可视化支持"
        })
    return signs

def format_markdown_report(report: Dict) -> str:
    """格式化为Markdown报告"""
    if "error" in report:
        return f"❌ **错误**：{report['error']}"

    md = f"""# 概念映射报告：{report['mapping_info']['from']} → {report['mapping_info']['to']}

## 📚 高中基础

**核心内容**：
{chr(10).join(['- ' + c for c in report['high_school_foundation']['核心内容']])}

**典型题型**：
{chr(10).join(['- ' + t for t in report['high_school_foundation']['典型题型']])}

**认知特点**：{report['high_school_foundation']['认知特点']}

---

## 🎓 大学拓展

**理论深化**：
{chr(10).join(['- ' + t for t in report['college_extension']['理论深化']])}

**应用场景**：
{chr(10).join(['- ' + a for a in report['college_extension']['应用场景']])}

**认知要求**：{report['college_extension']['认知要求']}

---

## ⚠️ 认知鸿沟（关键难点）

"""
    for i, gap in enumerate(report['cognitive_gaps'], 1):
        md += f"{i}. **{gap}**\n"

    md += """
---

## 🌉 桥接练习（过渡训练）

"""
    for ex in report['bridge_exercises']:
        md += f"""### {ex['title']}
{ex['content']}

"""

    md += """---

## 🛤️ 推荐学习路径

"""
    for stage in report['learning_path']:
        md += f"""### 阶段{stage['stage']}：{stage['name']}（{stage['duration']}）

**任务**：
{chr(10).join(['- ' + t for t in stage['tasks']])}

**目标**：{stage['goal']}

"""

    md += """---

## 🚨 预警信号

如果在学习过程中出现以下情况，说明你可能遇到了认知断层：

"""
    for sign in report['warning_signs']:
        md += f"""- **症状**：{sign['symptom']}
  - **原因**：{sign['cause']}
  - **对策**：{sign['solution']}

"""

    return md

def main():
    parser = argparse.ArgumentParser(description='高中-大学数学概念映射工具')
    parser.add_argument('--from', dest='hs_concept', required=True,
                       help='高中概念（如：导数、积分、向量、数列、概率）')
    parser.add_argument('--to', dest='college_concept',
                       help='目标大学概念（可选）')
    parser.add_argument('--mode', choices=['mapping', 'ability', 'gap'],
                       default='mapping',
                       help='输出模式')
    parser.add_argument('--output-format', choices=['markdown', 'json'],
                       default='markdown')

    args = parser.parse_args()

    if args.mode == 'ability':
        # 输出能力对标分析
        report = {
            "title": "2026高考改革能力 → 大学数学能力对标",
            "mapping": {
                "情境理解": "学术文献阅读与问题定义",
                "数学建模": "理论建模与算法设计",
                "跨学科应用": "多学科交叉研究",
                "信息处理": "数据科学与大数据分析"
            }
        }
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        report = generate_mapping(args.hs_concept, args.college_concept)
        if args.output_format == 'json':
            output = json.dumps(report, ensure_ascii=False, indent=2)
        else:
            output = format_markdown_report(report)

    print(output)

if __name__ == "__main__":
    main()
