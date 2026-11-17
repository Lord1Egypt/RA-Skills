# 麟览（LINLAN）AI 开发助手使用参考说明

[English](./README.en.md)

当前版本：`v1.0.2-linlan` | 发布日期：2026-09

本参考资料包用于麟览公司 AI 试点项目，适配 **Trae**、**CodeBuddy**、**Claude Code** 和 **opencode** 四款 AI 工具。核心目标是降低 AI 开发助手任务的上下文准备成本，帮助使用人员沉淀需求、设计、测试、审查和效果评估材料，同时不改变项目既有研发流程。

---

## 文件索引

### 根目录

| 文件 | 说明 |
|---|---|
| [AGENTS.md](./AGENTS.md) | 项目级 AI 开发助手使用参考（opencode 原生读取，含麟览公司试点工程参考） |
| [CLAUDE.md](./CLAUDE.md) | Claude Code 引用桥接文件（含公司典型技术栈） |
| [VERSION.md](./VERSION.md) | 参考资料包版本、兼容性和分发说明 |
| [deploy.cmd](./deploy.cmd) | Windows 最短入口，**双击即可部署**（自动定位 `scripts/deploy.ps1`；内嵌布局下零输入） |
| [deploy.sh](./deploy.sh) | macOS / Linux 最短入口，转发给 `scripts/deploy.sh` |
| [scripts/deploy.ps1](./scripts/deploy.ps1) | Windows 一键部署脚本（全量复制 + 规则落位 + `-Vendor` 内嵌 + `-Shortcuts` 右键入口） |
| [scripts/deploy.sh](./scripts/deploy.sh) | macOS / Linux 一键部署脚本 |

### 工具规则入口

规则文件在包内放在 `rules/`（非隐藏目录），部署时复制改名为目标项目的点目录文件：

| 工具 | 包内文件 | 目标项目路径 | 说明 |
|---|---|---|---|
| Trae | [rules/trae-poc-rule.md](./rules/trae-poc-rule.md) | `.trae/rules/poc-rule.md` | 复制改名后自动读取 |
| CodeBuddy | [rules/codebuddy-poc-rule.md](./rules/codebuddy-poc-rule.md) | `.codebuddy/rules/poc-rule.md` | 复制改名后自动读取 |

### AI Pilot 主目录

| 文件 | 说明 |
|---|---|
| [ai-pilot/README.md](./ai-pilot/README.md) | 参考资料包使用说明与目录总览 |

### 标准模板（`ai-pilot/standards/`）

| 文件 | 用途 |
|---|---|
| [00-ai-usage-rule.md](./ai-pilot/standards/00-ai-usage-rule.md) | AI 使用规则总览 |
| [01-requirement-spec-template.md](./ai-pilot/standards/01-requirement-spec-template.md) | 需求规格说明模板 |
| [02-design-template.md](./ai-pilot/standards/02-design-template.md) | 技术设计模板 |
| [03-api-design-template.md](./ai-pilot/standards/03-api-design-template.md) | 接口设计模板 |
| [04-db-design-template.md](./ai-pilot/standards/04-db-design-template.md) | 数据库设计模板 |
| [05-test-case-template.md](./ai-pilot/standards/05-test-case-template.md) | 测试用例模板 |
| [06-code-review-template.md](./ai-pilot/standards/06-code-review-template.md) | 代码审查模板 |
| [07-release-note-template.md](./ai-pilot/standards/07-release-note-template.md) | 发布说明模板 |
| [08-ai-usage-record-template.md](./ai-pilot/standards/08-ai-usage-record-template.md) | AI 使用记录模板 |
| [09-poc-evaluation-template.md](./ai-pilot/standards/09-poc-evaluation-template.md) | 试点评估模板 |
| [10-prompt-guide.md](./ai-pilot/standards/10-prompt-guide.md) | Prompt 编写指南 |
| [11-context-1week-template.md](./ai-pilot/standards/11-context-1week-template.md) | 1WEEK 级任务上下文模板 |
| [12-context-3day-template.md](./ai-pilot/standards/12-context-3day-template.md) | 3DAY 级任务上下文模板 |
| [13-context-1day-template.md](./ai-pilot/standards/13-context-1day-template.md) | 1DAY 级任务上下文模板 |
| [14-test-execution-log-template.md](./ai-pilot/standards/14-test-execution-log-template.md) | 测试执行日志模板 |

### 快捷指令 Workflow（`ai-pilot/reference/workflows/`）

| 指令 | 文件 | 说明 |
|---|---|---|
| 初始化项目 | [00-init-project.md](./ai-pilot/reference/workflows/00-init-project.md) | 扫描配置并预填项目信息 |
| 开始任务 | [01-start-task.md](./ai-pilot/reference/workflows/01-start-task.md) | 创建任务目录和基础产物 |
| 梳理需求 | [02-prepare-requirement.md](./ai-pilot/reference/workflows/02-prepare-requirement.md) | 生成或更新需求说明 |
| 开始设计 | [03-prepare-design.md](./ai-pilot/reference/workflows/03-prepare-design.md) | 生成或更新技术设计 |
| 编写测试用例 | [04-prepare-test-cases.md](./ai-pilot/reference/workflows/04-prepare-test-cases.md) | 生成或更新测试用例 |
| 开始编码 | [05-start-coding.md](./ai-pilot/reference/workflows/05-start-coding.md) | 基于任务上下文实现代码 |
| 执行测试 | [06-run-tests.md](./ai-pilot/reference/workflows/06-run-tests.md) | 运行最小必要测试集 |
| 审查代码 | [07-code-review.md](./ai-pilot/reference/workflows/07-code-review.md) | 基于 diff 做风险审查 |
| 完成任务 | [08-finish-task.md](./ai-pilot/reference/workflows/08-finish-task.md) | 补充 AI 使用记录和完整性检查 |
| 生成阶段汇总 | [09-generate-summary.md](./ai-pilot/reference/workflows/09-generate-summary.md) | 基于任务产物生成试点汇总 |

### 参考资料（`ai-pilot/reference/`）

| 文件 | 说明 |
|---|---|
| [quick-commands.md](./ai-pilot/reference/quick-commands.md) | 一页纸快速指令卡 |
| [metrics-definition.md](./ai-pilot/reference/metrics-definition.md) | 效果评估参考口径 |
| [summary-template.md](./ai-pilot/reference/summary-template.md) | 阶段复盘参考模板 |
| [gitignore.template](./ai-pilot/reference/gitignore.template) | 安全 gitignore 参考 |
| [pre-commit-config.yaml](./ai-pilot/reference/pre-commit-config.yaml) | gitleaks pre-commit 参考 |

---

## 任务产物目录

真实任务产物建议沉淀到：

```
ai-pilot/poc/{任务编号}/
```

标准任务产物包括：

| 文件 | 用途 |
|---|---|
| `context.md` | 任务上下文索引 |
| `requirement.md` | 需求背景、范围、验收标准 |
| `design.md` | 技术方案、影响范围、关键流程 |
| `api-design.md` | 接口定义、请求响应、错误码 |
| `db-design.md` | 表结构、字段、索引、迁移策略 |
| `test-cases.md` | 功能、异常、边界、回归测试 |
| `test-execution-log.md` | 测试执行日志 |
| `review-summary.md` | 代码审查摘要 |
| `release-note.md` | 上线内容、影响范围、回滚方案 |
| `ai-usage-record.md` | AI 使用过程、采纳情况、效率指标 |

---

## 任务复杂度分级

| 级别 | 适用场景 | 建议产物 |
|---|---|---|
| **1WEEK**（>3天） | 新功能、架构变更、跨系统改造 | context 完整版 + 8 个核心文件 |
| **3DAY**（1-3天） | 中等需求、接口开发 | context 精简版 + 5 个核心文件 |
| **1DAY**（<1天） | Bug fix、配置修改 | review-summary + ai-usage-record |

---

## 快速上手

### 一键部署（推荐）

按"傻瓜程度"从高到低，任选一种：

| 方式 | 怎么做 | 适合谁 |
|---|---|---|
| **跟 AI 说一句话** | 在项目里对 AI 说"把 assist-skills 部署到当前项目" | 所有人（最推荐） |
| **双击** | 技能包内嵌在项目里时，双击 `deploy.cmd` 即零输入完成；在安装位置双击则按提示输入目标目录 | 不想用命令的人 |
| **右键「发送到」** | 先跑一次 `deploy.cmd -Shortcuts`，之后右键项目文件夹 → 发送到 → 部署AI开发助手(assist-skills) | 完全不想碰命令的人 |
| **命令行一行** | 见下方代码块 | 习惯终端的人 |

```cmd
:: Windows：包根目录的 deploy.cmd，自动定位 scripts\deploy.ps1
"%USERPROFILE%\.openclaw\workspace\skills\assist-skills\deploy.cmd" D:\your-project
```

```bash
# macOS / Linux
bash ~/.openclaw/workspace/skills/assist-skills/deploy.sh --target ~/my-project
```

也支持配别名（`function ai-deploy { & "$HOME\.openclaw\workspace\skills\assist-skills\deploy.cmd" @args }` / `alias ai-deploy="bash ~/.openclaw/workspace/skills/assist-skills/deploy.sh"`），之后只需 `ai-deploy D:\your-project`。

### 团队分发：让项目自带部署入口

项目负责人执行一次：

```cmd
:: 部署 + 把技能包内嵌到 <项目>\tools\assist-skills
deploy.cmd -Target "D:\your-project" -Vendor
```

提交后，**队友克隆仓库只需双击 `tools\assist-skills\deploy.cmd`**（零输入）即可完成接入，完全不需要安装本技能包、不需要命令、不需要别名。内嵌位置可用 `-VendorDir` 调整（默认 `tools\assist-skills`）。

脚本会把包内全部内容复制到目标项目根目录，并自动把 `rules/` 下两份规则文件改名落地为 `.trae/rules/poc-rule.md`、`.codebuddy/rules/poc-rule.md`。默认不覆盖目标项目中已存在的同名文件，先加 `-DryRun` / `--dry-run` 可预览。

### 手工部署

1. 将参考资料包内容复制到项目根目录（含 `AGENTS.md`、`CLAUDE.md`、`VERSION.md`、`ai-pilot/`、`rules/`）
2. 使用 Trae / CodeBuddy 时，把 `rules/trae-poc-rule.md`、`rules/codebuddy-poc-rule.md` 复制改名为 `.trae/rules/poc-rule.md`、`.codebuddy/rules/poc-rule.md`
3. 在 AI 对话中输入 `初始化项目`，让 AI 扫描项目并预填 `AGENTS.md` 第 1-4 节
4. 补充业务背景并确认 AI 推断结果后，开始使用 AI 工具

---

## 使用边界

- 请勿放置生产密钥、Token、连接串、真实个人信息或敏感业务数据
- 不建议所有任务都生成完整 8 个文件，可按任务复杂度裁剪
- AI 输出不建议直接进入交付，应经 Review、构建检查和测试验证确认