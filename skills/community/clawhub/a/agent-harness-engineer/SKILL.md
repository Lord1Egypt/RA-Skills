---
name: agent-harness-engineer
description: >
  指导AI coding工具构建生产级Agent系统。当用户需要设计、实现或优化AI Agent系统时触发。
  特别适用于：Agent架构设计、Harness工程、工具系统、权限模型、上下文管理、多智能体协作、
  记忆系统、安全沙箱、MCP集成等场景。支持从概念设计到生产部署的完整Agent系统构建。
  
  触发关键词：构建agent、创建智能体、agent系统、自动化工具、AI助手、多智能体、
  agent优化、升级agent、agent脚手架、agent项目模板、agent框架。
  
  核心目标：帮助AI coding工具生成结构完整、可扩展、生产就绪的Agent项目，
  而非仅提供最小化demo代码。
  
  与v1/v2版本的区别：
  - v1版本：提供理论文档和最小示例，AI coding工具需要自己理解如何应用
  - v2版本：提供分阶段构建指南，每个阶段都有明确的理论指导、实践步骤、检查清单和常见问题
  - v3版本（当前）：引入三级构建规模、代码生成禁止复制策略、技术栈分级推荐、抽象接口引导模式。
    AI coding工具必须根据用户需求生成定制化代码，不得直接复制reference中的示例代码。
    reference中的代码已全部改为"抽象接口/骨架 + AI引导提示"，确保AI主动设计而非被动复制。
---

# Agent Harness Engineer v3

本 Skill 将帮助你设计、实现和优化生产级的 AI Agent 系统，当前是 v3 版本。

本版本采用**分阶段构建模式**，将 Agent 系统构建拆分为 7 个明确的阶段，每个阶段都有：
- **理论指导**：该阶段需要应用什么设计原则
- **抽象接口层**：定义而非实现，引导 AI 根据需求生成代码（v3 核心变更）
- **AI 构建提示**：在关键位置给出引导，告诉 AI 应该生成什么
- **检查清单**：完成标准是什么（按规模分级）
- **常见问题**：这个阶段容易踩什么坑

## v3 核心变更（必读）

### 变更1：三级构建规模

Agent 系统不再只有一种构建方式。根据用户需求，分为三级：

```
┌───────────────────┬───────────────────────┬──────────────────────────┬──────────────────────────┐
│  维度             │  Minimal（最小）       │  Professional（专业）     │  Enterprise（企业）       │
├───────────────────┼───────────────────────┼──────────────────────────┼──────────────────────────┤
│  目标             │  快速原型/学习验证     │  团队工具/生产级应用      │  企业平台/高并发/多租户   │
│  预期代码量       │  ~300-500行           │  ~2000-4000行            │  ~6000-10000行+          │
│  第三方库         │  仅SDK（1-2个）       │  5-8个关键库             │  10+个全套生态栈         │
│  沙箱             │  路径白名单检查        │  Docker容器隔离           │  Firecracker微VM隔离      │
│  日志             │  print() / console.log│ structlog / loguru / pino│  OpenTelemetry 全链路     │
│  CLI              │  input() / 简单argparse│ click / typer / commander│  rich + 交互式TUI         │
│  配置管理         │  .env 文件            │  YAML + pydantic/zod     │  7级层级化配置覆盖        │
│  测试             │  手动测试或无          │  pytest/jest + mock      │  pytest/jest + CI/CD      │
│  监控             │  无                   │  基础 metrics 计数器     │  Prometheus + Grafana     │
│  上下文压缩       │  仅 Snip（历史截断）   │  完整四级压缩管道         │  四级 + 压缩状态恢复      │
│  记忆系统         │  无                   │  文件系统持久化           │  向量数据库 + 自动做梦    │
│  MCP集成          │  无                   │  基础 stdio MCP          │  全协议 + 连接池管理      │
│  多Agent          │  不支持               │  可选（Coordinator）     │  支持（Coordinator+Swarm）│
└───────────────────┴───────────────────────┴──────────────────────────┴──────────────────────────┘
```

### 变更2：代码生成禁止复制策略

> **关键规则：AI coding工具必须根据用户需求设计并生成代码，不得直接复制 reference 文件或 template 文件中的代码片段。**
> 
> Reference 文件中的代码已从"完整实现"改为"抽象接口/类定义 + AI构建提示"。
> Template 文件中的代码已从"完整实现"改为"骨架 + TODO + AI构建提示"。
>
> **为什么？** 之前的 reference 和 template 中包含完整可运行代码（如 read_file 实现、sandbox 实现），AI工具会直接复制，导致生成的系统永远是"最小实现"，无法根据用户需求调整复杂度和技术栈。

**AI coding工具的正确行为：**
1. 阅读 reference 中的抽象接口定义，理解需要哪些方法和属性
2. 阅读 reference 中的设计原理，理解为什么这样设计
3. 根据用户选择的规模和用途，决定生成代码的复杂度和完整度
4. 参考 technology-stack.md 选择合适的三方库
5. **自己设计并编写代码**，而非复制粘贴

### 变更3：技术栈分级推荐

参考 `references/11-technology-stack.md`，每个维度（日志、CLI、HTTP、沙箱、监控等）都提供 Minimal / Professional / Enterprise 三级推荐方案。AI 必须根据用户选择的规模，选择对应级别的技术栈。

## 快速导航

- **[SKILL.md](SKILL.md)** (本文件): 核心原则、构建规模分级、代码生成策略
- **[references/01-phase-init.md](references/01-phase-init.md)**: Phase 1: 项目初始化（三级规模目录结构）
- **[references/02-phase-llm.md](references/02-phase-llm.md)**: Phase 2: LLM抽象层（含streaming、retry、token计数接口）
- **[references/03-phase-tools.md](references/03-phase-tools.md)**: Phase 3: 工具系统（含concurrency分区算法、MCP adapter）
- **[references/04-phase-agent-loop.md](references/04-phase-agent-loop.md)**: Phase 4: Agent核心循环（含状态机、7个continue站点、流式架构）
- **[references/05-phase-context.md](references/05-phase-context.md)**: Phase 5: 上下文管理（含四级压缩完整算法、Session WAL设计）
- **[references/06-phase-permissions.md](references/06-phase-permissions.md)**: Phase 6: 权限安全（含5种模式、7级规则、6层防御、沙箱技术对比）
- **[references/07-phase-production.md](references/07-phase-production.md)**: Phase 7: 生产化（含OpenTelemetry、三层可观测、CI/CD）
- **[references/08-core-concepts.md](references/08-core-concepts.md)**: 核心概念速查（三大支柱、三组件虚拟化、13条防护规则）
- **[references/09-multi-agent.md](references/09-multi-agent.md)**: 多智能体（子Agent隔离设计、Token节省量化、Worktree隔离）
- **[references/10-mcp-integration.md](references/10-mcp-integration.md)**: MCP集成（6种传输协议、连接池、OAuth、资源管理）
- **[references/11-technology-stack.md](references/11-technology-stack.md)**: 技术栈分级选择指南（日志/CLI/HTTP/沙箱/监控/测试/数据库）
- **[references/12-sandbox-advanced.md](references/12-sandbox-advanced.md)**: 沙箱深度设计（Docker/Firecracker/gVisor/Wasm对比、bubblewrap集成）
- **[references/13-session-design.md](references/13-session-design.md)**: 会话设计（WAL模式、事件类型、状态机、回放恢复机制）
- **[references/14-observability.md](references/14-observability.md)**: 可观测性（OpenTelemetry/Prometheus/Langfuse集成、结构化日志）
- **[templates/minimal/](../templates/minimal/)**: Minimal 规模脚手架模板
- **[templates/professional/](../templates/professional/)**: Professional 规模脚手架模板
- **[templates/enterprise/](../templates/enterprise/)**: Enterprise 规模脚手架模板

## 核心原则

### 1. Harness Engineering 三大支柱

- **Context Engineering（上下文工程）**: 管理信息的可访问性、结构和时机
  - 静态上下文：CLAUDE.md/AGENTS.md、设计文档
  - 动态上下文：日志、指标、Git状态、CI/CD状态
  - 上下文压缩：四级管道（Snip → Microcompact → Context-Collapse → Autocompact）
  - 核心原则: "Agent无法在上下文中访问的信息不存在"

- **Architectural Constraints（架构约束）**: 通过机械执行而非建议来建立边界
  - 权限模型：5种模式 × 7级规则层级
  - 工具约束：Schema验证、并发安全标记
  - 安全边界：沙盒隔离、硬编码拒绝、纵深防御（6层）

- **Entropy Management（熵管理）**: 定期清理Agent解决代码退化
  - 文档一致性验证、约束违规扫描、模式强制执行
  - 依赖审计、性能监控、覆盖率守卫

### 2. 三组件虚拟化架构

```
Session（会话）= 追加式事件日志（Append-only Event Log）
  - 不可变、可序列化、可回放
  - 类似数据库WAL，是系统的唯一事实来源
  - 支持故障恢复、负载迁移、调试回放

Harness（编排器）= 无状态编排循环
  - 全部输入来自Session日志
  - 可随时崩溃、重启、迁移
  - 给定同样的Session日志，任何实例都会做出同样决策

Sandbox（沙箱）= 隔离执行环境
  - 文件系统隔离、网络隔离、进程隔离
  - 凭证外置，按需创建和销毁
  - 限制爆炸半径（Blast Radius Containment）
```

## 需求确认（构建前的必要步骤）

> **重要：在开始构建Agent之前，必须先确认用户需求。**
> **如果用户已经明确提供了以下信息，可以跳过本环节。**
> **如果用户没有提供，AI coding工具必须主动询问用户做选择，不得自行决定。**

### 需要确认的问题

当用户说"帮我构建一个Agent"但没有明确说明以下信息时，AI coding工具必须主动询问：

| 问题 | 选项/说明 | 影响 |
|------|---------|------|
| **技术栈偏好？** | Python / Node.js / TypeScript / Go | 决定项目脚手架语言 |
| **LLM供应商？** | Anthropic / OpenAI / Azure / 本地模型 | 决定默认配置 |
| **构建规模？** | Minimal / Professional / Enterprise | 决定项目复杂度、代码量、三方库数量 |
| **主要用途？** | 编码助手 / 自动化运维 / 数据分析 / 通用对话 / 其他 | 决定工具集 |
| **部署环境？** | 本地 / 云服务器 / 容器 / Serverless | 决定配置方式 |
| **沙箱隔离需求？** | 无 / 基础路径检查 / Docker隔离 / Firecracker微VM | 决定安全方案 |
| **监控需求？** | 无 / 基础日志 / 全链路追踪(Prometheus+OpenTelemetry) | 决定可观测方案 |
| **是否需要多Agent协作？** | 是 / 否 | 决定是否需要Phase 9内容 |

### 询问示例

如果用户说"帮我构建一个Agent"，但没有提供上述信息，AI coding工具应该这样询问：

```
在开始构建Agent之前，我需要确认几个问题：

1. **技术栈偏好**：
   - Python（推荐，功能完善）
   - Node.js/TypeScript

2. **LLM供应商**：
   - Anthropic (Claude) - 复杂推理、长上下文
   - OpenAI (GPT) - 通用任务、生态丰富
   - Azure OpenAI - 企业合规
   - 本地模型 (Ollama/vLLM) - 隐私敏感

3. **构建规模**（重要！决定生成代码的复杂度和技术栈）：
   - Minimal：快速原型，~300行代码，几乎无三方库依赖
   - Professional：生产级应用，~3000行代码，包含Docker沙箱、日志系统、测试
   - Enterprise：企业平台，~8000行代码，全链路监控、微VM沙箱、多Agent

4. **主要用途**：编码助手 / 自动化运维 / 数据分析 / 通用对话 / 其他

5. **沙箱隔离需求**：
   - 不需要（Agent在本地直接执行）
   - 基础路径检查（沙箱限制工作目录）
   - Docker容器隔离（推荐Professional场景）
   - Firecracker微VM（推荐Enterprise高安全场景）

6. **监控需求**：
   - 不需要
   - 基础结构化日志（推荐Professional场景）
   - 全链路追踪（推荐Enterprise场景）

7. **是否需要多Agent协作**？
   - 是 / 否

请告诉我你的选择，我会根据你的需求构建最合适的Agent项目。
```

### 快速确认模式

如果用户已经提供了部分信息，AI coding工具只需要补充询问未提供的信息：

```
根据你的需求（Python技术栈 + Anthropic模型 + 编码助手），
我还需要确认：

1. 构建规模？
   - Minimal：快速原型（300行）
   - Professional：生产级（3000行）
   - Enterprise：企业平台（8000行）

2. 沙箱隔离需求？
   - 无 / 基础路径检查 / Docker隔离 / Firecracker微VM

3. 监控需求？
   - 无 / 基础日志 / 全链路追踪

4. 是否需要多Agent协作？
   - 是 / 否

请补充提供以上信息，我将开始构建。
```

### 默认值策略

如果用户没有明确偏好，AI coding工具可以建议默认值，但必须说明原因：

```
你未明确说明偏好，我将使用以下默认值：
- 技术栈：Python（功能完善，社区活跃）
- LLM供应商：Anthropic（长上下文优势）
- 构建规模：Professional（平衡功能与复杂度，适合团队工具阶段）
- 主要用途：通用对话
- 沙箱：Docker隔离
- 监控：基础结构化日志
- 多Agent协作：否

如果你有其他偏好，请在回复中说明，我会相应调整。
```

### 构建规模决策矩阵

AI可以辅助用户选择规模：

```
┌─────────────────────────────────────────────────────────────┐
│ 帮你选择构建规模：                                            │
│                                                              │
│ ● 如果你是开发者，想快速验证Agent概念 → Minimal               │
│ ● 如果你是团队，需要可维护的生产级Agent → Professional        │
│ ● 如果你是平台方，需要服务多用户 → Enterprise                 │
│                                                              │
│ 如果你不确定，建议从 Professional 开始。                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 分阶段构建指南

> **核心规则（v3 强制）**：
> 1. 以下每个 Phase 的摘要仅提供目标概述。**实际构建时必须打开对应的 reference 文件**，其中包含设计原理、抽象接口定义、AI构建提示。
> 2. **禁止直接复制 reference 或 template 中的代码片段。** AI 必须根据用户选择的规模生成定制化代码。
> 3. 每个阶段完成后，必须使用**与该规模对应的检查清单**进行验收。

### Phase 1: 项目初始化 → `references/01-phase-init.md`

**目标**：建立项目骨架，定义目录结构（三级规模不同结构）和配置文件。

**规模差异**：
- Minimal: 单文件或最小目录结构
- Professional: 标准 src/config/tests 分离
- Enterprise: 多包 monorepo 结构

### Phase 2: LLM抽象层 → `references/02-phase-llm.md`

**目标**：实现与供应商无关的LLM客户端抽象。

**规模差异**：
- Minimal: 单一供应商直连
- Professional: 工厂模式 + streaming + retry
- Enterprise: 多供应商 + prompt cache管理 + token计数 + lazy import

### Phase 3: 工具系统 → `references/03-phase-tools.md`

**目标**：实现模块化的工具注册和执行机制。

**规模差异**：
- Minimal: 函数字典注册
- Professional: Registry + Schema验证 + MCP adapter
- Enterprise: 并发分区算法 + 工具依赖图 + 工具结果truncation

### Phase 4: Agent核心循环 → `references/04-phase-agent-loop.md`

**目标**：实现健壮的Agent主循环，包含错误恢复和状态管理。

**规模差异**：
- Minimal: 简单 while 循环
- Professional: while(true) + 7个Continue站点 + 状态机
- Enterprise: AsyncGenerator流式 + 双层超时 + Session回放

### Phase 5: 上下文管理 → `references/05-phase-context.md`

**目标**：实现四级压缩管道和记忆系统。

**规模差异**：
- Minimal: 仅 Snip 历史截断
- Professional: 完整四级管道 + 文件记忆
- Enterprise: 四级 + 压缩状态恢复 + 向量数据库记忆

### Phase 6: 权限安全 → `references/06-phase-permissions.md`

**目标**：实现权限控制和沙箱机制。

**规模差异**：
- Minimal: 命令黑名单
- Professional: 权限模型 + Hook系统 + Docker沙箱
- Enterprise: 6层纵深防御 + Firecracker + 审计日志

### Phase 7: 生产化 → `references/07-phase-production.md`

**目标**：添加测试、监控、日志。

**规模差异**：
- Minimal: 无
- Professional: pytest + structlog + 基础metrics
- Enterprise: CI/CD + OpenTelemetry + Prometheus

## 十大设计哲学

1. **Async Generator流式架构**: 不是返回最终结果，而是yield每一个中间事件
2. **通过Continue站点实现状态机**: while(true) + 7个continue站点
3. **编译时特性门控**: if (feature('FEATURE_X')) // bun:bundle编译时求值
4. **缓存前缀稳定性**: 内置工具排序后作为稳定前缀，MCP工具变化不影响缓存
5. **纵深防御**: 6层叠加使绕过概率指数下降
6. **数据驱动的可扩展性**: settings.json + agents/*.md + skills/*.md + hooks
7. **上下文即稀缺资源**: 工具延迟加载、记忆按需附加、四级压缩管道
8. **层级化配置覆盖**: 7级设置，CLI > Flag > Policy > Managed > Local > Project > User
9. **隔离的子Agent上下文**: 子Agent从空白消息列表开始，完成后只返回摘要
10. **可逆性优先**: 文件编辑通过Edit（替换字符串），不是Write（覆盖）

## 常见陷阱

1. **不要在Stop hook中做太重的操作**: 可能触发prompt-too-long错误，导致逻辑被静默跳过
2. **Hook allow不能绕过deny规则**: deny > settings rules > hook allow，这是安全不可变量
3. **hasAttemptedReactiveCompact不重置**: 防止compact→仍然太长→error→stop hook→compact的无限循环
4. **数组合并策略是连接+去重，而非替换**: 权限规则需要累加而非覆盖
5. **沙盒设置文件被硬编码为不可写**: 防止Agent通过修改settings.json来关闭沙盒
6. **MCP工具默认使用always_ask**: 第三方工具不应被自动信任
7. **Prompt Cache有最小长度要求**: 约1024 token，太短的前缀不会被缓存
8. **上下文压缩后必须主动恢复关键状态**: 文件内容、Skill上下文、Plan、任务列表

## 参考资源

- **核心文档**: 本目录下的 `references/` 文件（共14个）
- **项目模板**: `templates/minimal/` `templates/professional/` `templates/enterprise/`
- **外部资源**:
  - Anthropic Managed Agents API文档
  - Claude Code源码（~512,664行TypeScript）
  - MCP协议规范
  - "Scaling Managed Agents: Decoupling the brain from the hands" - Anthropic技术论文