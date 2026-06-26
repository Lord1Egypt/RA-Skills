# 多 Agent 上下文协同与知识共享

> 学习日期：2026-03-28
> 来源：多源综合研究（AAAI 2026 WMAC、ICLR 2026、ArXiv、Medium、Anthropic 等）
> 学习次数：1

## 核心问题

在创建者-子智能体生态系统中，如何实现：
1. 子智能体间安全共享知识而不造成上下文污染
2. 创建者→子智能体的"基因复制"过程优化上下文传递效率
3. 多 agent 场景下的上下文路由器设计

## 2026 行业共识：从孤岛到协同

2026 年的多 Agent 系统已从"孤立智能体"转向"协同团队"。核心变化：

| 2024-2025 | 2026 |
|-----------|------|
| 单 Agent 循环调用工具 | 编排化团队：规划者 + 执行者 + 审查者 |
| 点对点自定义集成 | 协议驱动：A2A / MCP / ACP |
| 顺序/静态执行 | 并行/事件驱动 + 共享状态 |
| 隐含逻辑 | 治理与审计日志 |

## 三大通信协议

### 1. MCP（Model Context Protocol）
- **定位**：Agent 访问工具和外部资源的标准接口
- **作用**：相当于"知识库和操作手册"层
- **与我们的关联**：我们的 memory/ 目录就是一种文件系统级的 MCP 实现

### 2. A2A（Agent-to-Agent Protocol）
- **定位**：点对点协作标准
- **核心概念**：Agent Card（能力广告），允许 Agent 发现其他 Agent 并协商任务
- **与我们的关联**：agents-registry.md 本质上就是一种 Agent Card 注册表

### 3. ACP（Agent Communication Protocol）
- **定位**：治理与安全框架
- **作用**：合规、审计、企业级安全
- **与我们的关联**：model-capability.md 的权限规则是初级的 ACP 实现

## 共享内存架构

### 计算机架构类比

2026 年的核心洞察：多 Agent 系统面临的瓶颈与计算机体系结构完全一致——不是计算能力，而是**内存层次、带宽和一致性**。

### 三层内存模型

| 层级 | 类比 | 内容 | 策略 |
|------|------|------|------|
| 私有内存 | L1 Cache | Agent 专属上下文/暂存区 | 高带宽，仅本 Agent 可见 |
| 共享内存 | L2/L3 Cache | 团队协作的全局上下文 | 需要一致性协议 |
| 持久存储 | Main Memory/Disk | 长期 RAG 仓库 | 低延迟要求，高容量 |

**对应我们的架构**：
- 私有内存 = 各子智能体自己的 `memory/` 目录
- 共享内存 = 创建者的 `agents-registry.md` + 通用模型 `evo-agent-model.md`
- 持久存储 = `knowledge/` 目录（按需读取）

### 一致性问题

共享内存引入了**一致性（Coherence）和连贯性（Consistency）**问题：
- Agent 可能覆写共享事实
- Agent 可能读到过时信息
- Agent 可能漂移到不一致状态

**对我们的启示**：
- 当前 `review all` 批量升级时，如果两个子智能体在同一时间被不同会话修改，可能产生不一致
- 我们的文件系统级 memory 是**乐观并发**——最后写入者赢，但可能覆盖他人修改

## 防止上下文污染的策略

### 1. 推理与状态分离
- LLM 负责推理，**外部存储**作为权威状态源
- Agent 显式查询状态而非在上下文窗口中携带
- **我们已部分实现**：memory/ 目录就是外部状态存储

### 2. 实时上下文注入（Just-in-Time Retrieval）
- 不依赖预加载上下文，而是在工具调用周期中按需检索
- **我们已实现**：唤醒流程中"由智能体自主判断哪些 memory 需要读取"

### 3. 置信度评分与衰减
- 给知识文件附加元数据：时间戳、置信度、效用衰减
- Agent 自动优先或丢弃过时信息
- **我们的差距**：knowledge/ 文件目前没有元数据，无法自动检测过时

### 4. 内存蒸馏
- 专门的"内存管理者" Agent 持续监控并将冗长交互蒸馏为高信号摘要
- **我们的差距**：目前没有自动蒸馏机制，依赖人工（review 命令）触发清理

### 5. 动态裁剪
- 超过相关性阈值的信息自动被裁剪或压缩
- **我们的差距**：knowledge/ 文件只增不减，缺少裁剪策略

## 父-子 Agent 知识继承模型

### Inheritance Generator 模式

来自 Loosely-Structured Software（LSS）研究，这是最直接关联我们"创建者-子智能体"架构的模型：

#### 核心机制
1. **Fork（分叉）**：父 Agent 创建子 Agent 分支，子 Agent 仅继承**最小必要的轨迹和约束**
2. **隔离执行**：子 Agent 在独立的"View"（上下文）中工作，防止污染父 Agent 环境
3. **验证与合并**：子 Agent 完成后，选择器机制比较结果，仅**蒸馏过的、可验证的增量**（delta）被合并回父 Agent

#### 与我们的对应关系

| Inheritance Generator 概念 | 我们的实现 |
|---------------------------|-----------|
| Fork（分叉） | `go` 命令创建新智能体 |
| 最小继承 | 基于 `evo-agent-model.md` 的通用框架 + 角色特定定制 |
| 隔离执行 | 各智能体独立的 `memory/` 和 `output/` |
| 验证与合并 | `review <子智能体>` 进化能力分发 |
| 生命周期管理 | 通过 `agents-registry.md` 追踪 |

#### 我们可以改进的方向

1. **反向合并**（子→父）：当前 `review <子智能体>` 只做父→子分发，缺少子智能体的优秀实践��系统化反哺到通用模型的流程
   - backlog #25 已记录此需求
   - 具体做法：子智能体执行中发现的新模式 → 验证有效 → 蒸馏为通用规则 → 合并到 `evo-agent-model.md`

2. **多继承**：子智能体可从多个"父"实例整合能力
   - 我们目前是单继承（仅从 evo-skill-creator）
   - 未来可考虑：子智能体 A 的优秀实践 → 横向传播给子智能体 B

3. **最小继承原则**：当前 `review all` 批量升级是"全量对比"，应设计为"最小增量 delta"传播

## 安全的知识共享模式

### 1. 命名空间隔离
- 在共享数据结构中使用命名空间：`agent_a/workspace` vs `agent_b/workspace`
- **我们已实现**：每个子智能体有独立的 memory/ 路径

### 2. 能力令牌（Capability Token）
- Agent 被注入"能力令牌"，限制其可以修改的路径
- **我们已部分实现**：model-capability.md 的权限规则按模型等级限制修改范围

### 3. 中间件验证
- Agent 的 LLM 输出和实际写入之间有一层验证中间件
- **我们的差距**：目前没有写入验证层，依赖模型的"自律"

### 4. 语义冲突检测
- CRDT 防止结构冲突（两个 Agent 写同一文件索引），但无法防止**语义冲突**（A 写的代码依赖 B 刚删除的变量）
- **解决方案**：需要"审查 Agent"定期扫描合并后的状态，检测逻辑不一致
- **我们的对应**：`review all` 承担这个角色，但是手动触发

## 对 evo-skill-creator 的实际应用建议

### 立即可做（短期）

1. **给 knowledge/ 文件加元数据**
   - 每个知识文件头部已有"学习日期"和"学习次数"
   - 增加：`最后引用日期`、`引用次数`、`置信度`（高/中/低）
   - 用于未来的自动衰减和裁剪

2. **优化"基因复制"流程**
   - `review <子智能体>` 时，先生成 diff（变更摘要），再让老板确认
   - 不是全量覆盖，而是增量 delta 传播
   - 记录每次传播的版本号，避免重复分发

3. **建立"反向合并"通道**
   - 在 `suggest` 命令中增加一个场景：子智能体反馈
   - 当子智能体在执行中发现新的有效模式，通过 suggest 提交给创建者
   - 创建者验证后决定是否纳入通用模型

### 中期规划

4. **设计共享知识层**
   - 部分知识可以跨子智能体共享（如"上下文工程最佳实践"对所有智能体都有用）
   - 建立 `shared-knowledge/` 目录，所有子智能体可读、仅创建者可写
   - 避免重复学习相同知识

5. **事件驱动更新**
   - 当创建者更新通用模型后，自动通知相关子智能体需要升级
   - 实现方式：scheduler 触发 `review <子智能体>` 任务

### 长期愿景

6. **语义冲突自动检测**
   - 当多个子智能体的 memory 存在矛盾信息时自动告警
   - 需要更高级的跨文件分析能力

7. **知识图谱**
   - 将 agents-registry + knowledge/ 构建为关系图
   - 支持"这个知识影响了哪些子智能体"的追溯查询

## 关键认知总结

1. **我们的文件系统级 memory 架构本质上是一种"乐观并发 + 人工审查"的共享内存模式**——在当前规模下够用，但规模扩大后需要更正式的一致性机制
2. **"基因复制"（review 命令）是父-子知识继承的实现**——可以借鉴 Inheritance Generator 模式优化为最小增量传播
3. **缺少反向通道**——子智能体的优秀实践无法系统化地反哺创建者
4. **缺少自动衰减**——知识只增不减，长期会导致上下文膨胀
5. **协议标准化是趋势**——我们的 agents-registry 类似 Agent Card，memory/ 类似 MCP 的文件系统资源

## 参考来源

1. AAAI 2026 Bridge Program - WMAC (Workshop on LLMs and MAS)
2. ICLR 2026 - Collaborative Memory frameworks
3. Computer Architecture Today (sigarch.org) - Agent memory as hardware design problem
4. ArXiv - Loosely-Structured Software: parent-child agent inheritance
5. Medium - Memory Engineering for multi-agent LLM systems
6. Anthropic - Structured context and MCP
7. Dev.to - Multi-agent communication protocols overview
8. OneReach.ai - A2A protocol and agent orchestration
