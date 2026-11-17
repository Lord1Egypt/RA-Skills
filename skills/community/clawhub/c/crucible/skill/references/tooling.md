# Crucible 工具链指南

> 推荐辅助工具，增强管线效果。非必需依赖 — Crucible 无它们也能运行。

---

## 1. Codegraph — 结构化代码智能

SQLite 知识图谱，一次调用返回源码 + 调用路径 + 影响范围。

### 安装
```bash
codegraph init   # 在目标项目根目录运行一次
```

### 各阶段使用

| 阶段 | 用途 | 查询示例 |
|------|------|---------|
| PM | 探索现有架构 | `"request router to database flow"` |
| Dev | 修改前 impact analysis | `"functionName callers"` |
| Gate 3 | Blast-radius 分析 | `"changedFunction impact"` |

### 与 Ponytail Ladder 的关系

Ladder 第 2 级 "代码库里已经有了吗？" → Codegraph 一次查询发现已有 helper/pattern。

### 优先级
```
codegraph_explore → 结构查询（最快最准）
fast_context_search → 语义模糊搜索
grep → 精确文本匹配
```

---

## 2. OpenSpec CLI — 规格驱动开发

多模型协作消除歧义，产出约束集和零决策计划。

### 安装
```bash
npm install -g @fission-ai/openspec && openspec init
```

### 与 Crucible 组合

| OpenSpec | Crucible | 组合 |
|----------|----------|------|
| spec-research | Stage 1 (PM) | 约束集替代传统 PRD |
| spec-plan | Stage 1→2 | 零决策计划 |
| spec-impl | Stage 3 (Dev) | 按 spec 机械执行 |
| spec-review | Gate 3 | 双模型交叉验证 |

### 何时用

| 场景 | 推荐 |
|------|------|
| 快速原型/MVP | 纯 Crucible |
| 复杂业务逻辑、多模型验证 | Crucible + OpenSpec |
| 团队协作、specs 作为文档 | Crucible + OpenSpec |

---

## 3. 检测与自动启用

管线启动时检测可用工具，有则注入对应指令，无则用内置蒸馏方法论。
