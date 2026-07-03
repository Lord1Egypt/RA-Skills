# 🤖 Agent Decision - AI Agent 开发决策辅助系统

> 想做 Agent 应用？先看这份报告再动手。

## 是什么

输入你的 Agent 产品想法，自动从 **8 大维度** 进行综合分析，生成专业交互式 HTML 可行性决策报告。

### 8 维度评估

| 维度 | 权重 | 关注点 |
|------|------|--------|
| 🧠 技术成熟度 | 15% | LLM选型、框架生态、开源替代 |
| ⚔️ 竞品格局 | 15% | 同类Agent数、头部集中度、差异化 |
| 📈 市场前景 | 15% | 市场规模、增长、付费意愿 |
| 🎯 行业适配 | 10% | Agent与行业需求契合度 |
| 🔧 开发可行性 | 15% | 技术难度、团队匹配、周期 |
| 🛡️ 系统稳定性 | 10% | 幻觉控制、可靠性、监控 |
| 💰 成本可控性 | 10% | Token成本、边际成本、ROI |
| 🚀 推广潜力 | 10% | GTM路径、定价、获客 |

## 报告特色

- 🎨 **Canvas雷达图** — 8轴交互式雷达图
- 🌙 **暗色专业主题** — 深蓝科技感UI
- 📊 **LLM对比表** — GPT-4o/DeepSeek/Claude/Qwen
- 🏗️ **框架选型矩阵** — CrewAI/LangChain/Dify/自研
- ⚠️ **风险矩阵** — 6类风险识别与应对
- 🗺️ **行动路线图** — 4阶段实施计划

## 使用

### WorkBuddy 对话中

```
Agent决策：做一个AI法律咨询Agent
帮我评估做AI编程助手Agent可行吗
```

### CLI

```bash
python scripts/report_generator.py \
  --name "产品名称" --direction "方向" --output "report.html" \
  --scores '{"tech_maturity":75,...}' ...
```

### Python API

```python
from report_generator import generate_report
html = generate_report({"name": "...", "scores": {...}, ...})
```

## 评分等级

- ≥80分：✅ 强烈建议做
- 65-79分：🟡 谨慎推进
- 50-64分：⚠️ 暂缓观望
- <50分：❌ 不建议做

## 作为 WorkBuddy Skill 安装

放置到 `~/.workbuddy/skills/agent-decision/` 即可。
