# A2A 协议深度研究——Agent Card 与能力发现

> 学习日期：2026-03-28
> 来源：WebSearch 综合研究（a2a-protocol.org、Spring.io、ArXiv、CalmOps 等）
> 学习次数：1
> 状态：已完成（首轮）

## 核心问题

1. A2A 协议中 Agent Card 的标准字段和能力描述格式是什么？
2. 动态能力发现如何实现？
3. 与我们的 agents-registry.md 的差距和改进空间在哪里？

## A2A 协议概述

### 定位与作用

**Agent-to-Agent (A2A) Protocol** 是 Google 在 2025 年底推出的点对点 Agent 协作标准，与 MCP、ACP 构成 2026 年多 Agent 系统的三大通信协议：

| 协议 | 定位 | 核心功能 |
|------|------|---------|
| MCP | Agent ↔ 工具/资源 | 标准化工具调用和资源访问 |
| A2A | Agent ↔ Agent | 点对点协作、能力发现、任务委托 |
| ACP | Agent ↔ 治理层 | 合规、审计、企业级安全 |

### 核心概念

A2A 的核心是 **Agent Card**——一种"能力广告"机制，允许 Agent：
1. **发布自己的能力**（我能做什么）
2. **发现其他 Agent**（谁能帮我）
3. **协商任务**（如何合作）

## Agent Card 标准字段

基于 A2A 协议规范和行业实践，Agent Card 包含以下核心字段：

### 1. 身份信息（Identity）

```yaml
id: "agent-unique-identifier"
name: "Agent Display Name"
version: "1.0.0"
type: "specialist|generalist|orchestrator"
```

- **id**：全局唯一标识符（通常是 UUID 或命名空间路径）
- **name**：人类可读的名称
- **version**：语义化版本号，用于能力演进追踪
- **type**：Agent 类型分类

### 2. 能力描述（Capabilities）

```yaml
capabilities:
  - id: "capability-1"
    name: "Code Review"
    description: "Perform security and quality code reviews"
    input_schema:
      type: "object"
      properties:
        code: { type: "string" }
        language: { type: "string" }
    output_schema:
      type: "object"
      properties:
        issues: { type: "array" }
        score: { type: "number" }
    constraints:
      max_file_size: "10MB"
      supported_languages: ["python", "javascript", "go"]
```

**关键要素**：
- **能力清单**：每个能力独立描述
- **输入/输出 Schema**：明确接口契约（类似 OpenAPI）
- **约束条件**：资源限制、前置条件

### 3. 服务端点（Endpoints）

```yaml
endpoints:
  - protocol: "https"
    url: "https://agent.example.com/api/v1"
    auth_method: "bearer_token"
  - protocol: "a2a"
    url: "a2a://agent.example.com"
```

### 4. 元数据（Metadata）

```yaml
metadata:
  owner: "team-name"
  created_at: "2026-03-01T00:00:00Z"
  updated_at: "2026-03-28T00:00:00Z"
  tags: ["code-review", "security", "quality"]
  cost_model:
    type: "per_request"
    price: 0.01
    currency: "USD"
  performance:
    avg_response_time_ms: 500
    success_rate: 0.99
```

### 5. 依赖与兼容性（Dependencies）

```yaml
dependencies:
  - agent_id: "code-analyzer"
    version: ">=2.0.0"
  - tool: "git"
    version: ">=2.30"
compatible_protocols:
  - "A2A/1.0"
  - "MCP/1.1"
```

## 动态能力发现机制

### 1. 注册与发布（Registry & Publication）

#### 集中式注册表（Centralized Registry）

类似 Docker Hub 或 npm Registry：

```
Agent 启动 → 向注册中心发布 Agent Card → 注册中心索引能力
其他 Agent → 查询注册中心 → 获取匹配的 Agent Card
```

**优点**：
- 统一发现入口
- 易于治理和审计
- 支持版本管理

**缺点**：
- 单点故障风险
- 需要中心化基础设施

#### 分布式发现（Distributed Discovery）

类似 DNS 或 P2P 网络：

```
Agent 启动 → 广播自己的 Agent Card → 邻居节点缓存
查询 Agent → 向邻居节点查询 → 递归/迭代查找
```

**优点**：
- 无单点故障
- 去中心化

**缺点**：
- 发现延迟较高
- 一致性保证较弱

### 2. 能力匹配（Capability Matching）

#### 基于语义的匹配

不仅匹配关键词，还理解意图：

```python
# 查询："我需要一个能分析 Python 代码安全问题的 Agent"
# 匹配逻辑：
1. 提取关键词：["Python", "code", "security", "analysis"]
2. 语义扩展：["static analysis", "vulnerability scan", "code review"]
3. 在 Agent Card 的 capabilities.description 和 tags 中搜索
4. 计算相似度得分，返回 Top-K
```

#### 基于 Schema 的匹配

严格的接口契约匹配：

```python
# 查询："我有一个 Python 文件，需要输出安全问题列表"
# 匹配逻辑：
1. 解析输入类型：{ code: string, language: "python" }
2. 解析期望输出：{ issues: array }
3. 在 Agent Card 的 input_schema 和 output_schema 中匹配
4. 返回完全兼容的 Agent
```

### 3. 动态更新（Dynamic Update）

Agent Card 不是静态的，会随着 Agent 的进化而更新：

#### 版本演进

```yaml
# v1.0 → v1.1：新增能力
capabilities:
  - id: "code-review"  # 已有
  - id: "refactoring-suggestion"  # 新增
```

#### 性能指标实时更新

```yaml
metadata:
  performance:
    avg_response_time_ms: 500  # 实时统计
    success_rate: 0.99         # 实时统计
    last_updated: "2026-03-28T10:30:00Z"
```

#### 订阅机制

```
Agent A 订阅 Agent B 的能力变更 →
Agent B 更新 Agent Card →
通知所有订阅者 →
Agent A 刷新本地缓存
```

## 与我们的 agents-registry.md 对比

### 当前实现（agents-registry.md）

```markdown
| 名称 | 角色 | 类型 | 创建日期 | skill 路径 | 状态 |
|------|------|------|----------|-----------|------|
| kavabot-engineer | 机器人软件工程师 | 工作 | 2026-03-26 | /path/to/skill | 运行中（v1.5） |
```

**优点**：
- 简单直观
- 易于人类阅读
- 满足当前小规模需求

**缺点**：
- **缺少能力描述**：只有"角色"，没有"能力清单"
- **缺少接口契约**：不知道如何调用、输入输出是什么
- **缺少性能指标**：不知道响应时间、成功率
- **缺少依赖关系**：不知道 Agent 之间的依赖
- **缺少版本语义**：v1.5 是什么含义？与 v1.4 的差异是什么？
- **不支持动态发现**：需要人工查表，无法程序化查询

### 改进方向

#### 短期（立即可做）

1. **增加能力字段**

```markdown
| 名称 | 角色 | 核心能力 | 类型 | 版本 | 状态 |
|------|------|---------|------|------|------|
| kavabot-engineer | 机器人软件工程师 | 日志排查、需求迭代、代码重构 | 工作 | v1.5 | 运行中 |
```

2. **建立版本变更日志**

在每个子智能体的 memory/ 目录下增加 `CHANGELOG.md`：

```markdown
# kavabot-engineer 版本历史

## v1.5 (2026-03-28)
- 新增：cron 命令（调度配置管理）
- 新增：双向 suggest（深度对话）
- 改进：review 命令支持进化赋能

## v1.4 (2026-03-27)
- 新增：数据目录声明
```

#### 中期（需要设计）

3. **结构化 Agent Card**

将 agents-registry.md 升级为 agents-registry.yaml：

```yaml
agents:
  - id: "kavabot-engineer"
    name: "Kavabot 软件工程师"
    version: "1.5.0"
    type: "specialist"
    role: "机器人本体软件工程师"
    capabilities:
      - id: "log-analysis"
        name: "日志排查"
        description: "分析 Kavabot 机器人日志，定位问题根因"
        input: "日志文件路径或日志片段"
        output: "问题诊断报告"
      - id: "requirement-iteration"
        name: "需求迭代"
        description: "实现新功能需求"
        input: "需求描述"
        output: "代码实现 + 测试"
      - id: "code-refactoring"
        name: "代码重构"
        description: "优化代码结构和质量"
        input: "目标代码路径"
        output: "重构后的代码"
    metadata:
      created_at: "2026-03-26"
      updated_at: "2026-03-28"
      skill_path: "~/.claude/skills/kavabot-engineer"
      category: "工作"
      tags: ["机器人", "C++", "ROS", "嵌入式"]
    status: "active"
    framework_version: "evo-agent-v1.5"
```

4. **能力查询接口**

创建一个辅助脚本 `query-agent.py`：

```python
# 查询：谁能帮我排查日志？
python query-agent.py --capability "log-analysis"
# 输出：kavabot-engineer, evo-skills-maintainer

# 查询：谁能做股票分析？
python query-agent.py --capability "stock-analysis"
# 输出：greate-stocks-operator
```

#### 长期（愿景）

5. **完整的 A2A 协议实现**

- 每个子智能体启动时向注册中心发布 Agent Card
- 支持 Agent 之间的直接调用（而非通过人工中转）
- 实现能力订阅和动态更新通知

6. **Agent 编排器（Orchestrator）**

创建一个专门的"编排器"智能体：

```
用户："我需要分析 Kavabot 的性能问题"
编排器：
  1. 查询注册表 → 发现 kavabot-engineer 有 log-analysis 能力
  2. 调用 kavabot-engineer 的 go 命令
  3. 汇总结果返回给用户
```

## 关键认知总结

1. **Agent Card 是"能力广告"**——不仅描述"我是谁"，更重要的是"我能做什么"
2. **接口契约是核心**——input_schema 和 output_schema 让 Agent 之间能程序化协作
3. **动态发现是趋势**——从静态注册表到实时查询、订阅更新
4. **我们的 agents-registry.md 是 Agent Card 的初级形态**——满足当前需求，但缺少结构化和程序化能力
5. **改进路径清晰**：
   - 短期：增加能力字段 + 版本变更日志
   - 中期：结构化 YAML + 查询接口
   - 长期：完整 A2A 协议实现 + Agent 编排器

## 对 evo-skill-creator 的实际应用

### 立即可做

1. **agents-registry.md 增加"核心能力"列**
   - 让人类一眼看出每个 Agent 能做什么
   - 为未来的程序化查询打基础

2. **要求子智能体维护 CHANGELOG.md**
   - 在 evo-agent-model.md 中增加"版本管理"章节
   - 每次 review 升级后，子智能体更新 CHANGELOG

3. **go 命令创建新智能体时，明确要求定义"核心能力清单"**
   - 不仅问"角色是什么"，还要问"具体能做哪些事"
   - 写入 SKILL.md 的"能力清单"段落

### 中期规划

4. **设计结构化 Agent Card**
   - 将 agents-registry.md 升级为 agents-registry.yaml
   - 包含完整的能力描述、输入输出、依赖关系

5. **实现能力查询工具**
   - 创建 query-agent.py 脚本
   - 支持按能力、标签、类型查询

### 长期愿景

6. **Agent 之间的直接协作**
   - 子智能体可以调用其他子智能体的能力
   - 实现真正的多 Agent 协同

## 参考来源

1. [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
2. [Agent Discovery - A2A Protocol](https://a2a-protocol.org/latest/topics/agent-discovery/)
3. [Building Interoperable Agents with A2A - Spring.io](https://spring.io/blog/2026/01/29/spring-ai-agentic-patterns-a2a-integration)
4. [A2A Protocol Complete Guide 2026 - CalmOps](https://calmops.com/ai/a2a-protocol-agent-communication-complete-guide-2026/)
5. [The AGNTCY Agent Directory Service - ArXiv](https://arxiv.org/html/2509.18787v1)
6. [Topology-Independent Naming and Capability-Based Discovery - ArXiv](https://arxiv.org/html/2601.14567v1)
7. [How AI agents communicate across systems - CodiLime](https://codilime.com/blog/a2a-protocol-explained/)
8. [Google's Agent2Agent Protocol Explained - Galileo.ai](https://galileo.ai/blog/google-agent2agent-a2a-protocol-guide)
