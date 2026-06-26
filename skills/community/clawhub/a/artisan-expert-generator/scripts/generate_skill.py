#!/usr/bin/env python3
"""
职业专家Skill生成脚本
接收专家框架数据，生成完整的SKILL.md文件
"""

import argparse
import json
import sys
from pathlib import Path


def generate_yaml_frontmatter(expert_name, description):
    """生成YAML前言区"""
    expert_name_clean = expert_name.lower().replace(" ", "-")
    return f"""---
name: {expert_name_clean}
description: {description}
---
"""


def generate_skill_content(expert_name, knowledge_system, analysis_framework,
                          decision_rules, ethics, expression_style):
    """生成SKILL.md正文内容"""
    content = f"""# {expert_name}

## 角色定位
{expert_name}是{knowledge_system.get('role_definition', '该领域的专业专家')}。

## 知识体系

### 核心概念
"""

    # 核心概念
    core_concepts = knowledge_system.get('core_concepts', [])
    for concept in core_concepts:
        content += f"- {concept}\n"

    content += "\n### 理论框架\n"
    theories = knowledge_system.get('theories', [])
    for theory in theories:
        content += f"- {theory}\n"

    # 分析框架
    content += "\n## 分析框架\n"
    steps = analysis_framework.get('steps', [])
    for i, step in enumerate(steps, 1):
        content += f"### Step {i}: {step.get('name', '步骤' + str(i))}\n"
        content += f"{step.get('description', '')}\n\n"

    # 决策启发式
    content += "## 决策启发式\n"
    for rule in decision_rules:
        condition = rule.get('condition', '')
        action = rule.get('action', '')
        content += f"- 如果{condition} → {action}\n"

    # 伦理边界
    content += "\n## 职业伦理与边界\n"
    content += "### 必须做的事\n"
    for must in ethics.get('must', []):
        content += f"- {must}\n"

    content += "\n### 绝对不做的事\n"
    for must_not in ethics.get('must_not', []):
        content += f"- {must_not}\n"

    content += "\n### 能力边界\n"
    for boundary in ethics.get('boundaries', []):
        content += f"- {boundary}\n"

    # 表达规范
    content += "\n## 表达规范\n"
    style = expression_style
    content += f"### 语言风格\n{style.get('language', '专业严谨')}\n\n"
    content += f"### 输出格式\n{style.get('format', '结构化报告')}\n\n"
    content += f"### 详细程度\n{style.get('detail', '适中')}\n\n"

    # 回答工作流
    content += "## 回答工作流\n"
    content += """遇到问题时，按照以下步骤行动：
1. 理解用户需求，识别问题的职业属性
2. 运用分析框架进行系统化分析
3. 检查是否涉及伦理边界
4. 运用决策启发式快速判断
5. 给出专业建议，注意表达规范
6. 如超出能力边界，明确说明局限性
"""

    # 诚实边界
    content += "\n## 诚实边界\n"
    content += f"""本Skill基于{expert_name}的标准化知识体系构建。
- 不替代真实专业人士的法律/医疗等专业建议
- 知识更新依赖外部资源，可能存在滞后性
- 复杂案例建议咨询人类专家
- 对待敏感问题保持客观中立
"""

    return content


def main():
    parser = argparse.ArgumentParser(description='生成职业专家SKILL.md文件')
    parser.add_argument('--expert_name', required=True, help='专家名称')
    parser.add_argument('--knowledge_system', required=True,
                       help='JSON格式知识体系')
    parser.add_argument('--analysis_framework', required=True,
                       help='JSON格式分析框架')
    parser.add_argument('--decision_rules', required=True,
                       help='JSON格式决策规则')
    parser.add_argument('--ethics', required=True,
                       help='JSON格式伦理边界')
    parser.add_argument('--expression_style', required=True,
                       help='JSON格式表达风格')
    parser.add_argument('--output_path', required=True, help='输出文件路径')

    args = parser.parse_args()

    try:
        # 解析JSON参数
        knowledge_system = json.loads(args.knowledge_system)
        analysis_framework = json.loads(args.analysis_framework)
        decision_rules = json.loads(args.decision_rules)
        ethics = json.loads(args.ethics)
        expression_style = json.loads(args.expression_style)

        # 生成描述
        description = f"{args.expert_name}专家：提供专业的{knowledge_system.get('domain', '该领域')}分析与建议"

        # 生成完整内容
        yaml_frontmatter = generate_yaml_frontmatter(args.expert_name, description)
        skill_content = generate_skill_content(
            args.expert_name, knowledge_system, analysis_framework,
            decision_rules, ethics, expression_style
        )

        full_content = yaml_frontmatter + "\n" + skill_content

        # 写入文件
        output_path = Path(args.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(full_content, encoding='utf-8')

        result = {
            "status": "success",
            "message": "SKILL.md生成成功",
            "output_path": str(output_path.absolute()),
            "expert_name": args.expert_name
        }
        print(json.dumps(result, ensure_ascii=False))

    except json.JSONDecodeError as e:
        result = {
            "status": "error",
            "message": f"JSON解析失败: {str(e)}"
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        result = {
            "status": "error",
            "message": f"生成失败: {str(e)}"
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
