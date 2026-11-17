---
name: code-visual-review
version: 2.0.0
description: "Generate visual HTML pages for code review (diff + risk tags), code walkthrough (call chains + trust boundaries), and architecture analysis (module dependencies + tech debt). Three modes with shared dark-theme template."
tags: [review, visual, file-based, template-based, diff, walkthrough, trust-boundary, architecture]
---

# Code Visual Review v2.0.0

生成可视化的 HTML 代码审查页面，支持三种模式：

| 模式 | 场景 | 输出内容 |
|------|------|----------|
| **Review 模式** | PR 审查、diff 分析 | 风险地图 + 逐文件 diff + Before/After 对比 |
| **Walkthrough 模式** | 代码理解、架构审查 | Request Path 图 + Call Stack 步骤 + Trust Boundary |
| **Architecture 模式** | 代码库架构分析 | 模块依赖图 + 健康度评分 + 技术债务清单 + Before/After 架构对比 |

三种模式共享同一套暗色主题 HTML 模板，可在同一页面中混合使用。

> v2.0.0 新增：Architecture 模式（合并自 architecture-review v1.0.0）

---

## 何时使用

### Review 模式
- 代码审查（Code Review）时，需要比纯文本 diff 更直观的审查报告
- 需要向团队解释一个 PR 的变更范围和风险等级
- 需要生成带逐文件 diff + 风险标注 + 修改动机的 PR 描述

### Walkthrough 模式
- 需要解释某个模块的调用链路和数据流
- 新人 onboarding 时理解代码结构
- 代码审查中解释复杂逻辑
- 标记安全边界和外部依赖

---

## Review 模式：PR 审查

### 核心能力

1. **PR 审查摘要页**
   - PR 标题 + 动机 + TL;DR
   - **风险热力图**：safe / worth a look / needs attention 三级标签
   - 逐文件 diff，带语法高亮和风险标注
   - Before/After 行为对比

2. **PR 描述生成**
   - 动机（Why）：解决了什么问题
   - 逐文件 Walkthrough：按阅读顺序排列，标注 why
   - Before/After 行为对比
   - 审查重点提示

### 使用指南

#### 场景 1：PR 审查摘要

用户提供 PR diff 或 git 输出，生成包含以下结构的 HTML：
1. **PR 标题 + 描述** — TL;DR 一句话总结
2. **风险地图** — 按文件列出风险等级
3. **逐文件 diff** — 带语法高亮的 diff，标注风险标签
4. **审查建议** — 告诉审查者应该重点关注哪些

#### 场景 2：PR 描述生成

用户提供分支名和变更文件列表，生成：
1. **Why** — 变更动机，Before/After 对比
2. **File-by-file** — 按阅读顺序排列的文件说明
3. **Where to focus** — 审查者应关注的文件

### Review 模式 HTML 结构

```html
<!-- 风险标签 -->
<span class="risk risk-safe">🟢 safe</span>
<span class="risk risk-worth">🟡 worth a look</span>
<span class="risk risk-attention">🔴 needs attention</span>

<!-- 风险地图 -->
<div class="risk-map">
  <div class="risk-map-item">src/auth.ts — 🟡 worth a look</div>
  <div class="risk-map-item">src/utils.ts — 🟢 safe</div>
</div>

<!-- Diff 块 -->
<div class="file-block">
  <div class="file-header">
    <span class="file-path">src/auth.ts</span>
    <span class="file-stats">+12 -3</span>
  </div>
  <div class="diff-line diff-add">+ new code here</div>
  <div class="diff-line diff-del">- old code here</div>
  <div class="diff-line diff-ctx">  context line</div>
</div>

<!-- Before/After 对比 -->
<div class="comparison">
  <div class="comparison-col before">
    <h4>Before</h4>
    <ul>
      <li>行为描述 1</li>
      <li>行为描述 2</li>
    </ul>
  </div>
  <div class="comparison-col after">
    <h4>After</h4>
    <ul>
      <li>新行为 1</li>
      <li>新行为 2</li>
    </ul>
  </div>
</div>
```

---

## Walkthrough 模式：代码理解

### 核心能力

1. **调用链路追踪**
   - 从入口到出口的完整数据流
   - 模块间依赖关系图（boxes & arrows）
   - 每个步骤标注文件路径和行号

2. **代码标注**
   - 关键逻辑逐步 Walkthrough
   - 可展开/折叠的源码块
   - 每个步骤的解释说明

3. **信任边界标注**
   - 标注安全边界（哪些是可信的，哪些不可信）
   - 外部依赖标注
   - 数据验证点标注

### 使用指南

#### 步骤 1：识别入口点

从用户可触达的入口开始（API endpoint、CLI 命令、Webhook 等）。

#### 步骤 2：追踪调用链

沿数据流追踪到最终输出（数据库写入、响应返回、外部调用等）。
记录每一步：
- 文件路径和行号
- 函数名
- 关键逻辑说明

#### 步骤 3：标注信任边界

标记：
- **可信区域**：经过验证的数据、内部服务
- **不可信区域**：用户输入、外部 API、第三方服务
- **验证点**：数据校验、权限检查的位置

#### 步骤 4：生成 HTML

将以上信息组织成自包含的 HTML 页面，包含：
1. **Request Path** — 可视化数据流
2. **Call Stack Walkthrough** — 逐步骤代码注解
3. **Trust Boundary** — 安全边界标注

### Walkthrough 模式 HTML 结构

```html
<!-- 请求路径图 -->
<div class="request-path">
  <div class="path-node untrusted">[Browser]</div>
  <span class="path-arrow">→</span>
  <div class="path-node untrusted">[LB]</div>
  <span class="path-arrow">→</span>
  <div class="path-node">[API /api/session]</div>
  <span class="path-arrow">→</span>
  <div class="path-node trust">[verifyToken]</div>
  <span class="path-arrow">→</span>
  <div class="path-node trust">[SessionStore]</div>
</div>

<!-- 调用步骤 -->
<div class="step">
  <span class="step-num">1</span>
  <span class="step-title">src/app/providers/AuthProvider.tsx:22-48</span>
  <div class="step-file">On mount, the React provider issues GET /api/session...</div>
  <details>
    <summary>show source</summary>
    <pre><code>// source code here</code></pre>
  </details>
</div>

<!-- 信任边界 -->
<div class="trust-boundary">
  <strong>⚠️ Trust Boundary</strong>
  <p>Everything below verifyToken is trusted. Everything above it is not.</p>
</div>

<!-- 注解 -->
<div class="annotation">
  This is where the JWT token is validated against the secret.
</div>
```

---

## Architecture 模式：代码库架构分析（v2.0.0 新增）

> 合并自 architecture-review v1.0.0。将代码库架构分析结果以 HTML 可视化报告呈现。

### 执行流程

#### Phase 1: 代码库扫描
收集代码库的结构信息：
1. **目录结构** — 顶层目录和关键子目录
2. **模块划分** — 识别主要模块/包/命名空间
3. **依赖关系** — 模块间的导入/导出关系
4. **技术栈** — 语言、框架、关键依赖库
5. **代码指标** — 文件数量、代码行数（大致估算）

#### Phase 2: 架构分析

基于扫描数据，分析以下维度：

| 维度 | 检查要点 |
|------|----------|
| **模块化程度** | 模块边界是否清晰、是否存在循环依赖、耦合度评估 |
| **分层合理性** | 是否遵循分层架构、是否存在跨层调用、依赖方向是否正确 |
| **技术债务** | 大文件/复杂文件识别、重复代码模式、过时依赖/废弃 API |
| **可维护性** | 命名一致性、错误处理模式、测试覆盖情况 |

#### Phase 3: 生成 HTML 报告

```
1. 报告头部 — 项目名称、分析日期、分析范围
2. 执行摘要 — 整体健康度评分（1-10）+ 3-5个关键发现 + 最高优先级建议
3. 架构视图（Mermaid图表）— 模块依赖图 + 分层架构图 + 数据流图
4. 核心发现（卡片网格）— 每个发现一张卡片，标注强度徽章（Strong / Worth exploring / Speculative）
5. 技术债务清单 — 按严重程度排序，估算修复工作量，优先级建议
6. Before/After 对比 — 当前架构 vs 建议架构，关键改进点可视化
7. 推荐行动 — 按优先级排序，标注强度徽章，预估工作量
```

### Architecture 模式 HTML 结构

```html
<!-- 健康度评分 -->
<div class="health-score">
  <span class="score-value">7.2</span>
  <span class="score-label">/10</span>
</div>

<!-- 模块依赖图（Mermaid） -->
<div class="architecture-diagram">
  <pre class="mermaid">
graph TD
    classDef good fill:#d4edda,stroke:#28a745
    classDef warn fill:#fff3cd,stroke:#ffc107
    classDef bad fill:#f8d7da,stroke:#dc3545
    
    UI[UI Layer]:::good --> Service[Service Layer]:::good
    Service --> Repository[Repository Layer]:::warn
    Repository --> Database[(Database)]:::good
    Service --> ExternalAPI[External API]:::bad
  </pre>
</div>

<!-- 核心发现卡片 -->
<div class="finding-card">
  <span class="badge badge-strong">Strong</span>
  <h4>循环依赖检测</h4>
  <p>Module A 和 Module B 存在双向依赖，建议引入接口层解耦</p>
  <span class="impact">影响范围: 3 个文件</span>
</div>

<!-- 技术债务清单 -->
<div class="debt-list">
  <div class="debt-item debt-critical">
    <span class="severity">Critical</span>
    <span class="description">过时依赖: lodash 4.17.15 (已知安全漏洞)</span>
    <span class="effort">修复工作量: 0.5h</span>
  </div>
</div>

<!-- Before/After 架构对比 -->
<div class="comparison">
  <div class="comparison-col before">
    <h4>当前架构</h4>
    <ul>
      <li>扁平模块结构，无分层</li>
      <li>直接数据库访问</li>
    </ul>
  </div>
  <div class="comparison-col after">
    <h4>建议架构</h4>
    <ul>
      <li>引入 Service 层</li>
      <li>Repository 模式隔离数据访问</li>
    </ul>
  </div>
</div>
```

### 适用场景

| 场景 | 报告重点 |
|------|----------|
| **架构评审** | 模块依赖图 + 分层分析 + 改进建议 |
| **技术债务评估** | 债务清单 + 优先级 + 修复工作量 |
| **项目健康度** | 健康度评分 + 关键指标 + 趋势 |
| **重构方案** | 现状分析 + 目标架构 + 迁移路径 |
| **新成员入职** | 架构概览 + 模块说明 + 关键流程 |

### Architecture 模式降级策略

| 场景 | 降级方案 |
|------|----------|
| 无法识别模块边界 | 使用目录结构作为模块划分，标注"基于目录推断" |
| 依赖关系无法解析 | 使用 import 语句推断，标注"部分依赖可能遗漏" |
| 代码量过大（>10000行） | 只分析顶层模块，标注"深层模块未分析" |
| Mermaid 渲染失败 | 退回到文本形式的依赖列表 |

---

## 组合模式

当审查同时需要多种视角时，可在同一页面中混合多种内容：

```html
<!-- 先展示 diff 审查 -->
<section>
  <h2>Code Changes</h2>
  <!-- Review 模式 diff 内容 -->
</section>

<!-- 再展示调用链理解 -->
<section>
  <h2>Call Chain Impact</h2>
  <!-- Walkthrough 模式内容 -->
</section>

<!-- 最后展示架构影响 -->
<section>
  <h2>Architecture Impact</h2>
  <!-- Architecture 模式内容 -->
</section>
```

---

## HTML 模板基础

所有输出使用统一的暗色主题模板，详见 `templates/base.html`。

**核心特性：**
- 单文件，无外部依赖（所有 CSS/JS 内联）
- 响应式布局，手机可读
- GitHub 风格 diff 配色（绿=新增，红=删除）
- 风险标签用颜色区分：🟢 safe / 🟡 worth a look / 🔴 needs attention
- 可折叠代码块（details/summary）
- 信任边界虚线框

**CSS 变量：**
```css
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --text-muted: #8b949e;
  --accent: #58a6ff;
  --green: #2ea043;
  --red: #da3633;
  --yellow: #d29922;
  --diff-add-bg: rgba(46,160,67,0.15);
  --diff-del-bg: rgba(218,54,51,0.15);
}
```

---

## 与 coding-framework 集成

### 数据流

```
coding-framework 模式2（代理审查）
  → 输出审查结果（JSON/Markdown）
  → code-visual-review（Review 模式）
  → 生成可视化 HTML
用户浏览器 / canvas 呈现
```

### 调度入口

- **Review 模式**：coding-framework 模式2（代理审查）输出可输入本技能生成可视化页面
- **Walkthrough 模式**：coding-framework 模式2 中的 architecture-critic 代理可调用本技能生成架构审查的可视化辅助
- **安全守卫**：Walkthrough 中标注的信任边界可供 coding-framework 模式4（安全守卫）参考

### 输入格式

接受以下输入：
1. `git diff` 输出
2. 代理审查的 JSON 结果
3. 手动提供的文件列表 + 变更说明
4. 入口文件路径 + 函数名（Walkthrough 模式）

---

## 错误处理与降级策略

### Review 模式

| 场景 | 降级方案 |
|------|----------|
| 无 diff 输入 | 提示用户提供 git diff 输出或 PR 链接 |
| diff 格式无法解析 | 退回到纯文本展示，标注"无法解析 diff 格式" |
| 文件数量过多（>20） | 只显示高风险文件 diff，其余折叠为摘要 |
| diff 过长（单文件 >500 行） | 只显示变更块（hunks），省略上下文 |

### Walkthrough 模式

| 场景 | 降级方案 |
|------|----------|
| 无法识别入口点 | 提示用户指定入口文件或函数名 |
| 调用链跨多个模块 | 只追踪主路径，标注"外部调用"供用户深入 |
| 代码量过大（>1000行） | 分段生成 walkthrough，每段聚焦一个子模块 |
| 无法读取源文件 | 标注"文件不可读"，使用函数签名推断逻辑 |
| 信任边界无法确定 | 标注"需人工确认"，使用虚线问号标注 |

### 渲染问题

| 场景 | 降级方案 |
|------|----------|
| canvas 工具不可用 | 将 HTML 写入文件，提示用户在浏览器打开 |
| HTML 文件过大 | 分段生成，每段一个文件 |
| 代码块过长 | 折叠显示，默认隐藏源码，点击展开 |
| 语法高亮失败 | 退回到纯文本 pre 标签 |

---

## 注意事项

- 所有 CSS 和 JS 必须内联，不引用外部资源
- diff 颜色使用 GitHub 暗色主题配色
- 风险标签只用三种：🟢 safe / 🟡 worth a look / 🔴 needs attention
- 移动端必须可读（响应式网格）
- 如果 diff 太长，只显示关键变更行（上下文行省略）

---

## 文件结构

```
code-visual-review/
├── SKILL.md                    # 本文档
└── templates/
    └── base.html               # 共享 HTML 模板（暗色主题 + 响应式）
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0.0 | 2026-08-01 | 新增 Architecture 模式（合并自 architecture-review v1.0.0） |
| v1.0.0 | 2026-07-31 | 合并 code-review-visualizer + code-walkthrough |

---

*Version 2.0.0 — 合并 architecture-review，三模式输出（Review + Walkthrough + Architecture）*
