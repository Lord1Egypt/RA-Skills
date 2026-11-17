# Vercel 案例：把 AI-first CLI 哲学推到底

Vercel CEO Guillermo Rauch 把 CLI 定位为 **"cloud for agents"** 的关键嵌入接口：当 OpenClaw、Claude Code 等工具把用户引入 Vercel 的 agentic 基础设施时，CLI 就是那道门。随着这类嵌入场景爆发，CLI 的设计假设必须从"人敲"转向"agent 调"。下面是 Vercel 在三个层面落地这套哲学的实证。

## 1. CLI 转零依赖、自更新、签名的原生二进制

- 推出可选的**原生二进制**：启动更快、无需 Node.js 运行时依赖。
- **代码签名**：OS 可验证二进制来自 Vercel 且未被篡改。
- 跨 macOS / Linux / Windows × x64 / arm64，`vercel` / `vc` 自动匹配 OS 与 CPU 架构。
- 对应原则 7（零依赖自包含）+ 11（确定性）：agent 在临时沙箱里反复拉起工具时，依赖链是不可预测性和攻击面的来源；单一签名二进制可信、快、无惊喜。

## 2. Docker inside Vercel Sandbox（2026-05-29 上线）

- agent 可在隔离沙箱内 **build 容器、装系统包、改文件**，不碰宿主机。
- 配合**持久化沙箱**，Docker 安装与拉取的镜像**跨会话保留**。
- 新增 **FUSE 文件系统驱动**与 **VPN 客户端**支持。
- 典型用途：跑 Redis/Postgres 作测试依赖、部署前验证镜像、从容器预览应用。
- 角色：Sandbox = agent 的**可计算执行环境**——CLI 是接口，Sandbox 是 agent 安全执行副作用的地方。

### 为什么是 microVM，而不是容器（深度调研 3-0 验证）

这是 agent-first 基础设施最被低估的一条哲学：**agent 生成的代码默认是不可信的**。

- 现状判断（已验证）：*"大多数 AI agent 今天直接以宿主机完整权限执行生成的代码"* —— 这是默认的、危险的姿势。
- Vercel 的回应：Sandbox 提供**短生命周期的 Linux microVM**，按 **trust-domain（信任域）做 VM 级隔离**，而非容器级共享内核。被定位为 *"cloud computers"* / agent 的**安全执行层**。
- 配套：开源 SDK + CLI + 一个 API，让 agent "启动一批隔离环境"。
- 对设计哲学的提炼：**当工具会执行 agent 产出的代码/命令时，隔离边界要做到 VM 级，输入校验（原则 9）只是第一层。** "信任域"是比"权限"更准的心智模型——同一 agent 的不同任务可能就该分属不同信任域。

> 注意（已被对抗式验证**驳回**，勿采信）："Sandbox 可用单个 API 调用克隆并启动数百万 agent" —— 此说法 1-2 未通过，属营销夸张。可信的是"快速、按需启动隔离环境"，不是"百万级单调用"。

## 3. Zero 语言：连编程语言本身都做成 agent 接口

Vercel Labs 的实验性系统语言（`vercel-labs/zero`，Apache-2.0，预发布），与 C/Rust 同空间但**编译器与工具链从第一天就设计给 agent 消费**：

- **结构化 JSON 诊断**：`zero check --json` 输出稳定错误码（如 `NAM003`）+ human message + typed `repair` 对象（可执行修复 ID）。
- **图优先编辑**：agent 不 patch 文本，而对编译器派生的 **ProgramGraph** 做带 graph-hash 校验的语义编辑（`zero graph patch`），把"改→格式化→重解析→检查"塌缩成一条编译器中介操作。
- **统一 CLI**：`zero check/run/build/explain/fix/skills`，agent 不用猜调哪个工具；`zero explain CODE` 给结构化解释，`zero fix --plan --json` 给机器可读修复计划。
- **版本对齐指引**：`zero skills` 随编译器版本下发用法，解决文档漂移。
- **可预测资源模型**：无强制 GC、无隐藏分配器、无隐式 async、无魔法全局；I/O 走能力对象，effect 写在签名里。
- 编译出 **<10 KiB** 原生二进制，零依赖。

Zero 是这套哲学的"极限版"：CLI 改造是让**现有云对 agent 可调用**；Zero 是把**最底层的砖（语言/编译器）也重做成 agent 的接口**。同一判断的两端：未来软件的主要读者/写者是 agent。

## 4. 一核多面：MCP + SDKs 作为标准层（深度调研 3-0 验证）

Vercel 把 SDKs、Sandboxes、Runtime Cache、Blob 定位为 agent 开发的**标准层**而非可选插件，并通过 **Framework Defined Infrastructure / 零配置**（"你写后端代码，Vercel 决定怎么跑"）和针对 agent "大量空等" 负载的 **Fluid compute + Active CPU Pricing** 计费，统一到同一编排、计算、存储层。对应原则 12。已验证的具体落点：

- **四个面，一个核**：Vercel 明确把 **CLI、API、MCP server、git** 一并定位为"给 agent 的接口/表面"——不是四个产品，是同一能力的四种调用形态。
- **Vercel MCP**：一个**安全、OAuth 合规**的 MCP server，开箱与 Claude（Code/Desktop）等 AI 工具集成。MCP 在这里是"标准层"的协议端点，不是另起炉灶。
- **AI SDK 6 的关键转变**：把 `Agent` 从一个**类（class）重定义为一个接口（interface）**——即 agent 是一组可组合的能力契约，而非某个具体实现；并扩展了 MCP 支持。AI SDK 作为**跨 provider 的标准/抽象层**。
- **`mcp-to-ai-sdk`**：一个 CLI，从 MCP server **生成静态、版本化的 AI SDK 工具**。这正是原则 5（自描述）+ 11（确定性）的工程化：把动态协议固化成版本对齐的静态工具，agent 拿到的是确定契约而非运行时协商。

## 5. OpenClaw / Claude Code 如何嵌入（证据偏弱，谨慎）

- `vercel-labs/vercel-openclaw` 是真实存在的一手仓库；另有社区 `Enderfga/openclaw-claude-code`。
- Vercel 提供把 **Claude Agent SDK 跑在 Vercel Sandbox** 上的官方指引（`vercel.com/kb/guide/using-vercel-sandbox-claude-agent-sdk`），以及 AI Gateway 的 coding-agents 文档。
- **诚实警告**：深度调研给出的 caveat 是 *"OpenClaw 嵌入证据偏弱（under-evidenced）"*。"这些工具把用户引入 Vercel agentic 基础设施" 是 Rauch 的叙事方向，仓库与集成路径是实的，但"爆发式增长 / 大规模嵌入"目前主要是一方说法，缺独立佐证。引用时按"方向成立、规模待证"处理。

## 调研偏差声明

本案例的来源**几乎全部是 Vercel 一方**（官方 blog / changelog / docs / Rauch 推文）。对抗式验证只能确认"Vercel 是否如此宣称且内部一致"，**不能**确认这些设计在生产中的实际优劣。第三方批评源（truefoundry / qovery / northflank）质量被标为 blog 级。把本文当作"Vercel 的方法论自述 + 已祛除明显夸张"，而非中立横评。
