# 灵枢·AI全栈构建师 (Full Stack Architect)

> AI驱动的全栈开发指导系统 — 集成 Agent 工作流、Vibe Coding 方法论与 2026 最新技术栈，从需求到上线的全链路开发伙伴

![Cover](assets/fullstack-01-cover.png)

---

## Tags

`full-stack` `code-assistant` `agent-workflow` `vibe-coding` `web-development` `mobile-dev` `game-dev` `architecture` `2026-stack`

---

## 简介

灵枢·AI全栈构建师是一个专业的全栈开发指导技能包，蒸馏自 **Claude Code Agent 模式 6 个月生产实践**与 **Cursor/Devin/v0/Bolt.new/Lovable/Replit Agent 等主流 AI 开发工具的方法论精华**。系统集成 **Agent 工作流引擎**（计划-执行-验证循环）、**Harness Engineering v1.0 驾驭工程**（四大护栏 + 五大上下文模式）、**2026 最新技术栈知识库**与 **PRD 自动生成系统**，覆盖前端、后端、移动应用、游戏开发与架构设计全领域。无论你是寻求技术咨询、快速原型验证还是完整项目交付，全栈构建师都能提供可验证、可落地的专业指导。

---

## 功能特性

### Agent 工作流引擎

蒸馏自 Claude Code 6 个月生产实战的 **计划-执行-验证循环**：

```
1. 理解上下文 → 制定计划
2. 执行最小可验证步骤
3. 验证执行结果
4. 通过 → 提交继续 | 失败 → 回滚重试
5. 最大迭代 15 次，防止无限循环
```

三种工作模式灵活切换：

| 模式 | 适用场景 | 特点 |
|------|---------|------|
| 知识指导模式 | 技术咨询、最佳实践 | 直接获取技术指导 |
| 项目执行模式 | 从 PRD 到代码落地 | 完整 Agent 循环 |
| Vibe Coding 模式 | 快速原型、MVP | 自然语言 → 可运行应用 |

### Vibe Coding 方法论

蒸馏自 v0、Bolt.new、Lovable、Replit Agent 等主流 AI 开发工具的实战经验：

- **按场景选工具**：快速验证 → 展示页面 → 全栈 App → 企业工具，每个场景都有最优推荐
- **安全铁律内置**：绝不硬编码密钥、参数化查询强制、AI 生成代码安全审查必做
- **30 分钟可运行原型**：对话即可产出可部署的 MVP

### Harness Engineering（驾驭工程）v1.0

蒸馏自 Mitchell Hashimoto 的驾驭工程哲学，核心原则：**Humans steer. Agents execute.**

#### 四大护栏

| 护栏 | 说明 |
|------|------|
| 上下文工程 | 精准控制 Agent 可见的上下文范围，防止注意力涣散 |
| 渐进式披露 | 按需逐步展开知识细节，避免一次性信息过载 |
| 上下文压缩 | 智能精简历史交互，维持长对话中的高质量输出 |
| 上下文路由 | 根据任务类型自动匹配最相关的知识域 |

#### 五大上下文模式

| 模式 | 说明 |
|------|------|
| 演进检索 | 根据项目演进阶段动态调整知识检索策略 |
| 架构约束 | 在代码生成过程中实时校验架构一致性 |
| 反馈循环 | 质量检查 → 修复建议 → 验证 → 迭代的闭环 |
| 熵管理 | 防止 Agent 在长任务中偏离目标，维持任务聚焦 |
| 工具子集原则 | 限制单次可用的工具范围，降低误操作风险 |

### 7 步 Agent 流水线

完整的从需求到上线的自动化管线：

1. **Step 1 — 需求诊断与分析**：自动加载最新技术栈推荐，输出需求摘要 + 复杂度评估
2. **Step 2 — PRD 生成与校验**：自动生成完整 PRD（项目概述、技术栈、用户故事），规范性校验
3. **Step 3 — 架构设计与技术选型**：基于 19 个领域知识库提供最佳实践与架构评审
4. **Step 4 — 用户故事分解与执行**：粒度分解 + 子任务并行执行 + 代码模板匹配
5. **Step 5 — 代码质量验证**：代码审查 + 安全扫描 + 测试覆盖率检查（目标 ≥80%）
6. **Step 6 — 部署与上线**：Vercel/Cloudflare/Docker 多平台部署配置
7. **Step 7 — 知识更新与积累**：项目模式沉淀 + 知识库自动更新

### 知识体系覆盖

- **01_基础知识**：编程语言、数据结构、网络、操作系统
- **02_前端开发**：React 19/Vue 3、现代 CSS、移动端、游戏开发
- **03_后端开发**：Node.js/Python/Go、数据库、API 设计
- **04_全栈架构**：系统设计、微服务、云原生、CI/CD
- **05_项目实战**：网站、应用、游戏、开源项目
- **06_工具资源**：开发工具、学习资源、最佳实践
- **07_PRD 执行**：PRD 生成、用户故事分解、模式沉淀
- **08_AI 应用开发**：AI SDK、MCP 协议、Agent 架构

---

## 系统架构

### 四大支柱

```
┌──────────────────────────────────────────────────────────────────┐
│                 灵枢·AI全栈构建师 v1.0                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  支柱一：Agent 工作流引擎                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  计划 → 执行 → 验证 → 回滚/继续 (最大 15 次迭代)          │   │
│  │  知识指导 | 项目执行 | Vibe Coding 三种模式即时切换        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  支柱二：Harness Engineering v1.0                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  四大护栏：上下文工程 | 渐进式披露 | 上下文压缩 | 上下文路由│   │
│  │  五大模式：演进检索 | 架构约束 | 反馈循环 | 熵管理 | 工具集│   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  支柱三：知识库系统                                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  前端19+ | 后端15+ | 架构12+ | AI应用8+ | 安全10+ | ...   │   │
│  │  19 个领域最佳实践文档 + 5 种语言代码模板库                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  支柱四：执行层                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  代码生成器 | PRD系统 | NLP引擎 | 技术栈引擎 | AI模型引擎  │   │
│  │  代码模板库 | 集成运行时                                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 7 步 Agent 流水线详解

```
Step 1: 需求诊断
  ├── 理解用户开发需求
  ├── 评估技术栈选择（基于 2026 最新推荐）
  └── 输出：需求摘要 + 技术栈推荐 + 复杂度评级

Step 2: PRD 生成与校验
  ├── 自动读取 prd-modules/prd-generator.md + prd-checker.md
  ├── 需求澄清（3-8 个关键问题）
  ├── PRD 结构生成（项目概述、技术栈、用户故事等）
  └── 输出：完整 PRD 文档

Step 3: 架构设计
  ├── 自动读取 references/ 对应领域最佳实践
  ├── 技术栈推荐 + 架构评审
  └── 输出：架构设计文档 + 目录结构 + API 设计

Step 4: 代码执行
  ├── 用户故事分解（最小粒度）
  ├── 子 Agent 并行执行无依赖任务
  └── 输出：可运行代码

Step 5: 质量验证
  ├── 代码审查（逻辑、安全、性能）
  ├── 测试覆盖率 ≥ 80%
  └── 输出：质量报告 + 修复建议

Step 6: 部署上线
  ├── Vercel / Cloudflare Workers / Docker
  └── 输出：部署成功 + 访问 URL

Step 7: 知识更新
  └── 整理本次项目模式 → 沉淀入知识库
```

---

## 支持的技术栈

### 前端（2026 年 5 月）

| 技术 | 版本 | 推荐度 | 说明 |
|------|------|--------|------|
| React | 19 | ★★★★★ | Server Components + Actions + use() hook |
| Next.js | 15 | ★★★★★ | App Router + Turbopack + Streaming SSR |
| Bun | 1.2+ | ★★★★☆ | 运行时+包管理+构建，比 Node.js 快 3-5x |
| Tailwind CSS | v4 | ★★★★★ | 零配置，自动内容检测 |
| shadcn/ui | latest | ★★★★★ | 可组合组件，非 npm 依赖 |
| Vercel AI SDK | 4.x | ★★★★☆ | 构建 AI 应用的标准 SDK |

### 后端（2026 年 5 月）

| 技术 | 版本 | 推荐度 | 说明 |
|------|------|--------|------|
| Hono | 4.x | ★★★★★ | 边缘优先的 Web 框架，多运行时 |
| tRPC | v11 | ★★★★☆ | 端到端类型安全 API |
| Drizzle ORM | latest | ★★★★☆ | TypeScript 优先，轻量 SQL ORM |
| PostgreSQL | 16+ | ★★★★★ | 最可靠的关系数据库 |
| Lucia Auth | 3.x | ★★★★☆ | 轻量认证库 |
| Zod | 3.x | ★★★★★ | TypeScript schema 验证 |

### 移动端

| 技术 | 说明 |
|------|------|
| React Native (Expo) | 跨平台移动应用首选 |
| Flutter | Google 跨平台 UI 框架 |
| SwiftUI / Jetpack Compose | 原生开发 |

### 游戏开发

| 技术 | 说明 |
|------|------|
| Unity | 3D/2D 游戏引擎 |
| Phaser.js | HTML5 2D 游戏框架 |
| Three.js / R3F | Web 3D 图形库 |

### 部署平台

| 平台 | 推荐度 | 适用场景 |
|------|--------|---------|
| Vercel | ★★★★★ | Next.js 应用首选 |
| Cloudflare Workers | ★★★★☆ | 边缘计算、Hono API |
| Docker | ★★★★☆ | 自托管、微服务 |
| Deno Deploy | ★★★☆☆ | Deno 生态应用 |

---

## 快速开始

### 安装

在 ClawHub 技能市场中搜索 `full-stack-architect` 或 `全栈构建师`，点击安装即可。

### 触发词

以下任意关键词均可激活本技能：

- `全栈开发` / `架构设计` / `代码生成`
- `技术选型` / `项目开发` / `前端开发`
- `后端开发` / `移动开发` / `游戏开发`
- `部署上线` / `代码优化` / `技术咨询`

### 三种工作模式一览

| 模式 | 命令示例 | 适用场景 |
|------|---------|---------|
| 知识指导 | "React 19 Server Components 怎么用？" | 技术咨询、最佳实践 |
| 项目执行 | "帮我开发一个笔记应用" | 从 PRD 到代码到部署 |
| Vibe Coding | "快速做一个 Todo App 原型" | MVP、快速验证想法 |

---

## 使用示例

### 示例 1：技术咨询（知识指导模式）

```
用户：2026 年开发全栈应用推荐什么技术栈？

系统：[加载 tech_stack_recommendations.md]
推荐组合：Next.js 15 + Hono 4.x + PostgreSQL 16 + Drizzle ORM
前端：React 19 (Server Components) + Tailwind CSS v4 + shadcn/ui
后端：Hono API Routes + tRPC v11 + Zod 3.x
部署：Vercel (前端) + Cloudflare Workers (API)
AI 集成：Vercel AI SDK 4.x + MCP 协议
```

### 示例 2：完整项目开发（项目执行模式）

```
用户：帮我开发一个 Markdown 笔记应用

系统：[启动 7 步 Agent 流水线]
Step 1 → 需求诊断：笔记应用，复杂度中等
Step 2 → PRD 生成：项目概述 + 技术栈 + 8 个用户故事
Step 3 → 架构设计：Next.js App Router + Drizzle + SQLite
Step 4 → 代码执行：
  - US-01: 笔记 CRUD (React Server Components + Server Actions)
  - US-02: Markdown 渲染 (react-markdown + rehype-highlight)
  - US-03: 标签系统 (Drizzle many-to-many)
  - US-04: 搜索功能 (Full-text search)
  ...（共 8 个用户故事）
Step 5 → 质量验证：ESLint + 安全审查 + 测试覆盖率 82%
Step 6 → 部署：Vercel 一键部署
Step 7 → 知识积累：Markdown 编辑器模式沉淀入知识库
```

### 示例 3：Vibe Coding 快速原型

```
用户：做一个宠物社交 App 的 MVP

系统：[Vibe Coding 模式]
- 推荐：Bolt.new / Lovable（展示页面零门槛）
- 技术栈：Next.js 15 + Tailwind v4 + Supabase
- 核心功能：宠物档案 + 动态 Feed + 点赞评论
- 30 分钟内可运行原型，一键部署
```

### 示例 4：安全审查

```
用户：审查这段 API 代码的安全性

系统：[加载 security_best_practices.md]
发现问题：
1. 硬编码 API Key → 改为环境变量
2. SQL 字符串拼接 → 改为 Drizzle 参数化查询
3. 无认证中间件 → 添加 Lucia Auth
4. XSS 漏洞（未转义用户输入）→ 添加 DOMPurify
输出修复代码 + 最佳实践说明
```

---

## 与通用 AI 编程助手的对比

| 维度 | 通用 AI 编程助手 | 灵枢·AI全栈构建师 |
|------|-----------------|-------------------|
| 工作流 | 单次追问式 | 计划-执行-验证的 Agent 循环 |
| 知识管理 | 依赖模型训练数据 | 19 个领域知识库持续蒸馏 |
| PRD 生成 | 无结构化能力 | 自动生成 + 规范性校验 + 多轮迭代 |
| 架构约束 | 无一致性保障 | 实时架构校验，防止偏离 |
| 上下文管理 | 容易丢失上下文 | Harness Engineering 四大护栏 |
| 安全审查 | 需要人工检查 | 自动扫描 + 修复建议内置 |
| 代码质量 | 一次生成 | 自动审查 + 测试覆盖率检查 |
| Vibe Coding | 无区分 | Luxe/Medium/Pure 三种风格选型 |
| 技术栈推荐 | 可能过时 | 蒸馏 2026 年 5 月最新实践 |
| 迭代保护 | 容易无限循环 | 硬性 15 次上限 |

---

## 目录结构

```
full-stack-architect/
├── SKILL.md                       # 技能主文件（ClawHub 标准格式）
├── README.md                      # 本文件 — 完整使用文档
├── LICENSE                        # MIT-0 许可证
├── skill.json                     # 技能元数据
├── requirements.txt               # Python 依赖
├── knowledge_index.json           # 知识索引
│
├── assets/                        # 配图资源
│   ├── fullstack-01-cover.png     # 封面图（1200×630）
│   ├── fullstack-02-architecture.png # 架构图（1200×800）
│   ├── fullstack-03-usecase.png   # 使用场景（1200×800）
│   └── fullstack-04-compare.png   # 效果对比（1200×630）
│
├── ai-models/                     # AI 模型引擎
│   ├── code_generator.py
│   ├── text_generator.py
│   └── model_manager.py
│
├── code-generator/                # 代码生成器
│   ├── code_engine.py
│   └── code_quality.py
│
├── code_snippets/                 # 5 种语言代码模板库
│   ├── react_snippets.md          # React 19 模板
│   ├── vue_snippets.md            # Vue 3 模板
│   ├── python_snippets.md         # Python 模板
│   ├── go_snippets.md             # Go 模板
│   └── nodejs_snippets.md         # Node.js 模板
│
├── docs/                          # 核心文档
│   └── harness-engineering-framework.md  # 驾驭工程框架
│
├── integrations/                  # 集成与运行时
│   ├── agent_runtime/
│   └── platform_adapters/
│
├── nlp/                           # NLP 模块
│   ├── dialogue_manager.py
│   ├── entity_extractor.py
│   └── intent_recognizer.py
│
├── prd-modules/                   # PRD 系统
│   ├── prd-generator.md           # PRD 生成器
│   ├── prd-checker.md             # PRD 规范性校验
│   ├── story-executor.md          # 用户故事执行器
│   └── templates/                 # 行业模板
│       ├── e-commerce.md
│       ├── education.md
│       └── finance.md
│
├── project_examples/              # 项目实战案例
│   └── web_app_example/
│
├── references/                    # 19 个领域知识库
│   ├── frontend_performance.md
│   ├── backend_performance.md
│   ├── security_best_practices.md
│   ├── cloud_native_devops.md
│   ├── mobile_development.md
│   ├── nodejs_best_practices.md
│   ├── go_best_practices.md
│   ├── vue_best_practices.md
│   ├── react_composition_patterns.md
│   ├── tech_stack_recommendations.md
│   └── ...（共 19 个文件）
│
├── scripts/                       # 工具脚本
│   ├── prd_generator_enhanced.py
│   ├── prd_linter.py
│   ├── tech_stack_recommender.py
│   └── test_framework.py
│
├── tech-stack/                    # 技术栈推荐引擎
│   ├── recommendation_algorithm.py
│   ├── tech_database.json
│   └── trends_analyzer.py
│
└── web-interface/                 # Web 界面
    ├── index.html
    ├── script.js
    └── style.css
```

---

## 安全铁律

1. **绝不硬编码密钥**：所有 API Key 使用环境变量
2. **参数化查询**：数据库查询禁止拼接用户输入
3. **安全审查必做**：AI 生成代码必须经过安全审查才能部署
4. **最小权限原则**：MCP 服务器 / 数据库连接使用只读或受限权限
5. **测试覆盖 ≥80%**：未达标的代码不允许进入下一步

---

## FAQ

### Q1：全栈构建师和 Cursor/Copilot 有什么本质区别？

Cursor/Copilot 是代码补全工具，在单次交互中提供代码建议。全栈构建师是完整的 Agent 系统，执行"计划→执行→验证→回滚"的闭环工作流，涵盖从 PRD 生成到部署上线的全链路。

### Q2：Vibe Coding 模式的安全保障如何？

Vibe Coding 模式仍然受安全铁律约束。即使快速原型，也不会允许硬编码密钥或拼接 SQL。所有输出代码均通过安全审查层过滤。

### Q3：知识库会过时吗？如何更新？

知识库中的技术栈推荐已更新至 2026 年 5 月。系统内置趋势分析引擎，会追踪生态系统变化。每次项目完成后自动沉淀新知识。

### Q4：Harness Engineering 对用户透明吗？

是的。四大护栏（上下文工程、渐进式披露、上下文压缩、上下文路由）在幕后工作，用户不会感知到额外负担，但能体验到更连贯的长对话质量。

### Q5：支持哪些编程语言？

前端主要支持 TypeScript/JavaScript（React 19、Vue 3、Next.js 15），后端支持 TypeScript/Node.js、Python、Go。可通过代码模板库扩展更多语言。

### Q6：PRD 生成需要多长时间？

通常在 2-5 轮对话内完成。首轮生成结构骨架，后续轮次逐步澄清需求、细化用户故事、校验粒度一致性。复杂项目最多迭代 15 轮。

### Q7：项目执行模式适合什么规模的项目？

适合中小型项目（单人/小团队 1-4 周开发周期）。大型企业项目建议结合人工架构评审，系统提供最佳实践参考而非替代架构师判断。

### Q8：Vibe Coding 产出可以直接用于生产吗？

Vibe Coding 定位是快速原型和 MVP 验证，产出需经过完整的 Step 5（质量验证 + 安全审查）后方可上线。建议通过项目执行模式获得生产级代码。

---

*灵枢·AI全栈构建师 v1.0.0 | MIT-0 License | 2026-05-25 | 维护者：Drip618*