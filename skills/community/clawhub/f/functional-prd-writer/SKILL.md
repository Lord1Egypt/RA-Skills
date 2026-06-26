---
name: "functional-prd-writer"
description: "Write concise, implementation-oriented functional PRDs with structured interview, quality checklist, and common pitfalls guide."
version: "1.1.0"
---

# Functional PRD Writer

Produce concise, implementation-oriented PRDs. Focus on **what the feature does** and **how it works**, so developers can start building immediately.

## Core Philosophy

Functional PRDs answer **what and how**. Every section should help a developer understand exactly what to build. Skip business strategy; focus on behavior, rules, data, and edge cases.

## 工作流程

### Step 1：需求澄清（必做）

在写 PRD 之前，先向用户确认以下关键信息（缺什么问什么）：

1. **功能名称** — 一句话说清楚做什么
2. **目标用户** — 谁用？管理员还是普通用户？
3. **核心场景** — 用户在什么情况下会用这个功能？
4. **技术约束** — 有没有限定技术栈、已有系统、接口？
5. **范围边界** — 这期做什么？明确不做什么？

> 💡 如果用户给的信息足够完整，直接进入 Step 2，不要反复确认。

### Step 2：规模判断

根据功能复杂度选择输出策略：

| 规模 | 特征 | 输出策略 |
|------|------|----------|
| **小型** | 单一页面/单个接口/无状态流转 | 精简版：概述 + 需求 + 接口 + 边界 |
| **中型** | 多页面/有状态/涉及权限 | 标准版：完整 8 节结构 |
| **大型** | 多模块/复杂流程/跨系统 | 详细版：完整结构 + 子模块拆分 + 数据流图 |

### Step 3：输出 PRD

按标准结构撰写（见下方），根据 Step 2 的规模判断决定详略。

### Step 4：自检

输出完成后，按以下清单自查：

- [ ] 每个功能点可独立转为测试用例
- [ ] 所有数值都有具体值（不是"适当"、"合理"）
- [ ] 状态流转画成了状态机
- [ ] 异常情况都有处理方案
- [ ] 权限控制明确（谁能看/谁能操作）
- [ ] 范围说明列出了"不做的内容"

## Standard Structure

### 1. 功能概述 (Feature Overview)
- 一句话描述这个功能是什么
- 要解决什么具体问题
- 适用范围（哪些用户/场景）

### 2. 功能需求 (Functional Requirements)
- 功能点列表（编号，每个功能点可独立测试）
- 每个功能点的输入/输出/行为描述
- 优先级标注（P0 必做 / P1 应做 / P2 可选）

### 3. 用户流程 (User Flows)
- 核心操作流程（步骤编号）
- 分支流程（异常/边界情况）
- 用文字流程图描述，格式：
  ```
  开始 → 步骤1 → 步骤2 → 分支判断 → ...
  ```

### 4. 交互与界面 (UI/UX Specs)
- 页面布局描述（哪些区域、什么内容）
- 表单字段说明（字段名、类型、校验规则、默认值）
- 操作反馈（成功/失败/加载中的提示方式）
- 特殊状态展示（空数据、加载中、错误、禁用等）

### 5. 数据与规则 (Data & Business Rules)
- 涉及的数据实体和字段
- 校验规则（格式、范围、必填等）
- 业务规则（条件判断、计算逻辑、状态流转）
- 权限控制（谁能看、谁能操作）

### 6. 接口设计 (API Design)
- 涉及的接口列表（路径、方法、用途）
- 请求参数和响应格式
- 错误码定义

### 7. 边界与异常 (Edge Cases & Error Handling)
- 输入异常如何处理
- 网络异常/超时如何处理
- 并发/竞态如何处理
- 数据不一致如何恢复

### 8. 非功能性需求 (Non-functional Requirements)
- 性能要求（响应时间、并发量）
- 安全要求（认证、加密、防护）
- 兼容性要求（浏览器、设备、系统版本）

## Writing Guidelines

- 用中文撰写，除非用户指定英文
- **简洁直接**：每个功能点一段话说清楚，不要铺陈背景
- **可测试**：每个需求描述都应该能直接转化为测试用例
- **给具体值**：不说"适当限制"，说"60秒内只能发送1次"
- **给具体格式**：不说"输入用户名"，说"输入用户名（3-20位字母数字，必填）"
- **画状态机**：有状态流转的必须画清楚（初始态→中间态→终态）
- 优先级标注：P0（必须有）/ P1（应该有）/ P2（锦上添花）
- 不写的明确说明：在"范围说明"中列出本期不做的内容

## 常见错误（避免）

| ❌ 错误写法 | ✅ 正确写法 |
|------------|------------|
| 用户输入合法的用户名 | 用户名：3-20位字母数字下划线，首字符非数字，必填 |
| 系统会适当限制频率 | 同一IP 60秒内最多发送3次，超限返回 429 |
| 支持多种导出格式 | 支持导出为 CSV（UTF-8 BOM）和 XLSX（.xlsx），默认 CSV |
| 异常时给出提示 | 网络超时：展示"请求超时，请重试"，提供"重试"按钮，自动重试1次 |
| 有权限控制 | Admin 角色可编辑/删除；普通用户仅查看；权限由 `role` 字段控制 |

## Reference Files

- **references/functional-prd-template.md** — 完整功能型 PRD 模板（Markdown）
- **references/common-patterns.md** — 常见功能模式参考（CRUD、表单、列表、状态机、权限等）

Read references when: user asks for a full template, or when the PRD involves common functional patterns.
