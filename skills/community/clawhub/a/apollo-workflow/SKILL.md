---
name: apollo-workflow
description: >
  把你的想法变成能用的代码：先想清楚，再一步一步做出来。每步有检查点，不完成不往下走。
version: 3.0.0
entry_point: true
marketplace_description: |
  Apollo人体操作系统的核心Pipeline——把你的想法变成能用的代码。
  
  **这不是独立的方法论，这是Apollo-os的执行引擎。**
  
  适用场景：开发新功能、修复Bug、写实现计划、任何需要系统化执行的编码任务。
  
  **核心流程（5步流水线）：**
  • Phase 1 Brainstorming：想清楚要做什么（苏格拉底式提问，把模糊想法变成设计文档）
  • Phase 2 Writing Plans：拆解成2-5分钟可完成的小任务
  • Phase 3 Subagent Development：并行Worker执行，TDD驱动
  • Phase 4 Systematic Debugging：根因调试，修完才能走
  • Phase 5 Finishing Branch：验证测试，用户选择交付方式
  
  **关键机制：**
  • HARD GATE门禁：每Phase之间有检查点，不完成不往下走
  • 状态机：自动记录当前Phase和进度，随时可恢复
  • 5层分工：研究员→规划师→执行Worker→验证→整合交付
  
  **Apollo-os组成部分：**
  感知层（dream/renal）、防御层（immu/autophagy）、响应层（neuro）、调控层（endo/circadian）、进化层（stem/epi）由workflow在执行过程中调用，不是独立步骤。
read_when:
  - User says: build / plan / develop / new feature / add something / coding task
  - User says: this is broken / debug / bug
  - User says: let's build / help me plan / I want to add X
  - Bug / test failure / unexpected behavior
  - Completing a feature branch
triggers:
  - build
  - plan
  - develop
  - new feature
  - add something
  - this is broken
  - debug
  - coding task
requires:
  bins:
    - git
  tools:
    - sessions_spawn
    - exec
---

# Apollo Workflow v3.0.0

## Apollo-os核心定位

**Apollo = 人体操作系统，workflow是它的执行引擎。**

人体器官在各Phase中被调用：
- Phase 1时 → apollo-dream整理上下文
- Phase 3执行时 → apollo-neuro选择路径，HARD GATE验证
- 遇到危险 → apollo-immu拦截
- 遇到bug → Phase 4四阶段内化在workflow里
- 需要清理 → apollo-autophagy
- 需要记忆 → apollo-renal

## 一句话流程

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
  想清楚    拆任务    并行做    调错误    收尾
```

---

## Phase 1: Brainstorming（想法澄清）

**目的：把模糊想法变成经批准的设计文档**

### 核心准则

在创造性工作之前，通过协作对话将想法转化为完整的设计和规格说明。

**硬性门槛：**
```
在调用任何实现技能，写任何代码、搭建任何项目、或采取任何实现动作之前，
必须先展示设计并获得主人批准。
无论感知到的复杂度如何，每个项目都要走这个流程。
```

### 流程检查表

按顺序完成：

1. **探索项目上下文** — 检查文件、文档、最近提交
2. **提出澄清问题** — 一次一个，理解目的/约束/成功标准
3. **提出 2-3 种方案** — 带有权衡和推荐
4. **展示设计** — 按复杂度缩放各部分，在每个部分后获批准
5. **写设计文档** — 保存到 `docs/plans/YYYY-MM-DD-<topic>-design.md`
6. **规格自审** — 快速内联检查占位符、矛盾、模糊、范围
7. **主人审查书面规格** — 在继续之前请主人审查规格文件

### 关键原则

- **一次一个问题** — 不要用多个问题压垮
- **多选优先** — 比开放问题更容易回答
- **YAGNI彻底** — 从所有设计中移除不必要功能
- **增量验证** — 展示设计，获得批准后再继续

### 输出

- `docs/plans/YYYY-MM-DD-<topic>-design.md`
- HG-1 gate文件：`p1-design-approved.json`

---

## Phase 2: Writing Plans（任务拆解）

**目的：把设计拆成2-5分钟可完成的小任务，TDD循环**

### 核心准则

写全面的实现计划，假设执行者对代码库零上下文。

**开始时宣布：** "我正在用 writing-plans 技能创建实现计划。"

### 文件结构

在定义任务之前，映射哪些文件将被创建或修改，每个文件负责什么。

- 用清晰边界和定义好接口的设计单元
- 偏好更小、专注的文件，不要大的什么都做的文件
- DRY。YAGNI。TDD。频繁commit。

### 小粒度任务

**每步是一个动作（2-5 分钟）：**
```
- "写失败的测试" — 一步
- "运行确保它失败" — 一步
- "写最少代码让测试通过" — 一步
- "运行确保测试通过" — 一步
- "Commit" — 一步
```

### 计划文档结构

```markdown
# [功能名] 实现计划

**目标：** [一句话描述构建内容]
**架构：** [2-3句话描述方法]
**技术栈：** [关键技术和库]

---

## 任务 1：[组件名]

**文件：**
- 创建：`exact/path/to/file.py`
- 修改：`exact/path/to/existing.py:123-145`

- [ ] **步骤 1：写失败的测试**
- [ ] **步骤 2：运行测试验证它失败**
- [ ] **步骤 3：写最少的实现代码**
- [ ] **步骤 4：运行测试验证它通过**
- [ ] **步骤 5：Commit**
```

### 无占位符

每步必须包含执行者需要的实际内容。以下是**计划失败**——永远不要写：
- "TBD"、"TODO"、"稍后实现"、"填细节"
- "添加适当的错误处理"/"添加验证"
- "类似于任务 N"

### 输出

- `docs/plans/YYYY-MM-DD-<feature>.md`
- HG-2 gate文件：`p2-plan-approved.json`

---

## Phase 3: Subagent Development（并行开发）

**目的：用test-driven development + 两级review驱动subagent完成任务**

### 两种模式

#### 模式A：子Agent并行（适合独立任务）

当多个任务完全独立时，按问题域分配给不同Agent并行处理。

#### 模式B：研究/综合分离（适合复杂研究任务）

多人并行研究，最后主Agent自己汇总——不把综合判断交给子Agent。

### 核心准则

**多人并行研究，最后一个人汇总。不要让子Agent去综合——那是Coordinator的工作。**

| 阶段 | 谁做 | 做什么 |
|------|------|--------|
| Research | Workers（并行） | 各自研究不同方向 |
| Synthesis | **Coordinator（自己）** | 读取结果，形成结论 |
| Implementation | Workers | 按结论执行 |
| Verification | Fresh Agent | 独立验证 |

### 关键规则

1. **研究阶段可以并行**
2. **综合阶段必须自己来**
3. **验证必须 fresh eyes**（新Agent来验证）
4. **失败优先 Continue**（修正失败 → 继续用同一个Agent）

### 输出

- 代码 + commit
- HG-3 gate文件：`p3-all-tasks-done.json`

---

## Phase 4: Systematic Debugging（根因调试）

**目的：修根因不修症状，四阶段铁律**

### 核心准则

**随机修 bug 浪费时间。快速补丁掩盖根本问题。**

**核心原则：永远先找根本原因再尝试修复。症状修复 = 失败。**

### 铁律

```
未经根本原因调查，不许修复
```

如果没完成第1阶段，就不能提出修复方案。

### 四阶段流程

#### 阶段 1：根本原因调查

1. **仔细阅读错误信息** — 不要跳过错误或警告
2. **稳定复现** — 能可靠地触发吗？具体步骤是什么？
3. **检查最近变更** — Git diff、最近提交
4. **追踪数据流** — 追踪到源头，在源头修复

#### 阶段 2：模式分析

1. **找类似工作的例子**
2. **对比参考** — 如果在实现某个模式，彻底读完参考实现
3. **识别差异**
4. **理解依赖**

#### 阶段 3：假设与测试

1. **形成一个假设** — "我认为 X 是根本原因"
2. **最小化测试** — 一次只改一个变量
3. **验证后再继续**
4. **当不知道时** — 说"我不理解 X"，不要假装知道

#### 阶段 4：实现

1. **创建失败的测试用例**
2. **实现单一修复** — 解决识别的根本原因，一次改一个
3. **验证修复**
4. **如果修复没用** — 停止，已经尝试了多少次？如果 < 3，回到阶段1

### 红旗

如果发现自己想：
- "先快速修复，以后再调查"
- "就试试改 X 看看行不行"
- "加多个变更，一起跑测试"
- **已经尝试了 2+ 次修复** — 停止，回到阶段1

**如果 3+ 修复都失败：** 质疑架构。与主人讨论。

### 输出

- bug修复 + commit
- HG-4 gate文件：`p4-bug-fixed.json`

---

## Phase 5: Finishing Branch（收尾）

**目的：验证测试 → 用户选择 → 执行决定**

### 流程

1. **运行完整测试套件**
2. **展示结果**
3. **用户选择交付方式：**
   - Merge到main
   - 创建PR
   - 保留分支
   - 丢弃分支

### 输出

- HG-5 gate文件：`p5-complete.json`

---

## HARD GATE机制

> 每个Phase之间必须通过硬性门禁（HARD GATE），不完成不往下走。

| Gate | 触发时机 | 检查文件 | 不通过则 |
|------|---------|---------|---------|
| HG-0 | workflow启动 | state.json创建 | 退出 |
| HG-1 | 进入Phase 2 | `p1-design-approved.json` | 报错退出 |
| HG-2 | 进入Phase 3 | `p2-plan-approved.json` | 报错退出 |
| HG-3 | 进入Phase 5 | `p3-all-tasks-done.json` | 报错退出 |
| HG-4 | Debug完成后 | `p4-bug-fixed.json` | 警告 |
| HG-5 | Finish执行前 | `p5-complete.json` | 报错退出 |

---

## 状态文件

```json
// .workflow/state.json
{
  "version": "3.0.0",
  "workflow_id": "uuid",
  "current_phase": "phase1|phase2|phase3|phase4|phase5",
  "topic": "用户请求概要",
  "design_file": "docs/plans/...-design.md",
  "plan_file": "docs/plans/...-feature.md",
  "completed_tasks": [1, 2, 3],
  "gates_passed": ["p1", "p2"]
}
```

---

## Phase跳跃规则

- 用户说"debug/bug" → 直接进 **Phase 4**
- 有已批准Design → 直接进 **Phase 2**
- 有已批准Plan + 用户选Subagent模式 → 直接进 **Phase 3**

---

## Apollo-os调用关系

workflow执行时感知人体器官：

| 时机 | 调用 | 作用 |
|------|------|------|
| Phase 1开始 | apollo-dream | 整理上下文，理解背景 |
| Phase 1澄清 | apollo-neuro | 判断问题复杂度，选择路径 |
| 遇到危险操作 | apollo-immu | 拦截危险命令 |
| Phase 3执行中 | HARD GATE验证 | 每步必须验证才能继续 |
| 遇到bug | Phase 4四阶段 | 内化在workflow里，不独立调用 |
| 需要清理 | apollo-autophagy | 清理无用代码 |
| 需要记忆 | apollo-renal | 过滤噪音上下文 |
| 任务完成 | apollo-dream | 整理本次经验 |

---

## 快速开始

```bash
# 启动workflow
bash scripts/workflow/workflow-launch.sh "我想加一个缓存功能"

# 检查状态
bash scripts/workflow/state-manager.sh check

# 手动推进phase
bash scripts/workflow/state-manager.sh advance phase2

# 检查门禁
bash scripts/workflow/phase-gate-check.sh phase2
```
