# Fund Advisor Agent

场外公募基金配置顾问 Agent，具备10年实战投资经验的资深理财经理角色。

## 功能特性

- 📊 **基金数据查询**: 实时查询基金净值、业绩、基金经理信息
- 🎯 **组合配置**: 基于投资者画像的个性化配置方案
- 📈 **风险评估**: VaR、夏普比率、最大回撤等风险指标
- 💰 **定投服务**: 智能定投计算、计划管理、止盈策略
- 🔔 **市场监控**: 估值预警、异动监控、消息推送
- 📄 **报告生成**: PDF/Word/Excel 专业报告
- 📚 **投资教育**: 知识库、学习进度、投资日记

## 技术架构

- **框架**: LangChain + LangGraph
- **技能**: web-search, document-generation, knowledge, feishu-message
- **工具**: 87个专业工具函数
- **存储**: MemorySaver + 文件系统 + S3

## 快速开始

```python
from src.agents.agent import build_agent

# 构建 Agent
agent = build_agent()

# 运行
response = agent.invoke({
    "messages": [
        ("user", "帮我配置一个稳健型基金组合，20万资金，3年期限")
    ]
})
```

## 文档目录

- [主文档](./SKILL.md) - 完整的 Skill 文档
- [工具开发规范](./references/tool-development.md) - 工具函数开发指南
- [技能集成指南](./references/skill-integration.md) - Skills 使用说明
- [Agent 最佳实践](./references/agent-best-practices.md) - Agent 构建指南
- [数据存储方案](./references/data-storage.md) - 数据管理策略
- [使用示例](./examples/usage-examples.md) - 常见场景示例

## 目录结构

```
fund-advisor/
├── SKILL.md                          # 主文档
├── README.md                         # 本文件
├── references/                       # 技术参考文档
│   ├── tool-development.md           # 工具开发规范
│   ├── skill-integration.md          # 技能集成指南
│   ├── agent-best-practices.md        # Agent 最佳实践
│   └── data-storage.md               # 数据存储方案
└── examples/                         # 使用示例
    └── usage-examples.md             # 场景示例代码
```

## 版本

- **版本号**: 1.0.0
- **发布日期**: 2026-04-03
- **作者**: AI Assistant
- **许可**: MIT License

## 依赖

- coze-coding-dev-sdk >= 0.5.11
- langchain >= 1.0
- langgraph >= 1.0
- requests

## 使用许可

MIT License - 详见 [LICENSE](./LICENSE)
