---
name: capforge
description: Austin Liu | Read-only by default: scan GitHub repos to extract reusable capability docs (capability.md), classify domains, validate format, and sync repos safely. No LLM analysis required.
version: 1.3.3
metadata:
  openclaw:
    requires:
      bins:
        - git
        - node
        - capforge
    # 明确声明本 skill 会在本机创建/写入的状态目录（用于安全扫描与用户知情）
    config:
      stateDirs:
        - "~/.capforge"
    install:
      # 通过固定依赖安装 capforge CLI（避免 npx 远程拉取执行）
      - kind: node
        package: capforge
        bins: [capforge]
    homepage: https://github.com/ldx-person/capforge
    # 额外品牌信息(非强制字段,作为前端展示/检索信息)
    emoji: "⚒️"
---

# CapForge(铸能)

**Austin Liu**:从 GitHub 开源项目中锻造可复用的能力资产。

## 安全与合规声明（重要）

本 skill **默认只读（read-only）**：只执行结构扫描、文档生成、域归类、格式校验与安全的仓库同步。

- 不会自动执行代码改造/重构
- 不会执行隐藏命令、`curl | sh`、或 `npx @latest` 这类不可审计的远程执行
- License 合规仅做提醒与门禁，不提供法律意见

### 运行前确认（降低误操作风险）

在运行任何命令前，你必须先把将要执行的命令逐条展示给用户，并获得用户明确确认后再执行（尤其是 git clone / git pull 等会写入磁盘的操作）。

如果用户明确要求执行改造/重构，请在执行前二次确认，并遵循 CapForge 的 license 门禁策略。

## 你会得到什么

CapForge 的职责是**纯代码结构扫描**(不调用 LLM)并产出可被 Agent / 人类阅读的 Markdown;你(或 OpenClaw/Clawdbot)再基于扫描结果把能力"资产化":

- `capability.md`:可复用能力的结构化说明(接口、输入输出、关键文件等)
- `domains.md`:跨项目能力域归类摘要
- `validation-report.md`:capability.md 结构校验报告

## 适用场景(核心卖点)

- 你想快速"看懂一个开源项目能复用什么",并沉淀为可检索的能力资产(`capability.md`)。
- 你想把多个开源 Agent 项目做横向对比,快速选型/组合能力(配合 `domains.md`)。

## 工作空间约定(重要)

CapForge 默认将所有克隆仓库与输出统一放在同一个工作空间:

- 默认:`~/.capforge/`
  - `repos/`:克隆的项目
  - `output/`:扫描/能力/计划等产物

你可以通过任意一种方式覆盖:

- `CAPFORGE_WORKSPACE=/path/to/ws`
- `capforge --workspace /path/to/ws <command>`

## 推荐流程（默认只读）

当用户给你一个 GitHub 项目链接时,按顺序执行:

### Step 1) Clone + Scan

```bash
capforge import <github-url>
capforge scan <project-name>
```

> `<project-name>` 一般是仓库名(URL 最后一段)。

### Step 2) 生成 capability.md(你来写,CapForge 不写)

先让 CapForge 生成扫描数据(Markdown):

```bash
capforge describe <project-name>
```

它会写入(默认工作空间):

- `~/.capforge/output/capabilities/<project-name>.md`

然后你需要基于:
1) 扫描数据
2) 仓库源码(`~/.capforge/repos/<project-name>/...`)
生成一个"真正的能力描述"并覆盖写回 `output/capabilities/<project-name>.md`(或另存为 `capability.md` 再统一收集)。

**capability.md 必须包含这些章节:**

- `## 概述`
- `## 技术栈`
- `## 核心能力`(建议 5-10 个能力点,包含真实接口/函数签名与关键文件路径)
- `## 集成指南`
- `## 改造文件`

### Step 3) 生成 transform-plan.md(你来写,CapForge 只给扫描数据)

```bash
npx capforge transform <project-name>
```

它会写入:

- `~/.capforge/output/transform-plans/<project-name>.md`

然后你需要把该文件改写为"真正的改造计划",建议结构:

```markdown
# <Project> 改造计划

## 总体策略

## 改造任务

### [high] Task 1: <title>
- **目标文件:** <targetFile>
- **动作:** extract|abstract|dehardcode|decouple|adapter
- **依赖:** <task ids>
- **描述:** <description>
- **验收标准:** <acceptanceCriteria>
```

### Step 4) 归类 domains.md

```bash
capforge classify-domains
```

输出:

- `~/.capforge/output/domains.md`

### Step 5) 校验格式

```bash
capforge validate
```

输出:

- `~/.capforge/output/validation-report.md`

## 同步更新（检查 GitHub 是否有新变更）

当用户说“更新项目 / 同步最新 / 检查更新”时，执行安全的增量更新（默认 ff-only，不会覆盖本地改动）：

```bash
# 更新单个项目
capforge update <project-name>

# 更新全部已导入项目
capforge update --all
```

如果检测到本地改动（dirty working tree），CapForge 会默认跳过并提示原因（避免误伤本地修改）。
