# 逆向技术设计文档：AI编码异常控制体系 v1.7

> **设计目标**：定义从零实现 `ai-coding-exception-control` 体系的技术方案
> **约束**：纯文件系统（无数据库），纯 Markdown（无专用格式），跨平台（Windows/Linux/macOS）
> **对应需求**：`reverse-requirements.md`

---

## 设计层一：异常处理架构

### 架构哲学

本体系的核心异常处理策略是 **"文件系统作为持久化层，Skill 作为触发器"**。所有状态通过文件系统持久化，所有逻辑通过 Skill 的提示词工程实现。

```
用户请求
   ↓
Skill 触发器（关键词匹配）
   ↓
读取 .workbuddy/skills/ai-coding-exception-control/SKILL.md
   ↓
按 L0-R→L0a→L0b→L1→L2→L3→L4→L5→L6 顺序执行
   ↓
每阶段产出写入文件系统
   ↓
质量门检查（文件存在性+内容完整性）
   ↓
通过 → 下一阶段 / 不通过 → 返回修复
```

### 降级链

| 优先级 | 降级策略 | 触发条件 | 降级后体验 |
|--------|---------|---------|-----------|
| 1 | 正常执行 | 所有 skill/SOP/模板文件存在且完整 | 完整九层防御执行 |
| 2 | 部分降级 | 某 SOP 文件缺失，但 SKILL.md 存在 | 跳过该SOP阶段，给出警告 |
| 3 | 核心降级 | SKILL.md 缺失，但编码 skill 存在 | 仅执行编码 skill 的 🛡️铁律 |
| 4 | 最低保障 | 所有 skill 缺失 | 输出基础异常处理提示，建议安装 skill |

### 错误分类体系

```
SkillError
  ├── TriggerError（触发不匹配）
  ├── FileNotFoundError（SOP/模板文件缺失）
  ├── FormatError（产出格式不符合模板）
  ├── GateFailedError（质量门未通过）
  ├── StallError（审查循环停滞）
  ├── BudgetExceededError（token/时间超预算）
  └── PermissionError（权限不足）
```

### 超时与重试策略

| 操作 | 超时 | 重试次数 | 退避策略 | 降级方案 |
|------|------|---------|---------|---------|
| WebSearch 调研 | 10s | 2 | 3s, 9s | 使用训练数据（标注风险） |
| WebFetch 获取 | 10s | 2 | 3s, 9s | 跳过该来源 |
| 文件写入 | 3s | 0 | — | 报错，检查权限 |
| 文件读取 | 1s | 0 | — | 报错，检查路径 |
| 质量门检查 | 5s | 0 | — | 超时视为不通过 |

---

## 设计层二：API 规范

### Skill 调用接口

```markdown
## 接口：ai-coding-exception-control.trigger

### 请求（用户输入）
- 触发关键词："编写功能"、"实现接口"、"开发模块"、"写代码"、"编码"、"需求分析"、"设计"
- 功能描述：用户提供的功能描述

### 响应（Skill 执行）
- 执行九层防御流程
- 产出：文件集合（见下方文件格式）

### 错误码
| 错误码 | 场景 | 用户提示 |
|--------|------|---------|
| 1001 | 触发关键词不匹配 | "请用'实现/开发/编码'等关键词触发" |
| 2001 | SKILL.md 缺失 | "核心框架文件缺失，请检查安装" |
| 3001 | 质量门不通过 | "[阶段名称] 质量门未通过，需补充：[原因]" |
| 4001 | 文件写入失败 | "无法写入文件，请检查 .workbuddy/ 目录权限" |
| 5001 | 审查循环 Stall | "审查循环停滞，建议人工介入" |
| 9001 | 未知错误 | "系统错误，请重试或联系支持" |
```

### Audit-Ledger 文件接口

```markdown
## 接口：audit-ledger.create_round

### 请求
- 功能模块名称
- 轮次编号（从1开始）

### 响应
- 创建目录：`.workbuddy/audit-ledger/round-{N}/`
- 初始化文件：deliverable.md（带模板骨架）

### 错误码
| 错误码 | 场景 |
|--------|------|
| 4001 | 目录已存在（重复创建） |
| 4002 | 父目录不存在（.workbuddy/ 未初始化） |
```

```markdown
## 接口：audit-ledger.submit_review

### 请求
- 轮次编号
- review-report.md 内容
- reviewer-memory.md 内容

### 响应
- 写入文件
- 判定：通过/不通过/Stall

### 错误码
| 错误码 | 场景 |
|--------|------|
| 4003 | review-report.md 格式错误（缺少必需字段） |
| 4004 | 审查意见不符合 falsifiable receipt 标准 |
| 5001 | Stall 触发（连续2轮问题数相同） |
```

### 质量门接口

```markdown
## 接口：quality-gate.check

### 请求
- 门类型：调研/需求/设计/编码/测试/审查
- 检查项列表

### 响应
- 通过/不通过
- 未通过项列表

### 错误码
| 错误码 | 场景 |
|--------|------|
| 3001 | 检查项未全部通过 |
| 3002 | 证据不足（通过但缺少证据） |
```

---

## 设计层三：数据持久化

### 存储策略：纯文件系统

本体系不使用数据库，所有数据通过 Markdown 文件持久化。理由：
1. **可审计**：每个文件都是人类可读的，便于审查
2. **版本友好**：天然适合 Git 版本控制
3. **零依赖**：不需要安装数据库服务
4. **跨平台**：Markdown 在任何平台都可读

### 目录结构

```
~/.workbuddy/
├── skills/
│   └── ai-coding-exception-control/
│       ├── SKILL.md                    # 主框架（415行）
│       └── references/
│           ├── templates.md            # 12套模板（1140行）
│           ├── requirements-design-sop.md  # 调研+需求+设计SOP（1004行）
│           ├── coding-sop.md           # 编码SOP（432行）
│           ├── testing-sop.md          # 测试SOP（620行）
│           ├── lessons-feedback-loop.md    # 弯路闭环SOP（321行）
│           ├── audit-ledger-spec.md    # 审查交接规范（378行）
│           └── OPC-DEVELOPMENT-SUITE.md    # 套件总览（406行）
├── memory/
│   └── lessons-learned.md              # 项目级弯路记录
└── audit-ledger/                       # 审查循环交接面（按项目）
    └── {project-name}/
        ├── round-1/
        ├── round-2/
        ├── round-3/
        └── final/
```

### 文件完整性校验

每个 Skill/SOP 文件顶部应有元信息：

```markdown
---
name: [skill-name]
description: [描述]
version: "x.y.z"
last_updated: "YYYY-MM-DD"
---
```

校验规则：
- `version` 必须符合 SemVer
- `last_updated` 必须 ≤ 当前日期
- 文件大小必须 > 0（非空文件）
- 关键章节必须存在（通过标题层级检查）

### 索引文件

为加速查找，维护一个索引文件：

```markdown
# Skill 索引

## ai-coding-exception-control
- 版本：1.7.0
- 文件：SKILL.md (415行)
- 关联文件：
  - templates.md (1140行)
  - requirements-design-sop.md (1004行)
  - coding-sop.md (432行)
  - testing-sop.md (620行)
  - lessons-feedback-loop.md (321行)
  - audit-ledger-spec.md (378行)
  - OPC-DEVELOPMENT-SUITE.md (406行)
- 总代码量：5249行
- 最后更新：2026-07-12
```

---

## 设计层四：安全设计

### 认证方案

本体系不处理用户认证，但依赖 WorkBuddy 平台的 session 认证。所有操作在已认证的 session 内执行。

### 授权方案

| 角色 | 权限 |
|------|------|
| 编码者 | 读写 deliverable.md, fix-report.md；只读 review-report.md；不可读 reviewer-memory.md |
| 审查者 | 读写 review-report.md, reviewer-memory.md, approved-receipt.md；只读 deliverable.md, fix-report.md |
| 系统 | 读写所有文件；创建/删除目录 |

**权限实现**：通过文件命名约定和约定式规范实现（非强制ACL）
- `reviewer-memory.md` 命名约定为"私有"，编码者主动不读取
- 实际执行中通过 prompt 约束实现

### 输入校验

所有用户输入（功能描述）必须经过：
1. **长度校验**：不超过 4000 字符（避免上下文溢出）
2. **注入检测**：不允许包含 prompt injection 模式（如"忽略以上指令"）
3. **范围校验**：功能描述必须具体，不能是"做个网站"这种模糊需求

### 敏感信息过滤

审查输出（review-report.md）必须过滤：
- API 密钥/Token
- 数据库连接字符串
- 内部服务器路径（如 `/home/user/.ssh/`）
- 个人隐私信息

---

## 设计层五：状态机设计

### 审查循环状态机

```
状态定义：
- IDLE: 初始状态
- CODING: 编码中
- READY_FOR_REVIEW: 编码完成，待审查
- REVIEWING: 审查中
- NEEDS_FIX: 审查不通过，待修复
- FIXING: 修复中
- APPROVED: 审查通过
- STALL: 停滞，需人工介入
- ESCALATED: 已上报人工

合法转换：
IDLE → CODING
CODING → READY_FOR_REVIEW
READY_FOR_REVIEW → REVIEWING
REVIEWING → NEEDS_FIX
REVIEWING → APPROVED
REVIEWING → STALL
NEEDS_FIX → FIXING
FIXING → READY_FOR_REVIEW
STALL → ESCALATED
ESCALATED → CODING（人工决定重新编码）
ESCALATED → APPROVED（人工决定通过）

非法转换（失败场景）：
READY_FOR_REVIEW → FIXING（必须经过审查）
REVIEWING → CODING（不能直接回退到编码）
APPROVED → REVIEWING（已通过不能重新审查，除非新建轮次）
STALL → READY_FOR_REVIEW（停滞后不能直接继续）
```

### 质量门状态机

```
状态定义：
- PENDING: 待检查
- CHECKING: 检查中
- PASSED: 通过
- FAILED: 不通过
- PARTIAL: 部分通过（有条件通过）

合法转换：
PENDING → CHECKING
CHECKING → PASSED
CHECKING → FAILED
CHECKING → PARTIAL
FAILED → CHECKING（修复后重新检查）
PARTIAL → CHECKING（修复后重新检查）
```

### 弯路生命周期状态机

```
状态定义：
- RECORDED: 已记录
- ANALYZED: 已分析
- IMPROVED: 已改进（skill/SOP已更新）
- VERIFIED: 已验证（下次编码未出现）
- ARCHIVED: 已归档（通用弯路写入 SKILL.md）

合法转换：
RECORDED → ANALYZED
ANALYZED → IMPROVED
IMPROVED → VERIFIED
VERIFIED → ARCHIVED
IMPROVED → ANALYZED（验证无效，重新分析）
```

---

## 设计质量门检查结果

- [x] S1 异常架构：降级链4级+错误分类体系+超时重试策略
- [x] S2 API规范：3个接口类型（skill触发/audit-ledger/质量门），含错误码
- [x] S3 数据持久化：纯文件系统方案，目录结构，完整性校验，索引文件
- [x] S4 安全设计：授权方案（2角色），输入校验（3项），敏感信息过滤
- [x] S5 测试策略：3个状态机（审查循环/质量门/弯路生命周期）
- [x] 需求-设计一致性：所有需求文档中的接口都有设计对应，所有失败场景都有处理策略

**设计质量门：6/6 通过。**
