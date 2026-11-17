# 🛡️ Code Spec Guardian — 代码规范守护者

> **Analyze · Distill · Enforce · Evolve** — 让 AI 写出符合你项目规范的代码，而不是每次都"差不多就行"。

[中文](#中文介绍) | [English](#english-introduction)

---

## 中文介绍

### 🤔 为什么需要这个 Skill？

你有没有遇到过这样的情况：

- AI 帮你写了个组件，结果命名风格和项目里的完全不一样
- AI 生成的 API 接口，响应格式和团队约定对不上
- 改了个 Bug，AI 用的缩进是 2 空格，你项目用的是 4 空格
- 每次让 AI 写代码，都得在 prompt 里反复强调"用我们项目的风格"...

**Code Spec Guardian** 就是为了解决这个问题而生的。

### ✨ 它能做什么？

| 能力 | 说明 |
|------|------|
| 🔍 **自动分析** | 轻量脚本检测语言/框架，AI 语义分析提取命名风格、UI 配色、架构分层、API 约定、SQL 规范、Git 规范 |
| 📦 **分模块沉淀** | 规范按模块存储，按需加载，不会一股脑灌进上下文浪费 token |
| ⚡ **自动执行** | 每次写代码、改代码、修 Bug 时自动加载相关规范，生成的代码天然符合项目风格 |
| 🔄 **自进化** | 不是静态文档库，而是活的规范系统——从每轮对话中持续学习、提炼、进化，越用越懂你的项目 |

### 🧠 核心设计：按需加载，不浪费 Token

```
用户："帮我写一个用户列表接口"
  → 只加载 api-spec.md + architecture.md（≈2K tokens）
  → 不会加载 sql-spec.md / ui-style.md / git-spec.md

用户："修复这个 SQL 查询的 Bug"
  → 只加载 sql-spec.md + code-style.md
  → 不碰 UI 和 API 规范
```

对比一次性加载全部规范（可能 10K+ tokens），按需加载**节省 70%+ 上下文占用**。

### 🧬 自进化机制 — 越用越懂你的项目

这不是一个写好就扔的静态文档库，而是一个**活的规范系统**。它在每次对话中持续学习、提炼、进化，让 AI 写出的代码越来越贴合你的项目风格。

#### 进化是如何发生的？

```
你说了一句话 / 纠正了一段代码 / 表达了一个偏好
        ↓
  AI 识别出规范信号
        ↓
  归类到对应模块（代码风格？UI？架构？）
        ↓
  与现有规范对比
        ↓
  增量写入规范文件 ✍️
```

#### 5 种触发进化的信号

| 信号 | 示例 | AI 的反应 |
|------|------|----------|
| 你明确给出规范 | "我们项目用 2 空格缩进" | 直接写入 code-style.md |
| 你纠正了 AI 的代码 | "不要用 var，用 const" | 提取为命名规范条目 |
| 你表达了偏好 | "API 返回用下划线命名" | 写入 api-spec.md |
| 代码中体现了新约定 | AI 发现你的 Service 都用了某种模式 | 自动识别并记录 |
| 你否定了某条规范 | "这条不用遵循" | 标记为 deprecated |

#### 日常增量 vs 重大变更

- **日常增量**（静默执行，不打扰你）：
  - 新增一条命名规范 → 追加到文件末尾，标注 `[auto: 2026-07-28]`
  - 修改一条已有规范 → 更新内容，旧条目保留为注释 `[deprecated: 2026-07-28]`

- **重大变更**（必须你确认才写入）：
  - ❌ 删除已有规范条目
  - ❌ 更换核心架构方案（如 Redux → Zustand）
  - ❌ 更换 UI 体系（如 Element UI → Ant Design）
  - ❌ 一次性改动涉及 3 个以上模块
  - 确认方式：展示简洁 diff 摘要，等你点头才写入

#### 进化时间线示例

```
Day 1:  "分析项目规范" → 全量扫描，生成 6 个模块，42 条规范
Day 2:  你说"用单引号" → code-style.md 新增 [CODE-07] 引号规范
Day 3:  你说"API 返回用 camelCase" → api-spec.md 新增 [API-08]
Day 5:  你说"换掉 Moment，用 dayjs" → 重大变更确认 → architecture.md 更新
Day 7:  规范已积累 58 条，AI 写代码已经和你手写的一模一样了
Day 14: 新同事加入，AI 一上来就知道你们项目的所有约定
```

#### 为什么自进化很重要？

传统的规范文档有两个致命问题：**写完就过时** 和 **没人维护**。Code Spec Guardian 解决了这两个问题：

- 规范在你和 AI 的日常协作中**自然生长**，不需要额外花时间维护
- 每条规范都有来源标注和时间戳，你可以追溯它是怎么来的
- 冲突检测确保不会自相矛盾——有冲突时 AI 会停下来问你
- 规范文件纳入 Git 版本控制，团队所有人共享同一份不断进化的规范

### 📁 项目结构

```
code-spec-guardian/
├── SKILL.md                    # 路由入口 + 使用说明（极简）
├── README.md                   # 你正在看的这个文件
├── references/
│   ├── index.md                # 规范索引
│   ├── skill-meta.json         # Skill 版本元数据
│   ├── evolution.md            # 自进化机制详解
│   ├── code-style.md           # 代码风格规范模板
│   ├── ui-style.md             # UI 风格规范模板
│   ├── architecture.md         # 架构规范模板
│   ├── api-spec.md             # API 设计规范模板
│   ├── sql-spec.md             # SQL/数据库规范模板
│   ├── git-spec.md             # Git 规范模板
│   ├── python-style.md         # Python 规范模板
│   ├── java-style.md           # Java 规范模板
│   ├── go-style.md             # Go 规范模板
│   ├── node-style.md           # Node.js 规范模板
│   ├── php-style.md            # PHP 规范模板
│   ├── rust-style.md           # Rust 规范模板
│   ├── analyze-code-style.md   # 代码风格分析指引
│   ├── analyze-ui-style.md     # UI 风格分析指引
│   ├── analyze-architecture.md # 架构分析指引
│   ├── analyze-api-spec.md     # API 分析指引
│   ├── analyze-sql-spec.md     # SQL 分析指引
│   ├── analyze-git-spec.md     # Git 分析指引
│   ├── analyze-python.md       # Python 分析指引
│   ├── analyze-java.md         # Java 分析指引
│   ├── analyze-go.md           # Go 分析指引
│   ├── analyze-node.md         # Node.js 分析指引
│   ├── analyze-php.md          # PHP 分析指引
│   └── analyze-rust.md         # Rust 分析指引
└── scripts/
    └── analyze_project.py      # 轻量项目上下文提取器
```

### 🚀 快速开始

1. **将此 Skill 安装到你的 AI 助手中**（支持 OpenClaw / Claude 等支持 Skill 机制的 AI Agent）

2. **在你的项目目录下，告诉 AI：**
   ```
   分析项目规范
   ```

3. **AI 会自动：**
   - 扫描项目代码结构和关键文件
   - 在项目根目录生成 `.code-spec/` 目录
   - 按模块输出规范文件
   - 展示规范摘要供你确认

4. **之后每次写代码、改 Bug、做 Code Review，AI 都会自动参照规范执行** ✅

### 🎯 使用场景

| 你说的话 | AI 做的事 |
|---------|----------|
| "分析项目规范" | 全量扫描项目，生成所有规范文件 |
| "帮我写一个登录页面" | 加载 UI + 架构规范，按规范生成 |
| "修复这个接口的 Bug" | 加载 API + 架构规范，修复时遵循规范 |
| "重构这个 Service" | 加载架构 + 代码风格规范，按规范重构 |
| "这个 SQL 查询优化一下" | 加载 SQL 规范，优化后符合命名和索引约定 |
| "查看当前规范" | 展示规范索引和内容 |
| "重置规范" | 清空并重新分析 |

### 🧬 自进化机制

- **日常增量**：你在对话中纠正了 AI 的代码风格 → AI 自动提取并更新规范文件，静默完成
- **重大变更**：更换组件库、修改架构约定等 → AI 会展示变更摘要，**等你确认后才写入**

> 详细机制见上方「🧬 自进化机制 — 越用越懂你的项目」专节

### 📐 规范文件格式

每个模块文件统一格式，简洁高效：

```markdown
# UI 风格规范
> 适用范围: .vue/.jsx/.tsx/.css | 最后更新: 2026-07-28

### [UI-01] 主题色
- 主色：#1890ff（蓝色系）
- 辅助色：#52c41a / #faad14 / #ff4d4f
- 示例：`color: var(--primary-color);`

### [UI-03] 字号体系
- 正文：14px / 标题：16-24px / 小字：12px
- 使用 rem，基准 1rem = 14px
```

- 编号制：`[模块-序号]`，便于引用（如"按 [UI-03] 规范来"）
- 单文件不超过 150 行 / 4KB
- 每条规范不超过 3 行 + 1 个最小示例

### 🔗 适配的 AI 平台

- ✅ **OpenClaw** — 原生 Skill 支持
- ✅ **Claude (via Skill mechanism)** — 通过 Skill 加载
- ✅ **其他支持 Markdown 指令注入的 AI Agent** — 手动将 SKILL.md 内容注入 system prompt 即可

### 📄 License

MIT — 自由使用，欢迎贡献。

---

## English Introduction

### 🤔 Why This Skill?

Ever had this happen to you?

- AI writes a component, but the naming convention is totally different from your project
- AI generates an API endpoint, but the response format doesn't match your team's standard
- AI fixes a Bug, but uses 2-space indentation while your project uses 4
- Every time you ask AI to write code, you have to repeat "follow our project's style" in the prompt...

**Code Spec Guardian** exists to solve exactly this problem.

### ✨ What Can It Do?

| Capability | Description |
|------------|-------------|
| 🔍 **Auto-Analyze** | Scan project code to extract naming conventions, UI palettes, architecture patterns, API contracts, SQL standards, Git workflows |
| 📦 **Modular Distillation** | Specs stored per-module, loaded on-demand — no dumping everything into context and wasting tokens |
| ⚡ **Auto-Enforce** | Automatically loads relevant specs when writing code, fixing bugs, or doing code review — output naturally conforms to project standards |
| 🔄 **Self-Evolving** | Not a static doc library, but a living spec system — continuously learns, distills, and evolves from every conversation turn, understanding your project better the more you use it |

### 🧠 Core Design: Load On-Demand, Save Tokens

```
User: "Help me write a user list API"
  → Only loads api-spec.md + architecture.md (~2K tokens)
  → Does NOT load sql-spec.md / ui-style.md / git-spec.md

User: "Fix this SQL query bug"
  → Only loads sql-spec.md + code-style.md
  → Doesn't touch UI or API specs
```

Compared to loading all specs at once (potentially 10K+ tokens), on-demand loading **saves 70%+ context usage**.

### 🔄 Self-Evolving — Gets Smarter the More You Use It

This is not a static documentation library that you write once and forget. It's a **living spec system** that continuously learns, distills, and evolves from every conversation turn, making AI-generated code increasingly aligned with your project's conventions over time.

#### How Does Evolution Happen?

```
You say something / correct a piece of code / express a preference
        ↓
  AI identifies a spec signal
        ↓
  Routes to the corresponding module (code style? UI? architecture?)
        ↓
  Compares with existing specs
        ↓
  Incrementally writes to spec file ✍️
```

#### 5 Signals That Trigger Evolution

| Signal | Example | AI's Response |
|--------|---------|---------------|
| You explicitly state a rule | "We use 2-space indentation" | Writes directly to code-style.md |
| You correct AI's code | "Don't use var, use const" | Extracts as a naming convention entry |
| You express a preference | "API responses use snake_case" | Writes to api-spec.md |
| Code reveals a pattern | AI notices your Services all follow a certain pattern | Auto-identifies and records |
| You reject a spec | "Don't follow this one" | Marks as deprecated |

#### Daily Incremental vs Major Changes

- **Daily incremental** (silent, no interruption):
  - New naming convention → appended to file, tagged `[auto: 2026-07-28]`
  - Modified existing spec → updated, old entry kept as comment `[deprecated: 2026-07-28]`

- **Major changes** (require your confirmation):
  - ❌ Deleting an existing spec entry
  - ❌ Changing core architecture (e.g., Redux → Zustand)
  - ❌ Changing UI framework (e.g., Element UI → Ant Design)
  - ❌ Changes spanning 3+ modules at once
  - Confirmation: shows a concise diff summary, waits for your approval

#### Evolution Timeline Example

```
Day 1:  "Analyze project specs" → Full scan, 6 modules, 42 spec entries
Day 2:  You say "use single quotes" → code-style.md gets [CODE-07]
Day 3:  You say "API returns camelCase" → api-spec.md gets [API-08]
Day 5:  You say "replace Moment with dayjs" → Major change confirmed → architecture.md updated
Day 7:  58 spec entries accumulated, AI code matches your handwriting
Day 14: New teammate joins, AI knows all your project conventions from the start
```

#### Why Self-Evolution Matters

Traditional spec docs have two fatal flaws: **they go stale immediately** and **nobody maintains them**. Code Spec Guardian solves both:

- Specs **grow naturally** during your daily AI collaboration — no extra maintenance time needed
- Every entry has source attribution and timestamps for full traceability
- Conflict detection prevents contradictions — AI pauses to ask you when conflicts arise
- Spec files go in Git version control, so the whole team shares one continuously evolving spec

### 📁 Project Structure

```
code-spec-guardian/
├── SKILL.md                    # Route entry + usage guide (minimal)
├── README.md                   # This file
├── references/
│   ├── index.md                # Spec index
│   ├── skill-meta.json         # Skill version metadata
│   ├── evolution.md            # Self-evolution mechanism
│   ├── code-style.md           # Code style spec template
│   ├── ui-style.md             # UI style spec template
│   ├── architecture.md         # Architecture spec template
│   ├── api-spec.md             # API design spec template
│   ├── sql-spec.md             # SQL/Database spec template
│   ├── git-spec.md             # Git spec template
│   ├── python-style.md         # Python spec template
│   ├── java-style.md           # Java spec template
│   ├── go-style.md             # Go spec template
│   ├── node-style.md           # Node.js spec template
│   ├── php-style.md            # PHP spec template
│   ├── rust-style.md           # Rust spec template
│   ├── analyze-code-style.md   # Code style analyzer
│   ├── analyze-ui-style.md     # UI style analyzer
│   ├── analyze-architecture.md # Architecture analyzer
│   ├── analyze-api-spec.md     # API spec analyzer
│   ├── analyze-sql-spec.md     # SQL spec analyzer
│   ├── analyze-git-spec.md     # Git spec analyzer
│   ├── analyze-python.md       # Python analyzer
│   ├── analyze-java.md         # Java analyzer
│   ├── analyze-go.md           # Go analyzer
│   ├── analyze-node.md         # Node.js analyzer
│   ├── analyze-php.md          # PHP analyzer
│   └── analyze-rust.md         # Rust analyzer
└── scripts/
    └── analyze_project.py      # Lightweight project context extractor
```

### 🚀 Quick Start

1. **Install this Skill into your AI assistant** (works with OpenClaw / Claude / any AI Agent that supports Skill-style markdown instructions)

2. **In your project directory, tell the AI:**
   ```
   Analyze project specs
   ```

3. **The AI will automatically:**
   - Scan project code structure and key files
   - Generate a `.code-spec/` directory in your project root
   - Output spec files organized by module
   - Show a summary for your confirmation

4. **From now on, every time you write code, fix bugs, or do code review, the AI will automatically follow your specs** ✅

### 🎯 Use Cases

| What You Say | What AI Does |
|--------------|--------------|
| "Analyze project specs" | Full scan, generate all spec files |
| "Write a login page" | Loads UI + architecture specs, generates per spec |
| "Fix this API bug" | Loads API + architecture specs, fixes while conforming |
| "Refactor this Service" | Loads architecture + code-style specs, refactors properly |
| "Optimize this SQL query" | Loads SQL spec, optimization follows naming & index conventions |
| "Show current specs" | Displays spec index and content |
| "Reset specs" | Clears and re-analyzes |

### 🧬 Self-Evolution Mechanism

- **Daily incremental**: You correct AI's code style in conversation → AI auto-extracts and updates spec files silently
- **Major changes**: Switching component library, changing architecture patterns, etc. → AI shows a change summary and **waits for your confirmation before writing**

> See the "🧬 Self-Evolving — Gets Smarter the More You Use It" section above for full details

### 📐 Spec File Format

Each module file follows a unified, concise format:

```markdown
# UI Style Specification
> Scope: .vue/.jsx/.tsx/.css | Last updated: 2026-07-28

### [UI-01] Theme Colors
- Primary: #1890ff (blue)
- Semantic: #52c41a / #faad14 / #ff4d4f
- Example: `color: var(--primary-color);`

### [UI-03] Typography Scale
- Body: 14px / Heading: 16-24px / Small: 12px
- Use rem, base 1rem = 14px
```

- Numbered: `[MODULE-NN]` for easy reference (e.g., "follow [UI-03]")
- Max 150 lines / 4KB per file
- Each spec: max 3 lines + 1 minimal example

### 🔗 Compatible AI Platforms

- ✅ **OpenClaw** — Native Skill support
- ✅ **Claude (via Skill mechanism)** — Load as a Skill
- ✅ **Other AI Agents with markdown instruction injection** — Manually inject SKILL.md content into system prompt

### 📄 License

MIT — Free to use, contributions welcome.

---

## 📋 版本更新记录 | Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1.0 | 2026-07-28 | 多语言支持，新增 Python/Java/Go 分析指引 |
| 1.2.0 | 2026-07-29 | analyze_project.py 瘦身（23KB→4KB），AI 语义分析取代正则匹配 |
| 1.2.1 | 2026-07-29 | 修复路由表引用缺失文件，补充 Node/PHP/Rust 指引；分析指引全面改为 exec/read 直接探索；index.md 条目数修正；日常使用流程增加 .code-spec/ 存在检测；_meta.json 改名 skill-meta.json；模板增加项目特有约定占位 |
| 1.2.2 | 2026-07-29 | 修复 16 项问题：README 项目结构更新；analyze-*.md 清理残留旧字段引用；skill-meta.json 补充 6 个语言模块；语言分析指引统一写入 `<lang>-style.md`；脚本配置文件列表补全多语言；SKILL.md 完成播报改为动态数量；区分 skill-meta.json 与产出 _meta.json；新增重新分析流程 |
| 1.2.3 | 2026-07-29 | 第三次审查修复 8 项：SKILL.md 路由表分隔列数修复；analyze-architecture.md 标题前缺空行；脚本改为多语言检测（`language` → `languages` 数组）；frameworks 检测改精确匹配避免子串误报；read_head 改用 utf-8-sig 兼容 BOM 文件；TypeScript 路由行改为说明性注释；步骤 4 补充读模板说明；README changelog 更新 |
| 1.2.4 | 2026-07-29 | 修复 ClawHub latest 未更新问题：改用 sync --bump 顺序发布，确保新版本被提升为 latest；README changelog 补全发布记录 |

---

<div align="center">

**⭐ If this helped you, give it a star! ⭐**

Made with ❤️ for developers who care about code quality.

</div>
