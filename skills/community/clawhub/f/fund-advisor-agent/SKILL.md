---
name: fund-advisor
description: 场外公募基金配置顾问 Agent Skill，具备10年实战投资经验的资深理财经理角色，提供基金数据查询、组合配置、风险评估、市场监控、投资教育等一站式专业理财服务。支持 web-search、document-generation、knowledge、feishu-message 四大技能集成。
license: MIT
tags: ["fund-investment", "wealth-management", "financial-advisor", "portfolio-management", "ai-agent"]
author: "AI Assistant"
version: "1.0.0"
keywords: ["基金投资", "理财顾问", "资产配置", "风险评估", "智能投顾"]
requirements: ["coze-coding-dev-sdk>=0.5.11", "langchain>=1.0", "langgraph>=1.0"]
platform: "coze-coding"
---

# 场外公募基金配置顾问 Agent

具备10年实战投资经验的资深理财经理角色，专注基金资产配置与风险管理。

## 核心定位

基于 LangChain/LangGraph 框架构建的智能投顾 Agent，通过 87 个专业工具函数提供从基金筛选、组合配置、风险评估、市场监控到投资教育的全流程专业服务。

## 技能集成

本 Skill 深度集成了以下四大核心技能：

| 技能 | 功能描述 | 集成的工具数量 |
|------|---------|---------------|
| **web-search** | 实时获取基金净值、业绩、基金经理、市场估值等数据 | 10个工具 |
| **document-generation** | 生成 PDF/DOCX/Excel 专业报告 | 4个工具 |
| **knowledge** | 基金投资知识库语义搜索与管理 | 4个工具 |
| **feishu-message** | 飞书消息推送（投资提醒、市场预警等） | 6个工具 |

## 核心能力

### 1. 基金数据查询与分析
- 基金净值、业绩、排名实时查询
- 基金经理信息与管理能力评估
- 基金筛选（按类型、公司、主题）
- 市场估值与温度查询
- 行业轮动与资金流向监控

### 2. 组合配置与管理
- 基于投资者画像的个性化配置方案
- 多基金对比分析（业绩、风险、持仓）
- 基金持仓与行业配置分析
- 组合收益计算与表现跟踪
- 收益归因分析

### 3. 风险评估与控制
- VaR 与夏普比率计算
- 最大回撤模拟
- 组合分散化分析
- 智能调仓与再平衡建议

### 4. 定投策略服务
- 定投收益智能计算
- 多种定投场景对比
- 定投计划创建与管理
- 智能止盈策略

### 5. 市场监控预警
- 市场涨跌预警
- 估值极端位置提醒
- 基金经理变更监控
- 基金规模与分红异动监控

### 6. 报告生成服务
- PDF 格式投资报告
- Word 格式配置方案
- Excel 格式数据明细

### 7. 消息通知服务
- 飞书 Webhook 集成
- 投资提醒推送
- 市场预警通知
- 定投扣款提醒

### 8. 投资教育与日记
- 投资知识课程生成
- 模拟投资场景
- 投资日记记录与分析
- 学习进度跟踪

## 快速开始

### 基本使用

```python
from src.agents.agent import build_agent

# 构建 Agent
agent = build_agent()

# 运行 Agent
result = agent.invoke({
    "messages": [
        ("user", "我想要配置一个稳健型的基金组合，可用资金20万，投资期3年")
    ]
})

print(result)
```

### 典型对话场景

#### 场景1：基金数据查询
```
用户：帮我查询一下易方达蓝筹精选（005827）的最新净值和业绩
Agent：使用 query_fund_data 工具查询，返回最新净值 1.7699元，近一年涨幅等数据
```

#### 场景2：组合配置
```
用户：中低风险，3年投资期，20万资金，请给我一个配置方案
Agent：综合分析后给出配置建议（债券70% + 股票30%），并详细说明选基逻辑
```

#### 场景3：定投计划
```
用户：我想开始定投沪深300指数，每月投2000元，请帮我计算收益
Agent：使用 calculate_sip_returns 工具计算，输出详细的收益测算和策略建议
```

## 工具使用规范

### 工具调用原则

1. **技能优先**：优先使用集成的 Skills（web-search、document-generation 等）
2. **按需调用**：仅在需要外部数据时才调用工具，避免冗余
3. **链路追踪**：使用 `new_context()` 获取请求上下文
4. **错误处理**：所有工具调用必须有异常捕获和友好提示

### 工具分类使用指南

#### 数据查询类（使用 web-search）
- `query_fund_data` - 查询基金净值、业绩
- `query_fund_performance` - 查询历史业绩
- `query_fund_manager` - 查询基金经理信息
- `query_market_valuation` - 查询市场估值

#### 报告生成类（使用 document-generation）
- `generate_portfolio_pdf_report` - 生成 PDF 报告
- `generate_allocation_excel` - 生成 Excel 配置表

#### 知识管理类（使用 knowledge）
- `search_fund_knowledge` - 搜索投资知识
- `get_investment_tips` - 获取投资建议

#### 消息推送类（使用 feishu-message）
- `setup_feishu_notification` - 配置飞书通知
- `send_market_alert_notification` - 发送市场预警

## 配置说明

### 依赖安装

```bash
# 核心依赖
coze-coding-dev-sdk>=0.5.11
langchain>=1.0
langgraph>=1.0

# 可选依赖
requests  # 用于 HTTP 请求
```

### 环境变量

```bash
# 模型配置（通过 coze_workload_identity 获取）
COZE_WORKLOAD_IDENTITY_API_KEY
COZE_INTEGRATION_MODEL_BASE_URL

# 飞书 Webhook（通过 coze_workload_identity 获取）
FEISHU_WEBHOOK_URL
```

### Agent 配置文件

配置文件位于 `config/agent_llm_config.json`：

```json
{
    "config": {
        "model": "doubao-seed-2-0-pro-260215",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_completion_tokens": 10000,
        "timeout": 600,
        "thinking": "disabled"
    },
    "sp": "# System Prompt...",
    "tools": ["tool1", "tool2", ...]
}
```

## 数据存储

### 存储方案
- **内存存储**：使用 `MemorySaver` 存储对话历史
- **文件存储**：用户数据、定投计划、投资日记等存储在 `/tmp` 目录
- **云存储**：报告文件自动上传到 S3，返回下载 URL

### 数据目录结构
```
/tmp/
├── user_profiles/       # 用户画像数据
├── sip_plans/          # 定投计划
├── market_alerts/      # 市场预警
├── fund_alerts/        # 基金异动
├── notifications/      # 消息通知配置
└── investment_diary/   # 投资日记
```

## 注意事项

### 1. 投资风险提示
- Agent 提供的建议仅供参考，不构成实际投资建议
- 市场有风险，投资需谨慎
- 过往业绩不代表未来表现

### 2. 数据时效性
- 基金净值数据为实时查询，可能存在轻微延迟
- 建议用户在做投资决策前，以官方数据为准

### 3. 合规性
- 不推荐具体基金产品代码，只提供配置方向和选基标准
- 所有建议需符合相关法律法规

### 4. 性能考虑
- 工具调用有超时限制（默认 600 秒）
- 建议控制单次对话的上下文长度
- 重要数据建议用户自行核实

## 技术架构

```
┌─────────────────────────────────────────┐
│          Fund Advisor Agent              │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐    │
│  │      System Prompt (SP)         │    │
│  │   10年实战投资经验理财经理角色   │    │
│  └─────────────────────────────────┘    │
│                   │                     │
│                   ▼                     │
│  ┌─────────────────────────────────┐    │
│  │      LLM (doubao-seed)          │    │
│  │   决策引擎 + 工具调用编排       │    │
│  └─────────────────────────────────┘    │
│                   │                     │
│        ┌──────────┼──────────┐          │
│        ▼          ▼          ▼          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ web-     │ │document- │ │knowledge │  │
│  │ search   │ │generation│ │          │  │
│  └──────────┘ └──────────┘ └──────────┘  │
│        │          │          │          │
│        └──────────┴──────────┘          │
│                   │                     │
│                   ▼                     │
│  ┌─────────────────────────────────┐    │
│  │   87个专业工具函数              │    │
│  │   基金查询 / 组合管理 / 风险评估 │    │
│  │   市场监控 / 报告生成 / 消息推送 │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## 版本历史

### v1.0.0 (2026-04-03)
- 初始版本发布
- 支持 87 个专业工具函数
- 集成 4 大核心技能
- 提供完整的基金投资顾问服务

## 作者与许可

- **作者**: AI Assistant
- **许可**: MIT License
- **版本**: 1.0.0

## 参考文档

- [工具开发规范](./references/tool-development.md)
- [技能集成指南](./references/skill-integration.md)
- [Agent 构建最佳实践](./references/agent-best-practices.md)
- [数据存储方案](./references/data-storage.md)
