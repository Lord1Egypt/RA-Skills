#!/usr/bin/env python3
"""重新生成最终报告的第二部分"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    # 加载筛选后的论文
    import json
    with open('v9_papers_filtered.json', 'r') as f:
        papers = json.load(f)
    
    print(f"加载了 {len(papers)} 篇筛选后的论文")
    
    # 第二部分
    prompt = """继续完成这份报告，从"3. 控费价值传导机制"开始，后续部分完整写完：

## 3. 控费价值传导机制

### 3.1 完整传导链

```
AI能力提升 
→ 诊疗效率优化（问诊加速、准确率提升）
→ 各个环节成本节约
→ 最终医保/商保总支出减少
```

### 3.2 各环节量化节约总结
请分点写出，每个环节一句话总结量化数据（基于文献研究）：
- 初筛分诊：节约多少？
- 检查/检验推荐：减少多少不必要检查？
- 重症早期预警：降低多少长期成本？
- 慢病持续管理：减少多少并发症？
- 理赔审核：减少多少欺诈和过度理赔？

### 4. 关键发现总结

请分点回答：
1. AI大模型相对传统方法的核心技术进步是什么？
2. 哪些临床场景AI已经达到商用水平，可以落地？
3. 哪些场景还需要进一步发展，不能完全依赖AI？

### 5. 对商业保险行业的具体建议

请分时间阶段给出具体建议：
- **短期（0-1年）**：优先布局什么场景？为什么？
- **中期（1-3年）**：需要建设什么核心能力？
- **长期（3年以上）**：怎么构建完整的AI控费生态？

### 6. 未来研究方向

还有哪些开放问题需要进一步研究？请列出3-5个。

请用中文回答，结构完整，写完所有部分。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v9.0-20260324/'
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n[生成最终报告第二部分...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '04_final_part2.md')
    
    if report:
        print(f"\n✅ 第二部分已保存，长度: {len(report)} 字符")
        lines = report.count('\n')
        print(f"   行数: {lines}")
    
    # 现在合并两部分
    print("\n[合并最终报告...]")
    with open(output_dir + '04_final_integrated_report.md', 'r') as f:
        part1 = f.read()
    
    # 找到截断位置，截断之前的内容
    lines_part1 = part1.split('\n')
    # 找到"### 3.1 完整传导链"之后截断
    new_part1 = []
    for line in lines_part1:
        if '### 3.1 完整传导链' in line:
            break
        new_part1.append(line)
    
    # 添加完整的3.1
    new_part1.append('### 3.1 完整传导链')
    new_part1.append('')
    new_part1.append('```')
    new_part1.append('AI能力提升 ')
    new_part1.append('→ 诊疗效率优化（问诊加速、准确率提升）')
    new_part1.append('→ 各个环节成本节约')
    new_part1.append('→ 最终医保/商保总支出减少')
    new_part1.append('```')
    new_part1.append('')
    
    full_report = '\n'.join(new_part1) + '\n' + report
    
    with open(output_dir + '04_final_integrated_report.md', 'w') as f:
        f.write(full_report)
    
    print(f"\n✅ 完整最终报告已合并保存")
    total_lines = full_report.count('\n')
    print(f"   总行数: {total_lines}")
    
    return full_report

if __name__ == '__main__':
    main()
