---yaml
name: agency-agents
description: AI Agent 团队 - 61 个专业 Agent，8 大部门，完整的 AI 代理机构。支持单 Agent 使用和多 Agent 协作编排。
version: 1.0.0
author: Jerry (based on agency-agents by @msitarzewski)
license: MIT
tags: [ai-agents, automation, productivity, enterprise]
---

# AI Agent 团队 - OpenClaw 技能

## 📦 技能概述

本技能提供 61 个专业 AI Agent，分为 8 大业务部门，可独立完成专业任务或多 Agent 协作完成复杂项目。

## 🎯 使用方式

### 方式 1：使用单个 Agent

```bash
# 语法
/openclaw skill use agency-agents --agent <agent-name> "<任务描述>"

# 示例
/openclaw skill use agency-agents --agent frontend-developer "帮我创建一个 React 登录页面组件"
/openclaw skill use agency-agents --agent growth-hacker "为我的 SaaS 产品设计增长策略"
/openclaw skill use agency-agents --agent ui-designer "审查我的网站设计并提供改进建议"
```

### 方式 2：使用 Agent 编排器（推荐）

```bash
# 自动调度多个 Agent 完成复杂项目
/openclaw skill use agency-agents --agent orchestrator "开发一个完整的电商网站，包括前端、后端和营销策略"
```

### 方式 3：使用整个部门

```bash
# 激活整个部门的 Agent 协作
/openclaw skill use agency-agents --department engineering "开发一个完整的 Web 应用"
/openclaw skill use agency-agents --department marketing "策划并执行一次营销活动"
```

## 🏢 可用部门

| 部门 | Agent 数量 | 用途 |
|------|-----------|------|
| engineering | 7 | 工程开发 |
| design | 7 | 设计相关 |
| marketing | 8 | 市场营销 |
| product | 3 | 产品管理 |
| project-management | 5 | 项目管理 |
| testing | 7 | 测试 QA |
| support | 6 | 业务支持 |
| specialized | 6 | 专业领域 |

## 🎭 可用 Agent

### 💻 工程部
- `frontend-developer` - 前端开发专家（React/Vue/Angular）
- `backend-architect` - 后端架构师（API/数据库/云）
- `mobile-app-builder` - 移动端开发（iOS/Android/跨平台）
- `ai-engineer` - AI 工程师（ML/深度学习/AI 集成）
- `devops-automator` - DevOps 自动化（CI/CD/基础设施）
- `rapid-prototyper` - 快速原型（MVP/POC）
- `senior-developer` - 高级开发（复杂实现/架构决策）

### 🎨 设计部
- `ui-designer` - UI 设计师（视觉/组件/设计系统）
- `ux-researcher` - UX 研究员（用户研究/可用性测试）
- `ux-architect` - UX 架构师（技术架构/CSS 系统）
- `brand-guardian` - 品牌守护者（品牌策略/一致性）
- `visual-storyteller` - 视觉叙事者（视觉故事/多媒体）
- `whimsy-injector` - 趣味注入师（微交互/品牌个性）
- `image-prompt-engineer` - 图像提示工程师（AI 图像生成）

### 📢 市场部
- `growth-hacker` - 增长黑客（用户获取/转化优化）
- `content-creator` - 内容创作者（多平台内容/编辑日历）
- `twitter-engager` - Twitter 互动专家（实时互动/思想领导）
- `tiktok-strategist` - TikTok 策略师（病毒内容/算法优化）
- `instagram-curator` - Instagram 策划师（视觉叙事/社群）
- `reddit-community-builder` - Reddit 社群建设者（社群运营）
- `app-store-optimizer` - 应用商店优化师（ASO/转化）
- `social-media-strategist` - 社交媒体策略师（跨平台策略）

### 📊 产品部
- `sprint-prioritizer` - 冲刺优先级专家（敏捷规划）
- `trend-researcher` - 趋势研究员（市场情报/竞争分析）
- `feedback-synthesizer` - 反馈整合师（用户反馈分析）

### 🎬 项目管理部
- `studio-producer` - 工作室制作人（高层协调/组合管理）
- `project-shepherd` - 项目协调员（跨职能协调）
- `studio-operations` - 工作室运营（日常效率/流程优化）
- `experiment-tracker` - 实验追踪师（A/B 测试）
- `senior-pm` - 高级项目经理（范围规划/任务分解）

### 🧪 测试部
- `evidence-collector` - 证据收集师（截图 QA/视觉验证）
- `reality-checker` - 现实检查员（质量认证/发布审批）
- `test-results-analyzer` - 测试结果分析师（测试评估）
- `performance-benchmarker` - 性能基准师（性能测试）
- `api-tester` - API 测试师（API 验证/集成测试）
- `tool-evaluator` - 工具评估师（技术评估）
- `workflow-optimizer` - 工作流优化师（流程分析）

### 🛟 支持部
- `support-responder` - 客服响应师（客户服务）
- `analytics-reporter` - 分析报告师（数据分析/仪表板）
- `finance-tracker` - 财务追踪师（财务规划/预算）
- `infrastructure-maintainer` - 基础设施维护师（系统可靠性）
- `legal-compliance-checker` - 法律合规师（合规/法规）
- `executive-summary-generator` - 高管摘要生成师（C -suite 沟通）

### 🎯 特别部门
- `orchestrator` - Agent 编排器（多 Agent 调度核心）
- `data-analytics-reporter` - 数据分析报告师（商业智能）
- `lsp-index-engineer` - LSP/索引工程师（代码智能）
- `sales-data-extraction-agent` - 销售数据提取师
- `data-consolidation-agent` - 数据整合师
- `report-distribution-agent` - 报告分发师

## 🔄 核心工作流

### 单 Agent 工作流

```
1. 用户指定 Agent 和任务
2. 加载对应 Agent 人格和专业知识
3. 执行任务并输出专业结果
4. 提供可交付成果
```

### 多 Agent 编排工作流

```
1. 项目分析阶段
   └─→ 高级项目经理：任务分解
   
2. 架构设计阶段
   └─→ 架构师：技术架构设计
   
3. 开发实施阶段（循环）
   ├─→ 开发工程师：实现任务
   └─→ 测试工程师：质量验证
   └─→ （如失败）→ 返回开发重试
   
4. 集成测试阶段
   └─→ 现实检查员：最终质量认证
   
5. 交付阶段
   └─→ 生成完整交付文档
```

## 📋 输出格式

### 标准输出

```markdown
# [Agent 名称] - [任务类型]

## 🎯 任务理解
[对任务的理解和分析]

## 📋 执行过程
[详细的工作步骤]

## 📦 交付成果
[具体的交付物，如代码、文档、策略等]

## ✅ 质量检查
[自我验证和质量保证]

## 💡 建议
[后续优化建议]
```

### 编排器输出

```markdown
# 项目完成报告

## 📊 项目概览
- 总任务数：X
- 完成时间：Y
- 参与 Agent：Z

## ✅ 完成情况
[所有任务的完成状态]

## 📦 交付清单
[所有交付物的列表和链接]

## 📈 质量报告
[整体质量评估和各项指标]
```

## ⚙️ 配置选项

### 环境变量

```bash
# 设置默认部门
AGENCY_AGENTS_DEFAULT_DEPARTMENT=engineering

# 设置质量检查严格度（1-5）
AGENCY_AGENTS_QA_LEVEL=3

# 设置最大重试次数
AGENCY_AGENTS_MAX_RETRIES=3

# 启用详细日志
AGENCY_AGENTS_VERBOSE=true
```

## 🎯 最佳实践

### 1. 选择合适的 Agent

- **明确任务类型** → 选择对应专业 Agent
- **复杂项目** → 使用编排器
- **需要多领域** → 使用部门协作

### 2. 提供清晰的任务描述

```bash
# ❌ 模糊
"帮我做个网站"

# ✅ 清晰
"帮我创建一个电商网站的前端，使用 React + Tailwind CSS，需要包含首页、商品列表、购物车、结账页面，要求响应式设计，支持移动端"
```

### 3. 迭代优化

- 第一次输出后提供反馈
- 让 Agent 调整和改进
- 必要时切换 Agent 获取不同视角

### 4. 质量保证

- 使用测试部 Agent 进行验证
- 关键项目使用现实检查员最终审核
- 重要决策使用多个 Agent 交叉验证

## 🔧 故障排除

### 常见问题

**Q: Agent 输出不符合预期？**
A: 提供更详细的任务描述，包括具体要求、技术栈、示例等

**Q: 多 Agent 协作效率低？**
A: 使用编排器自动调度，或手动指定 Agent 顺序

**Q: 需要特定领域专业知识？**
A: 选择对应部门的 Agent，或联系支持获取定制建议

## 📞 技术支持

- 📧 Email: support@your-company.com
- 💬 Discord: 加入社区获取帮助
- 📚 文档：完整使用指南

## 📄 许可证

MIT License - 基于 [agency-agents](https://github.com/msitarzewski/agency-agents) 项目改造
