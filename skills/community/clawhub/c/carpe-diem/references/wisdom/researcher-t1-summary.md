# Anthropic 工程博客文章摘要

## 1. Claude Code Best Practices
**URL:** https://www.anthropic.com/engineering/claude-code-best-practices

### 核心问题
如何有效使用 Claude Code 这一自主编码环境，最大化其上下文窗口利用率，减少人工干预，同时避免常见陷阱。

### 关键洞察
1. **上下文窗口是核心资源**：LLM 性能随上下文窗口填充而下降，管理上下文是最重要的资源管理技能。给 Claude 提供验证手段（测试、构建、截图比对）让它能闭环工作。
2. **探索 → 规划 → 编码四阶段工作流**：先用 plan mode 探索和规划，再切换到编码模式执行，最后提交。避免"直接跳到写代码"导致解决错误问题。
3. **CLAUDE.md 是持久化记忆的关键**：项目级规则文件，包含 bash 命令、代码风格、工作流规则。但必须保持精简——每行都要问"删掉这行会导致 Claude 犯错吗？"，否则关键规则会被淹没。
4. **技能（Skills）和子代理（Subagents）扩展能力**：Skills 提供领域知识，子代理在独立上下文窗口中执行隔离任务，hook 是确定性保障。
5. **有效沟通技巧**：像问资深工程师一样问问题；让 Claude 先面试你，生成完整 spec 再执行；使用 `/clear` 在不同任务间重置上下文。

### 可迁移的模式
- 开发者应始终为 AI 提供可执行的验证检查（测试、lint、截图对比），让 AI 能自我迭代
- 用 CLAUDE.md 固化项目约定，但保持精简；定期审查和修剪
- 复杂任务走"探索→规划→编码→提交"四阶段，简单任务直接执行
- 使用子代理进行独立研究或审查，避免主上下文被污染

### 反向提醒
- 不要过度指定 CLAUDE.md——太长的规则文件会被忽略
- 规划模式有开销，小改动（修 typo、加日志）可直接执行
- 不要在同一个 session 里混入不相关任务——上下文污染会降低性能

---

## 2. Building Effective Agents
**URL:** https://www.anthropic.com/engineering/building-effective-agents

### 核心问题
如何构建有效的 LLM 代理系统？在什么情况下应该使用 workflow 模式，什么情况下使用 autonomous agent 模式？

### 关键洞察
1. **Workflow vs. Agent 的区分**：Workflow 是 LLM 和工具通过预定义代码路径编排的系统；Agent 是 LLM 动态控制自身流程和工具使用的系统。最成功的实现使用简单、可组合的模式，而非复杂框架。
2. **五种基本 Workflow 模式**：
   - **Prompt Chaining**：将任务分解为序列步骤，适合可清晰分解的任务
   - **Routing**：分类输入并路由到专门化的后续任务，适合有不同类别的情况
   - **Parallelization**：同时运行独立子任务（Sectioning）或同一任务多次（Voting）
   - **Orchestrator-Workers**：中央 LLM 动态分解任务并委派给 worker LLM
   - **Evaluator-Optimizer**：一个 LLM 生成，另一个评估和反馈，循环迭代
3. **Agent 的核心机制**：LLM 在循环中使用工具，基于环境反馈自主决策。需要精心设计工具集和文档（ACI = Agent-Computer Interface）。
4. **三条核心原则**：保持设计简单性、优先透明性（显式展示规划步骤）、精心设计工具文档和测试。
5. **框架的陷阱**：框架增加了抽象层，掩盖了底层 prompt 和响应，使调试更困难。建议先用 LLM API 直接实现，理解后再使用框架。

### 可迁移的模式
- 从最简单的方案开始，只在需要时才增加复杂度
- 先评估单次 LLM 调用 + 检索 + 上下文示例是否足够
- 根据任务特性选择正确的 workflow 模式，而不是盲目使用 agent
- 工具设计投入与 HCI 设计同等甚至更多的精力（ACI 原则）

### 反向提醒
- 并非所有场景都需要 agentic 系统——简单方案通常更好
- Agent 有更高的延迟和成本，可能有复合错误的风险
- 在沙盒环境中充分测试后再部署 agent
- 不要被框架的便利性诱惑——理解底层机制才能做好调试

---

## 3. Equipping Agents for the Real World with Agent Skills
**URL:** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

### 核心问题
如何用可组合、可扩展、可移植的方式为通用 AI 代理配备领域专业知识？

### 关键洞察
1. **Agent Skills 的核心理念**：一个 Skill 是一个包含 `SKILL.md` 文件的目录，通过渐进式揭露（Progressive Disclosure）机制让代理按需加载知识，避免上下文窗口被一次性填满。
2. **三层渐进式揭露**：第一层是 metadata（name + description），代理启动时预加载在系统 prompt 中；第二层是 SKILL.md 全文，在代理认为相关时加载；第三层是 SKILL.md 中引用的附加文件，仅在需要时加载。
3. **Skills 与代码执行**：Skills 可以包含预写的 Python 脚本等代码，代理可以执行这些确定性代码来完成任务（如 PDF 表单字段提取），比 LLM 生成更高效可靠。
4. **开发迭代方法**：先用评估发现代理能力缺口，再增量构建 Skill 来填补；从 Claude 的视角观察它如何使用 Skill；让 Claude 在完成任务时自省并记录经验到 Skill 中。
5. **安全考虑**：仅从可信来源安装 Skill，安装前审计文件内容，特别关注代码依赖和外部网络连接指令。

### 可迁移的模式
- 用技能替代长 prompt：将领域知识打包成可复用的 Skill，而不是塞进系统 prompt
- 渐进式揭露设计：让代理按需发现和加载知识，而不是一次性加载所有内容
- 用确定性代码替代 LLM 生成：对排序、表单提取等操作，用预写脚本更高效可靠
- 让代理自省并记录经验：通过 Claude 的自我反思来发现它真正需要的上下文

### 反向提醒
- 恶意 Skill 可能引入安全漏洞——需要审计来源和内容
- Skill 过大会导致上下文膨胀，需要用渐进式揭露来管理
- 并非所有知识都适合用 Skill 封装——与当前项目高度绑定的约定更适合放进 CLAUDE.md

---

## 4. Effective Context Engineering for AI Agents
**URL:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

### 核心问题
从 prompt engineering 进化到 context engineering——如何有效策划和管理 AI 代理的上下文，使其在有限注意力预算下保持最佳表现？

### 关键洞察
1. **Context Engineering vs. Prompt Engineering**：Prompt engineering 关注如何写 prompt；Context engineering 关注如何策划和维护推理时的全部 token 集合（系统指令、工具、MCP、外部数据、消息历史等），是一个迭代的、每轮推理都发生的策划过程。
2. **上下文腐烂（Context Rot）**：随着上下文窗口 token 数增加，模型准确回忆信息的能力下降。这是所有 LLM 的共性，源于 Transformer 架构的 n² 成对注意力关系。
3. **"最小高信号 token 集"原则**：好的 context engineering 是找到最小的、信号最强的 token 集，最大化期望输出的可能性。系统 prompt 应处于"刚好合适的高度"——既不过度硬编码，也不过于模糊。
4. **三种长时任务技术**：
   - **Compaction（压缩）**：在上下文接近限制时，让模型总结并压缩关键信息，丢弃冗余工具输出
   - **Structured Note-taking（结构化笔记）**：代理定期将笔记写到上下文之外的持久内存，如 NOTES.md 文件
   - **Sub-agent Architectures（子代理架构）**：专门化的子代理在干净的上下文中处理聚焦任务，向主代理返回浓缩摘要
5. **"Just-in-time" 上下文策略**：代理维护轻量级标识符（文件路径、查询、链接），运行时动态加载数据，而非一次性预处理所有数据。这类似于人类的认知模式——不记忆全部信息，而是通过文件系统和组织系统按需检索。

### 可迁移的模式
- 把上下文当作有限资源管理：每个新 token 都消耗注意力预算
- 系统 prompt 保持清晰简洁，用 XML 标签或 Markdown 标题分节
- 工具集要精简：如果一个人类工程师不确定该用哪个工具，AI 代理更不可能做好
- 对长时任务使用压缩、结构化笔记、子代理三种技术

### 反向提醒
- 压缩可能丢失细微但关键的信息——需要精心调优压缩 prompt
- 运行时探索比检索预计算数据慢——需要权衡速度与灵活性
- 更大的上下文窗口不会自动解决上下文污染问题
- 工具过多会导致代理在工具选择上犹豫不决

---

## 5. Effective Harnesses for Long-Running Agents
**URL:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

### 核心问题
AI 代理如何在多个上下文窗口之间保持一致性，实现跨小时甚至跨天的持续工作？

### 关键洞察
1. **长期运行代理的核心挑战**：代理必须在离散的 session 中工作，每个新 session 从零开始，没有之前会话的记忆。类比为"轮班工程师"——每个新班次来的工程师对之前发生的事情一无所知。
2. **双部分解决方案**：
   - **Initializer Agent（初始化代理）**：第一个 session 使用专用 prompt，设置环境（init.sh 脚本、claude-progress.txt 进度文件、初始 git commit）
   - **Coding Agent（编码代理）**：后续每个 session 要求代理做增量进展，然后留下结构化更新
3. **Feature List 是关键设计**：初始化代理编写包含 200+ 条功能需求的 JSON 文件，每条标记为"未通过"。后续编码代理每次只处理一个功能，仅修改 `passes` 字段状态——防止代理一次性完成过多或过早宣布胜利。
4. **增量进展 + 清洁状态**：代理每次只做一个功能，通过 git commit 和有意义的提交信息来保持代码库清洁，在进度文件中记录摘要。这让后续 session 能快速通过 git log 和进度文件了解当前状态。
5. **端到端测试**：初始化代理写一个 `init.sh` 脚本启动开发服务器，编码代理在 session 开始时先测试基本功能是否正常，确保没有被遗留的 bug 影响。

### 可迁移的模式
- 为长期运行的任务创建功能清单文件，每条功能标记完成状态
- 使用初始化代理设置环境骨架，后续代理只做增量变更
- 用进度文件（如 claude-progress.txt）+ git 历史作为跨 session 的通信机制
- 每个 session 结束时让代理提交代码、写进度更新，保持清洁状态
- 让代理在开始新功能前先做端到端测试，确认现有功能正常

### 反向提醒
- 这种方案针对全栈 Web 应用做了优化，其他领域（科学研究、金融建模）可能需要调整
- 浏览器自动化工具有局限性（如 Claude 看不到浏览器原生 alert 弹窗）
- 单一通用编码代理 vs. 多代理架构（专门的测试代理、QA 代理）的优劣尚无定论
- 功能清单的维护需要强约束——代理倾向于不恰当地修改或删除测试条目

---

## 6. How We Built Claude Code Auto Mode
**URL:** https://www.anthropic.com/engineering/claude-code-auto-mode

### 核心问题
如何在减少用户审批疲劳的同时，保障 AI 代理自主操作的安全性？

### 关键洞察
1. **Auto Mode 的定位**：介于手动审批和 `--dangerously-skip-permissions` 之间的中间地带——用模型分类器替代人工审批，兼顾安全性和流畅性。用户实际批准了 93% 的权限请求。
2. **双层防御架构**：
   - **输入层**：Prompt Injection Probe 在工具结果进入上下文前扫描，发现劫持企图时在上下文中添加警告
   - **输出层**：Transcript Classifier（基于 Sonnet 4.6）在每次工具调用执行前评估，两级过滤（快速单 token 过滤器 → 仅在被标记时进入 CoT 推理）
3. **四级威胁模型**：过度积极行为（最常见）、诚实错误（误解影响范围）、Prompt 注入、模型不对齐。分类器主要针对前两种。
4. **三层权限决策**：Tier 1 内置安全白名单（只读操作）→ Tier 2 项目内文件操作（无需分类器）→ Tier 3 转录分类器（shell 命令、网络请求、外部工具等）
5. **实际性能**：在 10,000 个真实调用中，完整 pipeline 的误报率仅 0.4%，但对真实过度积极行为的漏报率为 17%。分类器禁用了已知授予任意代码执行的权限规则（如通配符脚本解释器）。

### 可迁移的模式
- 使用两级分类器架构：快速过滤 + 仅在需要时进行深度推理，平衡效率与召回率
- 剥离助手文本和工具结果，让分类器只基于用户消息和工具调用做判断——防止代理说服分类器
- 拒绝-继续机制：被阻止的操作不中断会话，代理尝试更安全的方法；连续 3 次拒绝或累计 20 次则升级给人类
- 子代理切换时的双向检查：委派出去时和返回结果时都做安全检查

### 反向提醒
- Auto mode 不是在高风险基础设施上替代人工仔细审查的方案
- 对真实过度积极行为 17% 的漏报率意味着仍有风险
- 输入层 + 输出层的双重防御体系需要持续维护和更新测试集
- 分类器在判断"用户是否真正授权了某个操作"上仍有困难

---

## 7. Contextual Retrieval
**URL:** https://www.anthropic.com/engineering/contextual-retrieval

### 核心问题
如何改进 RAG（检索增强生成）的检索步骤，解决传统 RAG 在分块时丢失上下文的问题？

### 关键洞察
1. **传统 RAG 的上下文困境**：文档被拆分成小块后，单个块缺乏上下文。例如，块内容为"公司营收比上一季度增长 3%"，但丢失了公司名称和时间信息，导致检索失败。
2. **Contextual Retrieval 方案**：在嵌入和创建 BM25 索引之前，为每个块预置块特定的上下文说明（通常 50-100 tokens）。使用 Claude 3 Haiku 生成这些上下文——输入整个文档和当前块，让模型生成简洁的上下文描述。
3. **性能提升数据**：
   - Contextual Embeddings 单独使用：Top-20 检索失败率降低 35%
   - Contextual Embeddings + Contextual BM25：失败率降低 49%
   - 加上 Reranking（重排序）后：失败率降低 67%（5.7% → 1.9%）
4. **Prompt Caching 降低成本**：利用 Claude 的 prompt caching 功能，文档只需加载一次到缓存中，对每个块生成上下文的成本约为每百万文档 token 1.02 美元。
5. **所有技术栈可叠加**：Contextual Embeddings + Contextual BM25 + Reranking + Top-20 chunks 的组合效果最好，每种技术都贡献了独立的改进。

### 可迁移的模式
- 如果知识库小于 200,000 tokens，直接用完整 prompt 缓存，无需 RAG
- 使用 Contextual Retrieval 时，用 Claude 自动为每个块生成上下文，而非手动标注
- 结合语义搜索（Embeddings）和精确匹配（BM25）获得最佳检索效果
- 添加 Reranking 步骤进一步提高 Top-K 结果质量

### 反向提醒
- Contextual Retrieval 是预处理步骤，需要在索引阶段完成，不适合实时变化的数据
- 生成上下文增加了索引成本，但运行时没有额外开销
- 更多块不总是更好——达到一定数量后，更多信息可能分散模型注意力
- 不同嵌入模型受益程度不同，需要针对具体场景评估
- 对于小知识库（<200k tokens），直接使用完整 prompt + 缓存可能更简单有效