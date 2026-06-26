#!/usr/bin/env python3
"""
Skill 评审报告生成工具
根据评审结果生成结构化的 Markdown 报告
"""

import sys
import json
from datetime import datetime
from pathlib import Path


def generate_report(skill_name, review_data, output_path=None):
    """
    生成评审报告
    
    Args:
        skill_name: Skill 名称
        review_data: 评审数据字典
        output_path: 输出路径（可选）
    """
    
    if output_path is None:
        date_str = datetime.now().strftime("%Y%m%d")
        output_dir = Path.cwd() / "skill-reviews"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{skill_name}-review-{date_str}.md"
    
    # 生成报告内容
    report = f"""# Skill 评审报告：{skill_name}

**评审日期**：{datetime.now().strftime("%Y-%m-%d")}  
**评审人**：AI Agent  

---

## 📊 结论概览

| 维度 | 评分 | 说明 |
|------|------|------|
| 可理解性 | {review_data.get('readability', 0)}/10 | 是否易于理解和执行 |
| Token 效率 | {review_data.get('token_efficiency', 0)}/10 | 上下文消耗是否合理 |
| 功能完备性 | {review_data.get('completeness', 0)}/10 | 是否覆盖核心场景 |
| 结构合理性 | {review_data.get('structure', 0)}/10 | 文件组织是否清晰 |
| **综合评分** | **{review_data.get('overall', 0)}/10** | 整体质量 |

---

## ✅ 优点

"""
    
    for i, strength in enumerate(review_data.get('strengths', []), 1):
        report += f"{i}. **{strength['title']}**  \n   {strength['description']}\n\n"
    
    report += "---\n\n## ⚠️ 存在的问题\n\n"
    
    # 分级问题
    for severity, emoji in [('critical', '🔴'), ('medium', '🟡'), ('minor', '🟢')]:
        issues = [i for i in review_data.get('issues', []) if i['severity'] == severity]
        if issues:
            severity_name = {'critical': '严重问题', 'medium': '中等问题', 'minor': '轻微问题'}[severity]
            report += f"### {emoji} {severity_name}\n\n"
            
            for idx, issue in enumerate(issues, 1):
                report += f"#### 问题 {idx}：{issue['title']}\n"
                report += f"- **位置**：{issue['location']}\n"
                report += f"- **描述**：{issue['description']}\n"
                report += f"- **影响**：{issue['impact']}\n"
                if 'example' in issue:
                    report += f"- **示例**：\n```markdown\n{issue['example']}\n```\n"
                report += "\n"
    
    report += "---\n\n## 🛠️ 优化计划\n\n"
    
    for idx, plan in enumerate(review_data.get('optimization_plans', []), 1):
        report += f"### 优化项 {idx}：{plan['title']}\n"
        report += f"- **类型**：{plan['type']}\n"
        report += f"- **具体步骤**：\n"
        for step in plan['steps']:
            report += f"  {step}\n"
        report += f"- **预期 Token 节省**：约 {plan['token_saved']} tokens\n"
        report += f"- **风险评估**：{plan['risk']}（{plan['risk_note']}）\n"
        if 'example' in plan:
            report += f"- **改进后示例**：\n```markdown\n{plan['example']}\n```\n"
        report += "\n"
    
    report += "---\n\n## 📈 Token 分析\n\n"
    report += "| 文件 | 当前 Token 数 | 优化后预估 | 节省比例 |\n"
    report += "|------|--------------|-----------|----------|\n"
    
    total_current = 0
    total_optimized = 0
    
    for item in review_data.get('token_analysis', []):
        current = item['current']
        optimized = item['optimized']
        saved_pct = round((1 - optimized/current) * 100, 1) if current > 0 else 0
        
        total_current += current
        total_optimized += optimized
        
        report += f"| {item['file']} | {current} | {optimized} | {saved_pct}% |\n"
    
    total_saved_pct = round((1 - total_optimized/total_current) * 100, 1) if total_current > 0 else 0
    report += f"| 总计 | {total_current} | {total_optimized} | **{total_saved_pct}%** |\n"
    
    report += "\n---\n\n## 🎯 优先级建议\n\n"
    report += f"1. **立即处理**：{', '.join(review_data.get('priority_immediate', ['无']))}\n"
    report += f"2. **中期优化**：{', '.join(review_data.get('priority_medium', ['无']))}\n"
    report += f"3. **长期改进**：{', '.join(review_data.get('priority_long', ['无']))}\n"
    
    report += "\n---\n\n## 📝 备注\n\n"
    if 'notes' in review_data:
        report += review_data['notes'] + "\n"
    else:
        report += "无特殊备注。\n"
    
    # 写入文件
    Path(output_path).write_text(report, encoding='utf-8')
    
    return output_path


def main():
    if len(sys.argv) < 2:
        print("用法: python generate_report.py <review_data.json> [output.md]")
        print("或传入 JSON 字符串作为第二个参数")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    # 判断是文件路径还是 JSON 字符串
    try:
        if Path(input_arg).exists():
            with open(input_arg, 'r', encoding='utf-8') as f:
                review_data = json.load(f)
            skill_name = review_data.get('skill_name', 'unknown-skill')
        else:
            review_data = json.loads(input_arg)
            skill_name = review_data.get('skill_name', 'unknown-skill')
    except json.JSONDecodeError:
        print("错误：无效的 JSON 数据")
        sys.exit(1)
    
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    result_path = generate_report(skill_name, review_data, output_path)
    print(f"✅ 报告已生成：{result_path}")


if __name__ == "__main__":
    main()
