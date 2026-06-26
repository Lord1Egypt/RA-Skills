#!/usr/bin/env python3
"""
补充：案例分析 + 国际对比
配置：minimax-m2.5 + 64k max_tokens
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')

from scripts.research_claw_bridge import ResearchTools

def main():
    tools = ResearchTools()
    
    import json
    with open('v9_papers_filtered.json', 'r') as f:
        papers = json.load(f)
    
    print(f"加载了 {len(papers)} 篇筛选后的论文")
    print(f"配置: minimax-m2.5 + 64k max_tokens")
    print(f"任务: 补充案例分析 + 国际对比")
    
    # 补充内容prompt
    prompt = """# AI大模型问诊诊疗价值深度研究 - 补充章节

## 11. 典型案例分析

请提供3-5个具体的AI问诊应用案例，每个案例包含：

### 案例1：儿科AI问诊（PediatricsGPT）

**应用场景**：
**核心功能**：
**实际效果**（具体数据）：
**控费价值**：

### 案例2：急诊骨折筛查

**应用场景**：
**核心功能**：
**实际效果**（具体数据）：
**控费价值**：

### 案例3：糖尿病视网膜病变筛查

**应用场景**：
**核心功能**：
**实际效果**（具体数据）：
**控费价值**：

### 案例4：保险理赔智能审核

**应用场景**：
**核心功能**：
**实际效果**（具体数据）：
**控费价值**：

### 案例5：慢病管理AI助手

**应用场景**：
**核心功能**：
**实际效果**（具体数据）：
**控费价值**：

---

## 12. 国际对比分析

### 12.1 中美AI医疗应用对比

| 维度 | 中国 | 美国 | 欧洲 | 分析 |
|------|------|------|------|------|
| **政策支持** | | | | |
| **技术应用成熟度** | | | | |
| **商业化进展** | | | | |
| **监管框架** | | | | |
| **医保覆盖** | | | | |

请完整填满表格。

### 12.2 典型公司/产品对比

| 公司/产品 | 国家 | 核心产品 | 应用场景 | 商业化程度 |
|----------|------|---------|---------|-----------|
| 平安好医生 | 中国 | | | |
| 阿里健康 | 中国 | | | |
| 腾讯健康 | 中国 | | | |
| Babylon Health | 英国 | | | |
| Ada Health | 德国 | | | |
| Babylon | 美国 | | | |

请完整填满表格。

### 12.3 中国市场的机遇与挑战

**机遇**：
1. 
2. 
3. 

**挑战**：
1. 
2. 
3. 

**建议**：
1. 
2. 
3. 

---

## 要求

1. 完整填写所有表格
2. 给出具体数据
3. 案例要有实际应用价值
4. 国际对比要客观

用markdown格式，用中文回答。完整输出所有内容。
"""
    
    output_dir = '/root/.openclaw/workspace/deep-research-knowledge-base/research/domains/insurance/cost-control/v11.0-20260324-final/'
    
    print("\n[生成案例分析 + 国际对比...]")
    
    report = tools.generate_survey_report(papers, prompt, output_path=output_dir + '01_case_studies_and_international_comparison.md')
    
    if report:
        print(f"\n✅ 补充章节已生成，长度: {len(report)} 字符")
        lines = report.count('\n')
        print(f"   行数: {lines}")
    
    return report

if __name__ == '__main__':
    main()
