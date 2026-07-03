---
name: agent-decision
description: AI Agent开发决策辅助系统。用户提出Agent应用想法，自动从技术选型、竞品格局、市场前景、行业趋势、开发可行性、系统稳定性、成本预算、推广策略8大维度进行综合分析，生成专业交互式HTML可行性决策报告。覆盖LLM选型/Agent框架/架构模式/幻觉控制/Token成本/RAG方案/Prompt工程/评测体系等Agent开发专属议题。触发词：Agent决策, Agent可行性, Agent开发, 做Agent应用, AI Agent评估, 智能体决策, 搭建Agent, Agent分析报告, agent decision, AI助手开发, 多智能体系统, Agent选型。
version: "1.0.0"
agent_created: true
agent_tools: Read, Write, Edit, Bash, WebFetch, WebSearch, Grep
metadata:
  openclaw:
    requires:
      bins:
        - python
    emoji: "🤖"
    homepage: https://github.com/bettermen/agent-decision
---

# AI Agent 开发决策辅助系统

## 概述

本技能为 AI Agent 应用开发提供专业的多维度可行性决策分析。用户只需提供 Agent 产品名称和应用方向，系统自动完成市场调研、技术评估、竞品分析、成本估算，生成专业的交互式可视化 HTML 决策报告。

## 核心能力

1. **技术选型分析** — LLM/GPT 模型对比选型、Agent 框架评估（LangChain/CrewAI/Dify/Coze/AutoGPT）、架构模式推荐
2. **竞品格局分析** — 搜索同类 Agent 产品、头部竞品拆解、差异化机会识别
3. **市场前景分析** — Agent 市场规模、增长率、细分赛道机会、政策环境
4. **行业趋势分析** — Agent 技术发展趋势、落地场景演进、投资热度
5. **开发可行性评估** — 技术难度、团队能力匹配、开发周期预估、技术债务风险
6. **系统稳定性方案** — 幻觉控制策略、可靠性保障、异常处理机制、质量监控体系
7. **成本预算估算** — LLM API Token 成本、服务器/向量数据库、人力投入、总 TCO
8. **推广策略建议** — GTM 策略、冷启动方案、定价模式、渠道选择
9. **综合可行性评分** — 8 维度加权评分、交互式雷达图、风险矩阵

## 使用方式

```
触发词 + Agent产品名称 + 应用方向描述
```

示例：
- "Agent决策：做一个AI客服多智能体系统"
- "帮我评估做AI法律咨询Agent可行吗"
- "分析AI编程助手Agent的可行性"
- "Agent可行性分析：做一个电商智能导购Agent"

## 工作流程

### 第一阶段：数据采集（并行搜索）

使用 WebSearch 工具并行搜索以下维度：

1. **技术生态**：搜索 `{产品方向} Agent LLM 技术选型 框架 LangChain CrewAI 2025 2026`
2. **竞品分析**：搜索 `{产品方向} AI Agent 竞品 产品 排行榜`
3. **市场数据**：搜索 `AI Agent 市场规模 增长率 2025 2026 预测`
4. **行业趋势**：搜索 `AI Agent 行业应用 趋势 落地场景 2025 2026`
5. **成本估算**：搜索 `LLM API Token 价格 成本 对比 GPT Claude DeepSeek 2025 2026`
6. **商业模式**：搜索 `AI Agent 商业模式 定价 变现 SaaS 2025`

### 第二阶段：深度分析（可选WebFetch）

对关键搜索结果中数据丰富的页面进行 WebFetch 获取详细信息。

### 第三阶段：报告生成

运行报告生成脚本生成交互式 HTML 报告：

```bash
python {baseDir}/scripts/report_generator.py \
  --name "产品名称" \
  --direction "产品方向" \
  --output "output_path.html" \
  --scores '{"tech_maturity":75,"competition":65,"market":80,"industry_fit":70,"dev_feasibility":75,"stability":68,"cost_control":72,"promotion":65}' \
  --tech '{"llm_options":[...],"frameworks":[...],"architecture":"...","detail":"..."}' \
  --competitors '{"count":45,"top3":[...],"saturation":"中等","detail":"..."}' \
  --market '{"size":"471亿","growth":"38%","forecast":"...","detail":"..."}' \
  --industry '{"trend":"快速上升","hot_scenarios":[...],"detail":"..."}' \
  --feasibility '{"difficulty":"中等","team_match":"高","timeline":"3-4个月","risks":[...],"detail":"..."}' \
  --stability '{"hallucination_control":"...","reliability":"...","monitoring":"...","detail":"..."}' \
  --cost '{"api_monthly":"5000-20000","infra":"3000-8000","labor":"5-15万/月","total_annual":"30-80万","detail":"..."}' \
  --promotion '{"gtm":"...","channels":[...],"pricing":"...","detail":"..."}'
```

或者直接在 Python 中调用：

```python
import json, sys
sys.path.insert(0, '{baseDir}/scripts')
from report_generator import generate_report

data = {
    "name": "产品名称",
    "direction": "产品方向",
    "scores": {...},
    "tech": {...},
    "competitors": {...},
    "market": {...},
    "industry": {...},
    "feasibility": {...},
    "stability": {...},
    "cost": {...},
    "promotion": {...}
}

html = generate_report(data)
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

## 报告结构

生成的 HTML 报告包含以下章节：

1. **封面页** — 产品名称、评估时间、总体评分、决策建议徽章
2. **执行摘要** — 核心结论与建议（可行/谨慎/暂缓/不建议）
3. **八维度雷达图** — 交互式 Canvas 雷达图，直观展示各维度优劣势
4. **技术选型分析** — LLM 模型对比表、Agent 框架选型矩阵、推荐架构
5. **竞品格局分析** — 竞品数量、头部玩家、市场饱和度、蓝海机会
6. **市场前景分析** — 市场规模、增长率、细分赛道机会
7. **行业趋势分析** — 技术成熟度曲线、落地场景热度、投资风向
8. **开发可行性评估** — 技术难度评级、团队匹配度、开发周期、里程碑建议
9. **系统稳定性方案** — 幻觉控制、可靠性设计、Prompt 版本管理、评测体系
10. **成本预算估算** — API Token 月度/年度成本、基础设施、人力 TCO
11. **推广策略建议** — GTM 路径、冷启动方案、定价策略、渠道矩阵
12. **风险矩阵** — 技术/市场/竞争/合规/运营 5 类风险评级
13. **综合决策建议** — 加权评分汇总、分阶段行动路线图

## 评分模型

基于以下 8 个维度加权评分（满分 100）：

| 维度 | 权重 | 评估标准 |
|------|------|----------|
| 技术成熟度 | 15% | LLM 能力匹配度、框架生态完善度、开源替代方案可用性 |
| 竞品格局 | 15% | 同类 Agent 产品数量、头部集中度、差异化空间 |
| 市场前景 | 15% | Agent 市场规模、细分赛道增长、用户付费意愿 |
| 行业适配 | 10% | Agent 能力与行业需求契合度、可替代传统方案的程度 |
| 开发可行性 | 15% | 技术难度、团队 LLM/AI 能力、开发周期合理性 |
| 系统稳定性 | 10% | 幻觉可控性、多轮对话一致性、异常恢复能力 |
| 成本可控性 | 10% | API Token 成本可控性、规模化边际成本、ROI 预期 |
| 推广潜力 | 10% | 产品自传播性、GTM 清晰度、商业模式可行性 |

评分等级：
- ≥80分：✅ **强烈建议做** — 技术成熟，市场明确，ROI 乐观
- 65-79分：🟡 **谨慎推进** — 有机会但需差异化或技术验证
- 50-64分：⚠️ **暂缓观望** — 先做 MVP 验证核心假设
- <50分：❌ **不建议做** — 技术/市场/成本有重大风险

## Agent 开发核心技术决策速查

| 决策项 | 选项 | 适用场景 | 风险提示 |
|--------|------|----------|----------|
| **LLM 选型** | GPT-4o / Claude 3.5 / DeepSeek-V3 / Qwen / Gemini | 按精度/成本/延迟三角权衡 | 单模型依赖风险，建议多模型 fallback |
| **Agent 框架** | LangChain / CrewAI / Dify / Coze / 自研 | LangChain灵活/CrewAI多智能体/Dify低代码 | 框架锁定风险，自研维护成本高 |
| **架构模式** | 单Agent / 多Agent协作 / RAG+Agent / 工作流编排 | 简单/复杂/知识密集型/流程化 | 多Agent调试难，RAG召回质量决定上限 |
| **记忆方案** | 会话窗口 / 摘要记忆 / 向量记忆 / 图谱记忆 | 短/长/语义/关系型上下文 | 记忆越长token成本越高 |
| **评测体系** | 人工评测 / LLM-as-Judge / 自动化回归 / 用户反馈 | 不同阶段的评测需求 | 评测覆盖率不足导致线上事故 |
| **部署方式** | API 服务 / 自托管模型 / 边缘部署 | 不同成本/延迟/隐私需求 | 自托管需要GPU资源，冷启动慢 |

## 注意事项

1. LLM API 价格波动频繁，成本估算需留 30% 缓冲
2. Agent 产品同质化严重，差异化定位是关键决策点
3. 幻觉问题仍是 Agent 商业化的最大技术瓶颈
4. 监管政策（AI 生成内容标识、数据安全）持续收紧
5. 最终决策需结合团队实际 AI 能力与资源判断
