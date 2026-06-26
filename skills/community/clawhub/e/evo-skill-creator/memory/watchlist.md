# 关注清单

> 关注 AI 领域的新趋势、新技术、新框架，服务于创建更强大的智能体。

## AI 模型动态

### 2026-04 Claude Opus 4.6 生态系统升级（更新：2026-04-02）
- **Adaptive Thinking + 可配置努力等级**：Low/Medium/Max 三档，平衡智能/速度/成本
- **Claude Cowork（桌面生产力预览）**：本地运行，跨文件夹/应用自主操作，无需手动复制粘贴
- **MCP Apps**：MCP 从数据/工具连接器升级为平台，Agent 可返回交互式 UI 组件（图表/表单/仪表板）
- **Computer Use 增强**：直接与系统 UI 交互（打开应用/导航浏览器/点击），弥补 API 集成空白
- **Persistent Memory 全面推出**：跨会话保留上下文/沟通风格/项目偏好，减少重复"简报"
- **128K 输出窗口**：Opus 4.6 支持超长输出，适合生成完整文档/代码库
- **Compaction API**：自动压缩上下文，延长会话寿命

### 2026-03 新模型能力等级更新
- **HyperAgents (Meta, arXiv:2603.19461)** — 跨领域自我改进框架，DGM 的升级版（DGM-H），元认知自修改能力。标志着 Level 2 递归自我改进不再是理论。
- **"50% 可靠性时间范围"** — 新指标趋势：衡量 Agent 自主运行多久才需要人工介入，取代 Pass@1 基准测试。

## Agent 框架与方法论

### Skill Engineering 成为主流（2026-04-04 更新）
- Skill 结构化（SKILL.md + YAML frontmatter + scripts/）已成为行业标准，不再是 niche 方案
- Claude "Tasks"：持久多步执行，与 Claude 工具控制深度集成
- 关键转变：从"提示工程"到"Skill 工程"——Skill 本质是 SOP + 护栏 + 领域知识
- **2026-04 新共识**：
  - "Execution-Layer Skills"——Skill 不再是静态指令，而是**模块化执行单元**
  - "Document & Clear" Pattern——长任务定期 dump 进度到文件 + /clear 重置上下文，防止 context rot
  - Hooks as Guardrails——PreToolUse/PostToolUse 作为确定性护栏
  - MCP 集成标准化——新数据源/工具通过 MCP Server 接入，而非自定义 wrapper

### 自我进化范式演进（2026-04-04 更新）
**四大核心范式**：
1. **Self-Play & Data Generation ("SWE-RL" 模式)**：Agent 自生成训练数据（bug 注入→修复循环）
2. **Metacognitive Improvement ("HyperAgents" 模式)**：修改"修改过程"本身，跨领域迁移改进策略
3. **Hierarchical Macro-Micro Learning (HiMAC 模式)**：宏观规划 + 微观执行分层，长期任务效果显著优于纯扩大模型
4. **Git-Native Evolution ("A-Evolve" 模式)**：进化即 CI/CD，每个变异版本化为 Git 标签，支持回滚审计

**2026 新趋势（ICLR 2026 + Agent0 + A-Evolve）**：
- **Curriculum Agent + Executor 双智能体自进化**：一个提出任务，一个执行，互相推动能力边界（Agent0, ICLR 2026 RSI Workshop）
- **Git-Native Evolution Loop**：Solve→Observe→Evolve→Gate→Reload 五阶段，Workspace-as-Code 直接编辑工作区文件
- **Contextual Drag 警告**：从错误/失败记忆中学习时，错误模式会污染未来推理，需要 Clean History 管理
- **Test-Time Improvement vs Post-Run Improvement**：前者无权重变化（Reflexion/Self-Refine），后者系统级改进（轨迹驱动重训练）
- **Metacognitive Self-Improvement**：优化"修改过程"本身，而非仅优化任务输出
- **自主任务时长翻倍定律**：METR 观察到 Agent 可靠完成任务的时长每 4 个月翻倍（2026 年初约 50 分钟）
- **Evaluation Gate 成为标配**：进化变异必须通过严格验证（bitwise/性能基准）才能被接受，非 optional

### 结构性侵蚀问题（SlopCodeBench, 2026-03）
- Agent 生成代码在迭代开发中系统性退化：冗余度 +89.8%，结构侵蚀 +80%
- Agent 代码比人类代码冗余 2.2 倍
- Prompt 干预能改善初始质量但**无法阻止长期退化率**
- 启示：**受限自我进化**（constrained self-evolution）是关键——进化必须有结构约束

### 持久执行（Durable Execution, 2026-03）
- 从"脆弱脚本"到"弹性长期进程"的架构转变
- 核心机制：自动状态持久化 + 事件历史回放 + 故障恢复
- Temporal / Azure Durable Functions 成为 Agent 基础设施
- 与 Scheduler 的关系：我们的 cron 调度是轻量级实现，完整版需要持久执行框架

### Agent Memory OS 范式巩固（2026-03/04）
- **三层内存已成共识**：Working Memory (RAM) → Recall (Cache) → Archival (Disk)
- **Letta (MemGPT)** 成为生产级参考实现：Agent 自管理上下文，自主决定何时归档/检索
- **向量数据库降级**：从"核心"降级为"组件之一"——混合架构是正确方向（验证我们 #19 结论）
- **Agent-Managed Memory**：Agent 主动决定何时归档、何时摘要、何时清除噪音
- **2026-04 新趋势**：
  - **自主内存管理**：Agent 通过 RL 训练使用"Memory Tools"自主写入/更新/删除，减少人工干预
  - **压缩与过滤**：Memory Filters（小型 LLM）决定什么值得保存，语义摘要+潜在状态压缩
  - **持续学习系统**：推理时学习（inference-time learning），将经验压缩到模型权重或持久知识结构
  - **生成式记忆**：不再只是检索原始文档（RAG），而是基于压缩潜在记忆生成综合响应
  - **混合检索**：向量搜索（语义）+ 元数据过滤（精确）+ 图遍历（关系）+ Cross-Encoder 重排序
  - **Context vs Memory 严格区分**：Context（临时、token 窗口）vs Memory（持久、跨会话）
  - **Tiered Memory 架构**：Working Memory (Redis) + Episodic/Semantic (Vector DB) + Procedural (Graph/Relational)

### MCP + A2A 协议栈成熟（2026-03）
- **MCP**：Agent-to-Tool 层，已成事实标准（百万级下载）
- **A2A**：Agent-to-Agent 层，通过 Agent Card 发现+委托+状态管理
- **ACP/UCP**：商业/治理层（新出现）
- 反模式：让单个 Agent 内化所有工具和子任务 → 上下文窗口退化 + 可靠性降低

## Agent 可靠性与质量保障（2026-04 新增）

### 代码质量退化防护（2026-04，新发现）
- **"Harness Engineering"取代 Prompt Engineering**：可靠性是环境级问题，不仅是模型级问题
- **核心策略**：
  - **Memory Consolidation（内存整理）**：定期摘要+剪枝，防止"睡眠剥夺"（噪音累积）
  - **Persistent Context（持久上下文）**：AGENT.md / 架构决策记录 / 编码标准作为稳定真相源
  - **Structured Handoffs（结构化交接）**：每次会话重新定向（检查目录/读进度/验证测试）
  - **Generator-Evaluator Loops（生成-评估循环）**：一个 Agent 生成，另一个评审，再提交
  - **Code Health as Proxy（代码健康度代理）**：模块化、清晰的代码库显著提升 Agent 表现
- **Evaluation-Led Development（评估驱动开发）**：
  - 自动质量门禁集成到 CI/CD
  - 中间步骤监控（不仅看结果，看推理路径）
  - Action Schema Validation（动作模式验证）：工具调用前验证，失败返回 Agent 自纠正
- **Governance & Human Oversight（治理与人工监督）**：
  - 风险分层（低风险自动化，高风险人工审核）
  - Human-with-the-loop（人类处理复杂判断，Agent 处理常规执行）
  - Living Governance（动态治理）：实时调整验证器和护栏
- **Testing & Resilience（测试与韧性）**：
  - End-to-End Testing（端到端测试）补充单元测试
  - Graceful Degradation（优雅降级）：重试、备用模型、"不知道"行为
  - Task Decomposition（任务分解）：避免开放式目标，强制离散可验证子任务

### "Prompt Engineer" → "Skill Engineer" 角色转变（2026-04 确认）
- **Skill 本质**：SOP（标准操作流程）+ 护栏（约束与安全）+ 领域知识
- **SKILL.md 最佳实践**（2026-04）：
  - **不要塞进系统提示**：系统提示应保持简洁，Skill 应模块化为独立文件
  - **结构化 vs 代码**：简单 Skill 用 Markdown，复杂逻辑用 Python/TypeScript + scripts/
  - **Markdown 的隐藏成本**：Token 消耗高（格式化字符占比大），大规模时考虑结构化存储
  - **可测试性**：Skill 应包含测试用例和验证标准
  - **版本管理**：Semantic Versioning + YAML frontmatter 中的 version 字段
- **Skill 分层架构**（2026-04 新共识）：
  - **Deterministic Logic（确定性逻辑）**：规则/验证/格式化 → 用代码实现，不依赖 LLM
  - **Agentic Logic（智能体逻辑）**：推理/规划/创造性决策 → 用 LLM 实现
  - **反模式**：让 LLM 做简单的字符串拼接、数学计算、格式验证（浪费 + 不可靠）

### Context Engineering 取代 Prompt Engineering（2026-03，验证已有学习 #11）
- Prompt 只占上下文 ~5%，其余 95% 才是成败关键
- PIV Loop（Plan-Implement-Validate）成为高效开发者标配
- 四层上下文架构：Goal → Technical → Behavioral → Attempt

### Agentic Variation Operators (AVO, 2026-03)
- 用自主 Agent 替代传统进化算法的固定变异/交叉操作
- 7 天自主进化超越 cuDNN 3.5% 和 FlashAttention-4 10.5%
- 核心循环：plan→implement→test→debug（与我们的 go→review 可对齐）
- 启示：Agent 驱动的进化循环在生产级别已被验证可行

### 轨迹感知安全 (Trajectory-Aware Safety, 2026-03)
- 从监控单个输出转向监控动作序列
- 检测进化轨迹偏移，即使单步看似正常但整体趋势异常也触发干预
- 与 execution.log 的进化：应记录步骤级动作序列，不仅是命令级摘要

### SKILL.md 开放标准（2026-04，新发现）
- **Agent Skills 开放标准**：模块化、可移植的 AI Agent 能力打包规范，核心是 SKILL.md 文件
- **Progressive Disclosure（渐进式披露）三阶段**：
  1. **Discovery（发现）**：启动时扫描 YAML frontmatter（name + description），构建轻量级能力注册表
  2. **Activation（激活）**：用户请求匹配时，加载完整 Markdown 指令到上下文
  3. **Execution（执行）**：按指令执行，按需访问 scripts/references/assets
- **标准目录结构**：
  - `SKILL.md`（必选）：YAML frontmatter + Markdown 指令
  - `scripts/`（可选）：可执行代码（Python/Shell）
  - `references/`（可选）：补充文档/详细指南
  - `assets/`（可选）：静态资源（模板/配置）
- **YAML Frontmatter 标准字段**：
  - `name`（必选）：匹配目录名
  - `description`（必选）：含触发短语，路由完全依赖自然语言
  - `version`、`license`、`compatibility`、`metadata`（author/tags）
  - **无独立 triggers 字段**：路由完全依赖 description 的自然语言
- **行业采用（2026-04）**：
  - **起源**：Anthropic（Claude Code），2025-12-18 开源
  - **治理**：agentskills.io 维护，供应商中立
  - **生态**：16+ AI 工具兼容（Cursor/GitHub Copilot/VS Code/CLI 工具）
  - **与 MCP 的关系**：MCP 专注 Agent-to-Tool（API/数据库连接），SKILL.md 专注程序性指导
- **对我们的启示**：子智能体分发需符合此标准，YAML frontmatter 已纳入学习计划 #43
- YAML frontmatter（name/description/version/tags）已成行业标准发现机制
- 我们的子智能体 SKILL.md 缺少标准化 frontmatter
- 应纳入 evo-agent-model.md 规范

### Claude Tasks + Agent Teams（2026-03，新发现）
- **Claude Tasks**：持久化任务系统，状态写入文件系统（`~/.claude/tasks`），跨会话保持上下文
- **Agent Teams**：并行多 Agent 协作，一个 lead 分解任务 + 多个 teammates 并行执行 + 相互校验
- **启示**：
  - 我们的 steward（管家）可以利用 Agent Teams 实现真正的并行唤醒+收集
  - 我们的 scheduler 可以考虑将任务状态持久化到文件系统而非仅靠 cron 触发
  - Cross-Session Coordination（CLAUDE_CODE_TASK_LIST_ID 环境变量）可能对多智能体协作有价值

### Skill 市场化与分发标准（2026-03，新发现）
- skills.sh (Vercel)：Skill 注册中心，CLI 安装（`npx skills add <name>`），类似 npm 生态
- SKILL.md 已成跨工具开放标准（Claude Code / Cursor / Gemini CLI 等 16+ 工具兼容）
- "Prompt Engineer" → "Skill Engineer" 角色转变已成行业共识
- **启示**：我们的子智能体如果要分发，需要符合这个开放标准（YAML frontmatter + 标准化目录结构）

### Agent 评估新范式（2026-04，新发现）
- **Trajectory vs Outcome Metrics（轨迹 vs 结果指标）**：
  - **Trajectory（轨迹）**：评估执行路径（推理步骤、工具选择、错误处理、延迟）
  - **Outcome（结果）**：评估最终产出（任务完成、准确性、合规性、用户满意度）
  - **为什么重要**：Agent 常因推理错误失败，而非输出错误，追踪"思考过程"是调试关键
- **非确定性环境的可靠性测量**：
  - **统计验证**：Cronbach's alpha / McDonald's omega 确保多次运行一致性
  - **LLM-as-Judge 优化**：目标 ≥0.80 Spearman 相关性，用小型人类偏好数据集校准
  - **级联错误**：多轮交互中成功率显著下降，单次成功不代表可靠
- **生产管道集成（Shift-Left & Shift-Right）**：
  - **Pre-Production Gates（预生产门禁）**：渐进式部署（dev 70% → staging 85% → prod 95%）
  - **Continuous Monitoring（持续监控）**：100% 流量轻量级启发式评估 + 5-10% 深度 LLM 评估
  - **Evaluation-as-Guardrails（评估即护栏）**：轨迹指标低于阈值时自动触发回退或人工升级
- **评估焦点领域**：
  - **Tool Usage（工具使用）**：准确性、参数有效性（防止幻觉工具调用）
  - **Trajectory（轨迹）**：推理连贯性、循环检测（捕获"静默失败"）
  - **Safety/Policy（安全/策略）**：约束遵守（边缘情况不违反企业规则）
  - **Consistency（一致性）**：跨运行输出方差（识别不稳定性）
- **关键结论**：不依赖静态基准（SWE-bench/WebArena），必须构建**领域特定评估管道**，在每个节点追踪 Agent 逻辑
- **Trajectory Evaluation 成为生产标准**：评估推理路径+工具选择是否最优，不仅看最终输出
- **多次运行一致性**：单次成功是虚荣指标，Cronbach's alpha 跨多次独立运行衡量可靠性
- **LLM-as-Judge + 结构化 Rubric**：评估 LLM 需校准到 0.80+ Spearman 相关性
- **CI/CD 集成**：评估不再是一次性的，而是持续集成到开发流程中
- **DeepEval DAG Metrics**：将评估标准映射到 Agent 执行图的确定性指标
- **启示**：review 命令的评审维度可参考 Trajectory Evaluation；execution.log 需要记录更细粒度的执行路径

### Agent 可靠性量化指标（2026-03，新发现）
- METR 观察：Agent 可自主完成任务的时长每 4 个月翻倍
- 前沿模型现在 50% 可靠性时间范围约 50 分钟（去年 < 15 分钟）
- **启示**：我们的 scheduler tick 间隔应跟踪此指标调整；50 分钟意味着 learn/scan 等长任务已经可行

### 自我进化形式化定义（2026-03，学术界确认）
- Closed-Loop Evolution 形式定义：Π = (Γ, {ψ_i}, {C_i}, {W_i}) — Policy + Memory + Controllers + Workflow
- 系统持续修改内部组件以响应反馈，无需持续人工干预
- **启示**：我们的进化模型可以映射——SKILL.md(Γ) + memory(ψ) + 命令体系(C) + go工作流(W)

### 生产级编排模式（2026-04，新发现）
- **从"生成"到"编排"的战略转变**：AI Agent 的核心价值在于独立运行、管理长期项目上下文、使用全套工具
- **从"Mega-bots"到协作生态系统**：单一超级模型 → 专业化 Agent 团队（减少幻觉、模块化验证）
- **多 Agent 编排模式驱动企业 ROI**：
  - **Sequential（顺序）**：任务链式传递，适合线性工作流
  - **Parallel（并行）**：独立任务同时执行，提升吞吐量
  - **Hierarchical（层级）**：Manager 分解任务 + Workers 执行，适合复杂项目（Supervisor Pattern）
  - **Collaborative（协作）**：Agent 间相互校验/辩论/投票，提升决策质量
- **System 2 Thinking**：循环迭代 + 自我批评，牺牲延迟换取可靠性
- **Event-Driven Architecture (EDA)**：企业级异步消息/事件驱动，适配遗留系统
- **生产级框架共识**（2026-04）：
  - **LangGraph**：状态机编排，检查点+故障恢复，生产级首选（支持循环、非 DAG）
  - **CrewAI**：角色驱动协作，适合团队模拟场景
  - **AutoGen**：对话驱动多 Agent，适合研究和原型
- **反模式警告**：单个 Agent 内化所有工具和子任务 → 上下文窗口退化 + 可靠性降低

### 知识图谱 Agent Memory（2026-04，新发现）
- **从"扁平向量"到"关系图谱"的转变**：向量搜索擅长相似片段检索，但将记忆视为孤立静态事实；知识图谱保留实体间关系，支持多跳推理、信息演化追踪、长期项目上下文维护
- **核心框架**：
  - **Cognee**：从非结构化数据构建知识图谱，支持关系推理而非孤立检索
  - **Mem0**：混合架构（向量搜索 + 图谱实体关系），个性化 + 长期持久化
  - **Zep / Graphiti**：时序知识图谱，追踪事实随时间变化（何时更新/替代），适合机构记忆
  - **LangMem (LangChain)**：将记忆图谱集成到 Agent 工作流，Agent 经验作为可遍历节点
  - **Neo4j**：成为底层数据库标准（复杂关系查询）
- **从"静态"到"自我进化"记忆**：
  - **Agent 自管理记忆**：Agent 决定存储什么、连接什么、剪枝什么（Evo-Memory 研究）
  - **类型化关系**：从文本块到结构化数据，显式定义关系（"替代"/"支持"/"矛盾"）
  - **时序感知**：系统知道 1 月的事实到 3 月可能失效（企业逻辑频繁变化）
- **为什么重要**：
  - **上下文连续性**：避免 Agent 忘记早期决策或项目级约束
  - **推理 vs 检索**：向量检索用于"查找信息"，图谱检索用于"理解连接"（多跳查询）
  - **成本效率**：正确管理的图谱记忆减少 token 成本（查询相关子图，而非重新注入大量无关上下文）
- **2026 共识**：从"记忆即文档存储"到"记忆即动态推理知识结构"

### Prompt-Shape Surgery（提示形状手术，2026-04 新发现）
- **核心问题**：模型在提示形状模拟"轮次边界"（turn boundary）时会过早停止或产生幻觉
- **解决方案**：插入非空标记（如 `[Tool Loaded]`）防止模型误判对话结构
- **为什么重要**：这是代码生成质量退化的一个新根因，纯 prompt 优化无法解决
- **启示**：子智能体的 SKILL.md 中长指令是否存在轮次边界误判风险？需要验证

### Clean-Room Agent Pattern（洁净室模式，2026-04 新发现）
- **场景**：高风险重构或系统重写
- **模式**：一个 Agent 定义需求和约束（Specifier），另一个隔离 Agent 仅基于规格实现（Implementer）
- **优势**：防止 Agent 在修改已理解偏差的代码时产生"漂移"
- **启示**：review 命令可以借鉴——一个视角评审，一个视角执行修改

### Agent IAM 与零信任架构（2026-04 新发现）
- **Agent 数字身份**：Agent 被分配数字身份和权限范围（scope of authority），与企业 IAM 体系集成
- **零信任延伸**：Agent 间通信采用 SPIFFE/mTLS 等机制，与敏感 API 同等安全级别
- **Memory Poisoning 防护**：记忆成为攻击面，需监控"记忆漂移"和未授权变异
- **启示**：我们的子智能体通过 `.claude/settings.local.json` 控制权限，这是轻量级 IAM；memory/private/ 的安全性需要关注

### SKILL.md 标准生态扩展（2026-04 更新）
- **采用规模**：从 16+ 平台扩展到 **30+ 平台**（Claude Code/Cursor/Copilot/Gemini CLI/OpenAI Codex/Augment 等）
- **确认**：YAML Frontmatter（name/description）是唯一的发现机制，无独立 triggers 字段
- **新增平台**：OpenAI Codex、Augment、Microsoft 多平台采用
- **启示**：标准已全面巩固，我们的子智能体必须补充 frontmatter

### Model Tiering 生产模式（2026-04 确认）
- **路由/分诊**：用廉价快速模型（Mini/Haiku 级别）
- **复杂推理**：仅在必要时使用重型模型（Opus/GPT-5 级别）
- **启示**：scheduler 调度的 cron 任务可以考虑 model tiering——learn 用重型，status 用轻量

### Validation-in-the-Loop（生成中验证，2026-04 新发现）
- **核心转变**：从"生成后验证"到"生成中持续验证"
- **实践**：在代码生成阶段嵌入架构合规性、lint、单元测试执行等验证
- **与 SlopCodeBench 的关系**：SlopCodeBench 揭示退化问题，Validation-in-the-Loop 是工程解决方案
- **启示**：go 命令中创建子智能体时，可以在创建过程中嵌入更多验证点（而非仅在最终检查清单）

| 工具/平台 | 定位 | 与我们的关系 |
|-----------|------|-------------|
| Letta | OS-like 分层内存 Agent 平台 | memory 架构参考 |
| Mem0 | 多层次个性化记忆 | 用户/会话/Agent 级记忆分离 |
| Graphiti | 时序知识图谱 | 因果关系与实体追踪 |
| SlopCodeBench | 代码退化基准 | 评估 Agent 长期代码质量 |
| Temporal | 持久执行框架 | Agent 任务可靠性 |
| LangGraph | Graph-based 状态机编排 | 生产级 Agent 编排首选 |
| DeepEval | DAG 确定性评估指标 | review 评估维度参考 |
| skills.sh (Vercel) | Skill 注册中心/市场 | 分发标准参考 |
| Cognee | 知识图谱 Agent Memory | 关系推理 + 结构化召回 |
| Zep | 时序知识图谱 Memory | 实体/意图提取 |
| TurboQuant (Google) | KV Cache 压缩 | 降低上下文内存/计算成本 |
| CrewAI | 角色驱动多 Agent 协作 | 团队模拟场景 |
| AutoGen / AG2 | 对话+事件驱动多 Agent | 研究和原型 |
| OpenAI Agents SDK | Handoff 原生多 Agent | 生产级工具包参考 |
| Maxim AI | Agent 可观测性平台 | 质量/性能/Token 监控 |
| Braintrust | CI/CD 评估集成 | 自动评估-改进循环 |
| Arize Phoenix | OTel-native Agent 可观测性 | 嵌入可视化 |
| A-Evolve | Git-Native Agent Evolution | 进化即 CI/CD，版本化变异 |
| KernelEvolve (Meta) | 自进化 Skill Library for Infrastructure | 生产级自进化技能库参考 |
| Agent0 (ICLR 2026) | Co-Evolutionary Dual-Agent | 双智能体自进化范式 |
