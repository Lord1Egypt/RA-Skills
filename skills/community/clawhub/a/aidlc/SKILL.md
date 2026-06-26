---
name: aidlc
description: >
  AI-Driven Development Life Cycle (AI-DLC) adaptive workflow for software development.
  Use when: starting a new project, new feature, bug fix, refactoring, migration, or any dev task.
  Chinese triggers: 新项目, 开始开发, 做个功能, 修复bug, 重构, 新需求, 新建项目.
  English triggers: start a project, new feature, AI-DLC, aidlc, inception, construction.
  Implements full AI-DLC methodology: workspace detection, adaptive requirements, user stories,
  workflow planning, design, code generation, and build/test.
---

# AI-DLC: AI-Driven Development Life Cycle

AI-DLC 是一种结构化但自适应的软件开发方法论，由 AI 主导流程、人审批把关。

## 核心原则

**流程适应工作，而不是反过来。** AI 根据请求复杂度、现有代码库状态和风险评估，智能决定需要执行哪些阶段。

- 简单变更 → 只执行必要阶段
- 复杂项目 → 完整三阶段 + 所有保障机制
- 每个阶段都有审批门控，必须人确认后才能继续

## 三阶段概览

```
用户请求 → INCEPTION → CONSTRUCTION → OPERATIONS → 完成
            (计划)      (构建)        (运营)
```

### 🔵 INCEPTION 阶段 — 做什么 + 为什么
- **Workspace Detection** (始终执行) — 分析是 greenfield 还是 brownfield
- **Reverse Engineering** (brownfield 有现有代码时执行) — 分析现有代码库
- **Requirements Analysis** (始终执行，深度自适应) — 收集需求并提问澄清
- **User Stories** (条件执行) — 创建用户故事和角色
- **Workflow Planning** (始终执行) — 确定执行计划
- **Application Design** (条件执行) — 高层组件设计
- **Units Generation** (条件执行) — 拆解为工作单元

### 🟢 CONSTRUCTION 阶段 — 怎么做
- **Per-Unit Loop** (每个工作单元依次执行):
  - Functional Design (条件执行)
  - NFR Requirements (条件执行)
  - NFR Design (条件执行)
  - Infrastructure Design (条件执行)
  - Code Generation (始终执行) — Part 1 计划 → Part 2 生成
- **Build and Test** (始终执行) — 构建、单元测试、集成测试

### 🟡 OPERATIONS 阶段 — 部署 (占位)

---

## MANDATORY: 工作流执行规则

### 规则文件加载顺序

**开始工作流时，必须按此顺序加载规则文件：**

1. 加载 `references/common/welcome-message.md` — 显示欢迎消息（新项目只执行一次）
2. 加载 `references/common/process-overview.md` — 工作流概览图
3. 加载 `references/common/session-continuity.md` — 会话恢复指引
4. 加载 `references/common/question-format-guide.md` — 问题格式规范
5. 扫描 `references/extensions/` 目录 — 加载所有扩展规则

### MANDATORY: 内容验证
在创建**任何文件之前**，必须按 `references/common/content-validation.md` 验证内容。

### MANDATORY: 问题文件格式
**禁止在聊天中直接提问**。所有问题必须写入 `.md` 文件，使用 `[Answer]:` 标签格式，详见 `references/common/question-format-guide.md`。

### MANDATORY: 审计日志
**所有用户输入必须原样记录**到 `aidlc-docs/audit.md`（时间戳用 ISO 8601）。禁止总结或改写用户原话。

### MANDATORY: 审批门控
每个阶段完成后，必须等待用户明确批准才能进入下一阶段。使用标准两选项格式：
- 🔧 **Request Changes** — 请求修改
- ✅ **Continue** — 继续下一阶段

### MANDATORY: 复选框更新
完成任何计划步骤后，**必须立即**在该交互中将步骤标记为 `[x]`。

---

## 完整工作流

### Step 0: 初始化（新项目）

1. 检查是否存在 `aidlc-docs/aidlc-state.md`
   - **存在** → 读取状态，从上次阶段恢复
   - **不存在** → 新项目，创建状态文件，继续检测工作区
2. 检查是否存在现有代码
3. 显示欢迎消息（新项目只执行一次）
4. 自动进入下一阶段

### Step 1: Workspace Detection (始终执行)

读取 `references/inception/workspace-detection.md`，按步骤执行。

- 扫描工作区判断 greenfield / brownfield
- 更新 `aidlc-docs/aidlc-state.md`
- 自动进入下一阶段（无需用户审批）

### Step 2: Reverse Engineering (brownfield 条件执行)

读取 `references/inception/reverse-engineering.md`，按步骤执行。

- 分析现有代码库，生成 architecture.md, component-inventory.md, api-documentation.md 等
- **必须等待用户明确批准**后才能继续

### Step 3: Requirements Analysis (始终执行，自适应深度)

读取 `references/inception/requirements-analysis.md`，按步骤执行。

深度级别：
- **Minimal** — 简单请求，只记录意图
- **Standard** — 正常复杂度，收集功能和 NFR
- **Comprehensive** — 复杂高风险，详细需求 + 追溯性

- 始终创建 `aidlc-docs/inception/requirements/requirement-verification-questions.md`（除非需求极其清晰）
- 等待用户回答所有 `[Answer]:` 标签
- 分析答案中的矛盾/歧义，必要时创建追问文件
- 生成 `aidlc-docs/inception/requirements/requirements.md`
- **必须等待用户明确批准**

### Step 4: User Stories (条件执行)

读取 `references/inception/user-stories.md`，按步骤执行。

**执行条件**（满足任一即执行）：
- 新用户功能、用户体验变化、多用户类型
- 需要验收标准的复杂业务逻辑
- 跨团队协作

**跳过条件**：
- 纯内部重构、明确范围的 bug 修复、技术债务清理

分为两部分：
- **Part 1 Planning** — 创建故事计划 + 提问 → 等待批准
- **Part 2 Generation** — 生成 stories.md + personas.md → 等待批准

### Step 5: Workflow Planning (始终执行)

读取 `references/inception/workflow-planning.md`，按步骤执行。

- 加载所有前序上下文
- 创建 `aidlc-docs/inception/plans/execution-plan.md`
- 展示推荐方案（执行哪些阶段，跳过哪些，说明原因）
- **必须等待用户明确批准**

### Step 6: Application Design (条件执行)

读取 `references/inception/application-design.md`，按步骤执行。

- **必须等待用户明确批准**

### Step 7: Units Generation (条件执行)

读取 `references/inception/units-generation.md`，按步骤执行。

- **必须等待用户明确批准**

### Step 8: Construction — Per-Unit Loop

对于每个工作单元，依次执行（跳过不适用的）：

1. **Functional Design** (条件执行) — 读取 `references/construction/functional-design.md`
2. **NFR Requirements** (条件执行) — 读取 `references/construction/nfr-requirements.md`
3. **NFR Design** (条件执行) — 读取 `references/construction/nfr-design.md`
4. **Infrastructure Design** (条件执行) — 读取 `references/construction/infrastructure-design.md`
5. **Code Generation** (始终执行) — 读取 `references/construction/code-generation.md`
   - Part 1: 创建详细代码生成计划 → 等待批准
   - Part 2: 执行计划生成代码 → 等待批准

每个阶段完成后用标准两选项消息请求批准。

### Step 9: Build and Test (始终执行)

读取 `references/construction/build-and-test.md`，按步骤执行。

- 生成 `build-and-test/` 目录下的构建说明、测试说明文件
- **必须等待用户明确批准**

### Step 10: Operations (占位)

读取 `references/operations/operations.md`。当前为占位阶段，构建测试活动已在 CONSTRUCTION 完成。

---

## 文件结构约定

```
<WORKSPACE-ROOT>/           # ⚠️ 应用代码放这里
├── [项目特定结构]           # 按项目类型（见 code-generation.md）
│
├── aidlc-docs/            # 📄 文档放这里
│   ├── inception/
│   │   ├── plans/
│   │   ├── reverse-engineering/   # brownfield
│   │   ├── requirements/
│   │   ├── user-stories/
│   │   └── application-design/
│   ├── construction/
│   │   ├── plans/
│   │   ├── {unit-name}/
│   │   │   ├── functional-design/
│   │   │   ├── nfr-requirements/
│   │   │   ├── nfr-design/
│   │   │   ├── infrastructure-design/
│   │   │   └── code/             # markdown 摘要
│   │   └── build-and-test/
│   ├── operations/
│   ├── aidlc-state.md
│   └── audit.md
```

**关键规则**：
- 应用代码：工作区根目录（禁止放 `aidlc-docs/` 内）
- 文档：`aidlc-docs/` 内
- 审计日志：追加到 `audit.md`，禁止覆盖

---

## 会话恢复（Resume）

读取 `references/common/session-continuity.md`：
1. 检查 `aidlc-state.md`，获取当前状态
2. 加载所有已完成阶段的工件
3. 显示 "Welcome back" 提示，包含当前阶段 + 下一步
4. 用户选择继续或回顾

---

## Bug 修复场景

读取 `references/inception/requirements-analysis.md`（Minimal 深度）：

1. Workspace Detection
2. Requirements Analysis (Minimal) — 记录 bug 描述和复现路径
3. Workflow Planning — 通常跳过大部分阶段
4. Code Generation — 修复 + 测试
5. Build and Test

对于 bug 修复，User Stories、NFR、Application Design 通常都跳过。

---

## 详细规则参考

本 SKILL.md 提供了完整工作流概览。每个阶段的详细步骤、工件格式、问题模板和审批格式，请查阅对应参考文件：

| 阶段 | 参考文件 |
|------|---------|
| 欢迎消息 | `references/common/welcome-message.md` |
| 工作流概览 | `references/common/process-overview.md` |
| 会话恢复 | `references/common/session-continuity.md` |
| 问题格式 | `references/common/question-format-guide.md` |
| 内容验证 | `references/common/content-validation.md` |
| 深度自适应 | `references/common/depth-levels.md` |
| ASCII 图规范 | `references/common/ascii-diagram-standards.md` |
| 过度自信预防 | `references/common/overconfidence-prevention.md` |
| 错误处理 | `references/common/error-handling.md` |
| 变更管理 | `references/common/workflow-changes.md` |
| 术语表 | `references/common/terminology.md` |
| 工作区检测 | `references/inception/workspace-detection.md` |
| 需求分析 | `references/inception/requirements-analysis.md` |
| 用户故事 | `references/inception/user-stories.md` |
| 工作流规划 | `references/inception/workflow-planning.md` |
| 应用设计 | `references/inception/application-design.md` |
| 单元生成 | `references/inception/units-generation.md` |
| 逆向工程 | `references/inception/reverse-engineering.md` |
| 代码生成 | `references/construction/code-generation.md` |
| 构建测试 | `references/construction/build-and-test.md` |
| NFR 需求 | `references/construction/nfr-requirements.md` |
| NFR 设计 | `references/construction/nfr-design.md` |
| 功能设计 | `references/construction/functional-design.md` |
| 基础设施设计 | `references/construction/infrastructure-design.md` |
| 运营 | `references/operations/operations.md` |
| 安全基线(扩展) | `references/extensions/security/baseline/security-baseline.md` |
