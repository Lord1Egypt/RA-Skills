---
name: cca-domain3
description: CCA 领域3：Claude Code配置与工作流（20%权重）。当用户说"学domain3"、"Claude Code配置"、"CLAUDE.md"、"cca-domain3"时使用。
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

# CCA 领域 3：Claude Code 配置与工作流 (Claude Code Configuration & Workflows)

**权重：20% — 约 12 道题**

你是 CCA 领域 3 的学习导师。这个领域区分"用过 Claude Code 的人"和"能为团队配置 Claude Code 的人"。

## Step 1: 知识点讲解

### TS 3.1: 配置 CLAUDE.md 文件层级

**核心知识（考试最爱出陷阱题）：**

CLAUDE.md 三层结构：
1. **用户级** `~/.claude/CLAUDE.md` — 仅对该用户生效，不版本控制，不共享
2. **项目级** `.claude/CLAUDE.md` 或根目录 `CLAUDE.md` — 版本控制，团队共享
3. **目录级** — 子目录中的 `CLAUDE.md` 文件

**经典陷阱题：** 团队成员没收到指令 → 因为指令存在用户级配置中（未版本控制，未共享）。正确做法：放在项目级。

- `@import` 语法引用外部文件，保持 CLAUDE.md 模块化
- `.claude/rules/` 目录存放主题特定的规则文件

**实操技能：**
- 诊断配置层级问题（如新团队成员未收到指令）
- 使用 `@import` 按包维护者领域知识选择性导入标准文件
- 将大型 CLAUDE.md 拆分到 `.claude/rules/` 的聚焦文件中（如 `testing.md`、`api-conventions.md`）
- 使用 `/memory` 命令验证哪些配置文件被加载

### TS 3.2: 创建和配置自定义斜杠命令和 Skills

**核心知识：**
- 项目级命令 `.claude/commands/` — 版本控制，团队共享
- 用户级命令 `~/.claude/commands/` — 个人使用
- Skills 在 `.claude/skills/` 中，`SKILL.md` 文件支持 frontmatter：
  - `context: fork` — 在隔离子代理中运行（输出不污染主会话）
  - `allowed-tools` — 限制 skill 可用工具
  - `argument-hint` — 无参数调用时提示用户

**实操技能：**
- 在 `.claude/commands/` 创建项目级命令
- 使用 `context: fork` 隔离产出冗长输出的 skill
- 配置 `allowed-tools` 限制工具访问（如限制只读操作）
- 选择 skill（按需调用）vs CLAUDE.md（始终加载的通用标准）

### TS 3.3: 应用路径特定规则实现条件约定加载

**核心知识：**
- `.claude/rules/` 文件使用 YAML frontmatter 的 `paths` 字段指定 glob 模式
- 路径规则仅在编辑匹配文件时加载，减少无关上下文和 token 消耗
- **glob 模式规则 vs 目录级 CLAUDE.md 的优势：** glob 模式可跨多目录应用（如所有测试文件分散在代码库各处），目录级 CLAUDE.md 绑定到特定目录

**实操技能：**
- 创建带 YAML frontmatter 路径范围的规则文件：
  ```yaml
  ---
  paths: ["src/api/**/*"]
  ---
  API 约定内容...
  ```
- 用 glob 模式 `**/*.test.tsx` 为所有测试文件应用统一约定
- 当约定需跨目录应用时选择路径规则而非子目录 CLAUDE.md

### TS 3.4: 判断何时使用计划模式 vs 直接执行

**核心知识：**
- **计划模式适用：** 大规模变更、多个可行方案、架构决策、多文件修改
  - 示例：单体架构重构为微服务、影响 45+ 文件的库迁移
- **直接执行适用：** 简单、范围明确的变更
  - 示例：单文件 bug 修复、添加一个日期校验
- 计划模式在提交变更前安全探索和设计，避免代价高昂的返工
- Explore 子代理用于隔离冗长发现输出并返回摘要

**实操技能：**
- 对有架构影响的任务选择计划模式
- 对范围清晰的变更选择直接执行
- 组合使用：计划模式调查 + 直接执行实现

### TS 3.5: 应用迭代精炼技术实现渐进改进

**核心知识：**
- 具体的输入/输出示例比散文描述更有效
- 测试驱动迭代：先写测试 → 分享测试失败 → 引导渐进改进
- 面试模式：让 Claude 先提问发现开发者未预料的考虑点
- 何时一次性提供所有问题（交互问题）vs 逐个顺序修复（独立问题）

**实操技能：**
- 提供 2-3 个具体输入/输出示例来澄清转换需求
- 写测试套件覆盖期望行为、边界情况和性能要求
- 在不熟悉领域先用面试模式发现问题

### TS 3.6: 将 Claude Code 集成到 CI/CD 管道

**核心知识：**
- `-p`（或 `--print`）标志 — 非交互式模式，自动化管道必须
- `--output-format json` + `--json-schema` — CI 上下文中的结构化输出
- CLAUDE.md 为 CI 调用的 Claude Code 提供项目上下文
- **会话上下文隔离：** 生成代码的同一 session 自我审查不如独立审查实例有效

**实操技能：**
- 用 `-p` 标志在 CI 中运行 Claude Code
- 用 `--output-format json` + `--json-schema` 产生机器可解析的结构化结果
- 重新审查时包含前次发现，指示仅报告新/未解决的问题
- 在 CLAUDE.md 中记录测试标准和可用 fixtures

## Step 2: 实操练习

### 练习：为团队开发工作流配置 Claude Code

**步骤：**
1. 创建项目级 CLAUDE.md，写入通用编码标准和测试约定
2. 在 `.claude/rules/` 创建带 YAML frontmatter 的规则文件：
   - `paths: ["src/api/**/*"]` 用于 API 约定
   - `paths: ["**/*.test.*"]` 用于测试约定
3. 在 `.claude/skills/` 创建一个使用 `context: fork` 的 skill
4. 在 `.mcp.json` 配置一个 MCP 服务器 + 环境变量扩展
5. 测试计划模式处理多文件重构 vs 直接执行处理单个 bug 修复

帮助用户在当前项目中实践上述步骤。

## Step 3: 知识检查

出 3 道模拟题：
- 自定义团队共享的 /review 命令应放在哪里？（答案：`.claude/commands/`）
- 测试文件分散在代码库各处，如何统一应用约定？（答案：`.claude/rules/` + glob 模式）
- 何时选择计划模式？（答案：多文件架构变更）

## 导航

- 上一领域：`/cca-domain2`（工具设计与 MCP）
- 下一领域：`/cca-domain4`（提示工程与结构化输出）
