---
name: crewai-team
description: 使用 CrewAI 多 Agent 团队进行产品需求分析和 PRD 生成
metadata: {"clawdbot":{"emoji":"👥","requires":{"bins":["python3.10"]}}}
---

# CrewAI 团队协作技能

## 概述

本技能调用 CrewAI 多 Agent 团队，进行完整的产品需求分析，输出标准 PRD 文档。

## 团队成员

| 角色 | 职责 |
|------|------|
| 📊 市场调研分析师 | 竞品分析、用户研究 |
| 🎨 产品设计专家 | 功能设计、UI 建议 |
| 🏗️ 技术总监 | 架构设计、任务拆分 |
| 💻 全栈技术专家 | 代码实现示例 |
| ✅ 质量专家 | 测试计划、验收标准 |

## 使用方法

### 方式 1：直接运行脚本

```bash
cd ~/.openclaw/workspace/crewai_team
python3.10 run_team.py "产品创意描述"
```

### 方式 2：通过 OpenClaw 子代理

```python
sessions_spawn(
    task="用 CrewAI 分析产品需求：[产品创意]",
    runtime="subagent",
    cwd="/Users/dayangyu/.openclaw/workspace/crewai_team"
)
```

### 方式 3：Python 代码调用

```python
from crewai_team.team_config import create_product_team

crew = create_product_team("产品创意", verbose=True)
result = crew.kickoff()
```

## 输出

完整的 PRD 文档，包含：
- 市场调研报告
- 产品设计方案
- 技术架构方案
- 开发指南
- 质量保障计划

## 前置条件

1. 安装 CrewAI: `python3.10 -m pip install crewai crewai-tools`
2. 配置 API Key: 复制 `.env.example` 为 `.env` 并填入 DashScope API Key

## 注意事项

- 首次运行需要 5-10 分钟（依赖下载 + 多轮分析）
- 确保有足够的 API 额度
- 输出结果建议人工审核
