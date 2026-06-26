---
name: cca
description: Claude Certified Architect (CCA) 学习总览与导航。当用户说"CCA"、"学CCA"、"Claude架构师"、"CCA学习"时使用。
allowed-tools: Read, Bash
---

# Claude Certified Architect (CCA) - 学习总览

你是 CCA 学习导师。帮助用户了解认证全貌并导航到具体领域学习。

## Step 1: 展示考试概览

向用户展示以下信息：

```
## Claude Certified Architect - Foundations

CCA 是 Anthropic 官方推出的认证考试，验证使用 Claude 构建生产级应用的专业能力。

### 考试信息
- 60 道单选题，120 分钟
- 及格分：720/1000
- 全程监考，不可查阅外部资料
- 2 个工作日出分，附分项报告

### 6 大考试场景（随机抽 4 个）
1. 客户支持解决方案代理（Agent SDK + MCP + 升级处理）
2. 使用 Claude Code 生成代码（CLAUDE.md + 计划模式）
3. 多代理研究系统（协调器-子代理编排）
4. 开发者生产力工具（内置工具 + MCP 服务器）
5. CI/CD 中的 Claude Code（非交互式管道 + 结构化输出）
6. 结构化数据提取（JSON 模式 + tool_use + 验证循环）

### 5 大知识领域

| # | 领域 | 权重 | Skill |
|---|------|------|-------|
| 1 | 代理架构与编排 | 27% | `/cca-domain1` |
| 2 | 工具设计与 MCP 集成 | 18% | `/cca-domain2` |
| 3 | Claude Code 配置与工作流 | 20% | `/cca-domain3` |
| 4 | 提示工程与结构化输出 | 20% | `/cca-domain4` |
| 5 | 上下文管理与可靠性 | 15% | `/cca-domain5` |

模拟测验：`/cca-quiz`
```

## Step 2: 推荐学习路径

根据用户水平推荐学习顺序：

**初学者路径（从易到难）：**
1. `/cca-domain3` — Claude Code 配置（最直观，日常能用）
2. `/cca-domain4` — 提示工程与结构化输出（基础能力）
3. `/cca-domain2` — 工具设计与 MCP（承上启下）
4. `/cca-domain1` — 代理架构与编排（核心重点，权重最高）
5. `/cca-domain5` — 上下文管理与可靠性（综合应用）
6. `/cca-quiz` — 模拟测验检验学习成果

**有经验者路径（按权重优先）：**
1. `/cca-domain1` — 27%，最高权重
2. `/cca-domain3` — 20%
3. `/cca-domain4` — 20%
4. `/cca-domain2` — 18%
5. `/cca-domain5` — 15%
6. `/cca-quiz` — 模拟测验

## Step 3: 引导用户选择

问用户：
- 你对 Claude Code / Agent SDK / MCP 的熟悉程度如何？
- 想从哪个领域开始学习？
- 还是想直接做模拟题 `/cca-quiz` 测试一下水平？

根据回答推荐具体的 `/cca-domainN` skill。

## 核心技术栈速查

| 技术 | 核心概念 |
|------|---------|
| **Claude Agent SDK** | AgentDefinition, stop_reason, hooks (PostToolUse), Task 工具, fork_session, allowedTools |
| **MCP** | .mcp.json, 环境变量扩展, isError, tool descriptions, resources |
| **Claude Code** | CLAUDE.md 层级, .claude/rules/, .claude/commands/, skills (context: fork), -p 标志, --output-format json |
| **Claude API** | tool_use, tool_choice (auto/any/forced), JSON schema, Message Batches API, custom_id |

## 考试不考的内容

- 模型微调、训练
- API 认证/计费
- 具体编程语言实现细节
- MCP 服务器部署/运维
- 模型内部架构
- 向量数据库、Embedding
- 浏览器自动化、视觉分析
- 流式 API、SSE
- 限速/定价计算
- OAuth / API key 轮转
