#!/usr/bin/env python3
"""
长题干数学题目解析器
实现信息提取、关系识别与建模指导
"""

import argparse
import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ExtractedInfo:
    variables: List[Dict]
    constraints: List[str]
    objectives: List[str]
    relations: List[Dict]
    keywords: List[str]

class ProblemAnalyzer:
    """数学问题分析器"""

    # 数学关键词库
    MATH_KEYWORDS = {
        "优化类": ["最大", "最小", "最优", "极值", "效率", "成本", "收益"],
        "变化类": ["变化率", "增长", "衰减", "速度", "加速度", "边际"],
        "几何类": ["距离", "角度", "面积", "体积", "曲线", "曲面"],
        "概率类": ["概率", "期望", "方差", "分布", "随机"],
        "代数类": ["方程", "函数", "不等式", "数列", "矩阵"]
    }

    # 变量模式识别
    VARIABLE_PATTERNS = [
        r'([a-zA-Z]_?\w*)\s*[=为是]\s*([\d\.]+)',  # x = 10
        r'([\d\.]+)\s*[个件台套种]\s*([一-龥]+)',  # 10个苹果
        r'([一-龥]+)\s*([a-zA-Z])\s*[=为]',  # 速度 v =
    ]

    def __init__(self, text: str):
        self.text = text
        self.word_count = len(text)

    def analyze(self) -> Dict:
        """完整分析流程"""
        info = self.extract_information()

        return {
            "meta": {
                "original_length": self.word_count,
                "analysis_time": "auto",
                "complexity_score": self._calc_complexity(info)
            },
            "information_extraction": {
                "variables": info.variables,
                "constraints": info.constraints,
                "objectives": info.objectives,
                "relations": info.relations
            },
            "structure_analysis": self._analyze_structure(),
            "modeling_guidance": self._generate_guidance(info),
            "reading_strategy": self._suggest_strategy()
        }

    def extract_information(self) -> ExtractedInfo:
        """提取关键信息"""
        variables = self._extract_variables()
        constraints = self._extract_constraints()
        objectives = self._extract_objectives()
        relations = self._extract_relations()
        keywords = self._extract_keywords()

        return ExtractedInfo(
            variables=variables,
            constraints=constraints,
            objectives=objectives,
            relations=relations,
            keywords=keywords
        )

    def _extract_variables(self) -> List[Dict]:
        """提取变量定义"""
        variables = []

        # 模式1: 字母 = 数值
        pattern1 = r'([a-zA-Z]_?\w*)\s*[=为]\s*([\d\.]+)\s*([一-龥a-zA-Z]*)'
        matches = re.findall(pattern1, self.text)
        for var, val, unit in matches:
            variables.append({
                "symbol": var,
                "value": float(val) if '.' in val else int(val),
                "unit": unit,
                "type": "known"
            })

        # 模式2: "设...为..."
        pattern2 = r'设\s*([a-zA-Z一-龥]+)\s*为\s*([a-zA-Z一-龥]+)'
        matches = re.findall(pattern2, self.text)
        for desc, symbol in matches:
            variables.append({
                "symbol": symbol,
                "description": desc,
                "type": "unknown"
            })

        return variables

    def _extract_constraints(self) -> List[str]:
        """提取约束条件"""
        constraints = []

        # 时间约束
        time_patterns = [r'(\d+)\s*年', r'(\d+)\s*月', r'(\d+)\s*天', r'(\d+)\s*秒']
        for pattern in time_patterns:
            matches = re.findall(pattern, self.text)
            if matches:
                constraints.append(f"时间约束: {matches}")

        # 范围约束
        range_patterns = [
            r'([a-zA-Z])\s*[∈∈]\s*\[?([\d\.,]+)\s*[,，]\s*([\d\.]+)\]?',
            r'([\d\.]+)\s*[≤<≤≥>≥]\s*([a-zA-Z])\s*[≤<≤≥>≥]\s*([\d\.]+)'
        ]

        # 自然约束
        if "非负" in self.text or "≥ 0" in self.text:
            constraints.append("非负约束: 所有物理量 ≥ 0")

        return constraints

    def _extract_objectives(self) -> List[str]:
        """提取问题目标"""
        objectives = []

        # 求解目标
        obj_patterns = [
            r'求\s*([一-龥a-zA-Z]+)',
            r'计算\s*([一-龥a-zA-Z]+)',
            r'确定\s*([一-龥a-zA-Z]+)',
            r'证明\s*([一-龥a-zA-Z]+)'
        ]

        for pattern in obj_patterns:
            matches = re.findall(pattern, self.text)
            objectives.extend(matches)

        return objectives

    def _extract_relations(self) -> List[Dict]:
        """提取变量关系"""
        relations = []

        # 等式关系
        eq_patterns = [
            r'([a-zA-Z])\s*=\s*([^=]+?)(?=[，。；]|$)',
        ]

        # 比例关系
        if "正比" in self.text or "成正比" in self.text:
            relations.append({"type": "正比", "expression": "y = kx"})
        if "反比" in self.text or "成反比" in self.text:
            relations.append({"type": "反比", "expression": "y = k/x"})

        return relations

    def _extract_keywords(self) -> List[str]:
        """提取数学关键词"""
        keywords = []
        for category, words in self.MATH_KEYWORDS.items():
            for word in words:
                if word in self.text:
                    keywords.append(f"{category}:{word}")
        return keywords

    def _analyze_structure(self) -> Dict:
        """分析题目结构"""
        paragraphs = self.text.split('\n')

        return {
            "paragraphs": len(paragraphs),
            "background_ratio": 0.6 if self.word_count > 200 else 0.4,
            "information_density": len(self._extract_variables()) / (self.word_count / 100),
            "structure_type": self._classify_structure()
        }

    def _classify_structure(self) -> str:
        """分类题目结构"""
        if "背景" in self.text[:50]:
            return "标准情境题(背景-信息-问题)"
        elif self.word_count > 300:
            return "长文本情境题"
        elif "如图" in self.text or "表格" in self.text:
            return "图文结合题"
        else:
            return "传统数学题"

    def _calc_complexity(self, info: ExtractedInfo) -> str:
        """计算复杂度"""
        score = len(info.variables) * 2 + len(info.constraints) * 3 + len(info.relations) * 2
        if score < 10:
            return "简单"
        elif score < 20:
            return "中等"
        else:
            return "复杂"

    def _generate_guidance(self, info: ExtractedInfo) -> Dict:
        """生成建模指导"""
        return {
            "step1_理解情境": {
                "action": "圈画关键术语，区分背景噪音与数学信息",
                "tips": ["先读问题，再读背景", "标记所有数字和符号"]
            },
            "step2_提取变量": {
                "action": f"识别{len(info.variables)}个变量，建立变量表",
                "variable_table": info.variables
            },
            "step3_建立关系": {
                "action": "根据约束条件和物理规律建立方程",
                "relation_map": info.relations
            },
            "step4_选择工具": {
                "action": "根据问题类型选择数学工具",
                "suggested_tools": self._suggest_tools(info)
            }
        }

    def _suggest_tools(self, info: ExtractedInfo) -> List[str]:
        """建议数学工具"""
        tools = []

        keywords = ' '.join(info.keywords)
        if "优化" in keywords or "极值" in keywords:
            tools.append("微积分(求导找极值)")
        if "变化率" in keywords:
            tools.append("微分方程")
        if "概率" in keywords:
            tools.append("概率论与统计")
        if "几何" in keywords:
            tools.append("解析几何/向量分析")

        return tools if tools else ["代数运算", "方程求解"]

    def _suggest_strategy(self) -> Dict:
        """建议阅读策略"""
        if self.word_count > 300:
            return {
                "strategy": "三遍阅读法",
                "steps": [
                    "第一遍(1min)：快速浏览，识别领域(物理/经济/生物等)",
                    "第二遍(3min)：精读背景，提取变量和约束",
                    "第三遍(2min)：聚焦问题，明确求解目标"
                ],
                "time_budget": "6-8分钟"
            }
        else:
            return {
                "strategy": "直接解析法",
                "steps": ["通读全文", "标记关键信息", "直接建模"],
                "time_budget": "3-5分钟"
            }

def format_report(analysis: Dict) -> str:
    """格式化分析报告"""
    md = f"""# 长题干题目解析报告

## 📊 基本信息

- **原文长度**：{analysis['meta']['original_length']} 字
- **复杂度**：{analysis['meta']['complexity_score']}
- **结构类型**：{analysis['structure_analysis']['structure_type']}

---

## 🔍 信息提取结果

### 识别变量（{len(analysis['information_extraction']['variables'])}个）

"""
    for var in analysis['information_extraction']['variables']:
        if 'value' in var:
            md += f"- **{var['symbol']}** = {var['value']} {var.get('unit', '')} ({var['type']})\n"
        else:
            md += f"- **{var['symbol']}**：{var.get('description', '未知')} ({var['type']})\n"

    md += f"""
### 约束条件（{len(analysis['information_extraction']['constraints'])}个）

"""
    for cons in analysis['information_extraction']['constraints']:
        md += f"- {cons}\n"

    md += f"""
### 求解目标

"""
    for obj in analysis['information_extraction']['objectives']:
        md += f"- {obj}\n"

    md += """
---

## 🧭 建模指导

"""
    for step, guidance in analysis['modeling_guidance'].items():
        step_name = step.replace('step', '步骤').replace('_', ' ')
        md += f"""### {step_name}
**行动**：{guidance['action']}

"""
        if 'tips' in guidance:
            md += "💡 **技巧**：" + " | ".join(guidance['tips']) + "\n\n"

    md += f"""---

## 📖 阅读策略建议

**推荐策略**：{analysis['reading_strategy']['strategy']}
**建议用时**：{analysis['reading_strategy']['time_budget']}

"""
    for step in analysis['reading_strategy']['steps']:
        md += f"- {step}\n"

    return md

def main():
    parser = argparse.ArgumentParser(description='长题干数学题目解析工具')
    parser.add_argument('--text', type=str, help='题目文本')
    parser.add_argument('--file', type=str, help='题目文件路径')
    parser.add_argument('--output-format', choices=['markdown', 'json'], default='markdown')

    args = parser.parse_args()

    # 获取文本
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        # 示例文本
        text = """
在某深度学习模型的训练过程中，工程师使用梯度下降法优化损失函数。
已知损失函数 L(w) = w² - 4w + 5 表示模型预测误差与参数 w 的关系，其中 w 为模型权重。
训练采用梯度下降法更新权重：w_{n+1} = w_n - η·L'(w_n)，其中 η > 0 为学习率。
当前面临的问题是：学习率 η 的选择直接影响收敛速度和稳定性。
求：(1) 损失函数的极小值点；(2) 最优学习率 η 的取值范围。
        """

    analyzer = ProblemAnalyzer(text)
    analysis = analyzer.analyze()

    if args.output_format == 'json':
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        print(format_report(analysis))

if __name__ == "__main__":
    main()
