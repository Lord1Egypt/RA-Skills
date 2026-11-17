# 麟览（LINLAN）AI 开发助手使用参考说明

本参考资料包用于麟览公司 AI 试点项目，适配 Trae、CodeBuddy、Claude Code 和 opencode。

核心目标是：降低 AI 开发助手任务的上下文准备成本，帮助使用人员沉淀需求、设计、测试、审查和效果评估材料，同时不改变项目既有研发流程。

## 1. 部署方式

### 一、一键部署（推荐）

按"傻瓜程度"任选一种：

| 方式 | 怎么做 |
|---|---|
| **跟 AI 说一句话** | 在项目里对 AI 说"把 assist-skills 部署到当前项目"，AI 会自动完成 |
| **双击** | 技能包内嵌在项目里（`tools\assist-skills\`）时双击 `deploy.cmd` 零输入完成；在安装位置双击则按提示输入目标目录 |
| **右键「发送到」** | 先跑一次 `deploy.cmd -Shortcuts`，之后右键项目文件夹 → 发送到 → 部署AI开发助手(assist-skills) |
| **命令行一行** | 见下 |

命令行方式（`deploy.cmd` / `deploy.sh` 会自动定位 `scripts/` 下脚本，参数一致）：

```cmd
:: Windows
"<技能包目录>\deploy.cmd" D:\your-project
```

```bash
# macOS / Linux
bash <技能包目录>/deploy.sh --target ~/my-project
```

也可以直接调用脚本本体：

```powershell
# Windows
pwsh -File "<技能包目录>\scripts\deploy.ps1" -Target "D:\your-project"
```

```bash
# macOS / Linux
bash <技能包目录>/scripts/deploy.sh --target ~/my-project
```

脚本会把技能包内全部内容复制到目标项目根目录，并自动把 `rules/` 下两份规则改名落地到 `.trae/rules/poc-rule.md`、`.codebuddy/rules/poc-rule.md`。默认不覆盖目标项目中已存在的同名文件，`-DryRun` / `--dry-run` 预览、`-Force` / `--force` 覆盖、`-SkipRules` / `--skip-rules` 跳过规则落地。

**团队分发（一次内嵌、队友零依赖）**：项目负责人执行 `deploy.cmd -Target "D:\your-project" -Vendor`，技能包会被内嵌到 `<项目>\tools\assist-skills`；队友克隆仓库后只需双击 `tools\assist-skills\deploy.cmd`（零输入）即可完成接入，无需安装技能包、无需命令、无需别名。

### 二、手工部署

使用人员通常只需要四步：

1. 将参考资料包内容复制到项目根目录（含 `AGENTS.md`、`CLAUDE.md`、`VERSION.md`、`ai-pilot/`、`rules/`）。
2. 使用 Trae / CodeBuddy 时，把 `rules/trae-poc-rule.md`、`rules/codebuddy-poc-rule.md` 复制改名为项目根目录下的 `.trae/rules/poc-rule.md`、`.codebuddy/rules/poc-rule.md`。
3. 在 AI 对话中输入 `初始化项目`，让 AI 扫描项目并预填 `AGENTS.md` 第 1-4 节。
4. 补充业务背景并确认 AI 推断结果后，开始使用 AI 工具。

不需要合并项目 README。

## 2. 目录说明

| 路径 | 说明 |
|---|---|
| `../AGENTS.md` | 项目级 AI 开发助手使用参考，opencode 原生读取（含麟览公司试点工程参考） |
| `../CLAUDE.md` | Claude Code 引用桥接文件（含公司典型技术栈） |
| `../rules/trae-poc-rule.md` | Trae 规则入口（部署后复制改名为 `.trae/rules/poc-rule.md`） |
| `../rules/codebuddy-poc-rule.md` | CodeBuddy 规则入口（部署后复制改名为 `.codebuddy/rules/poc-rule.md`） |
| `../deploy.cmd` | Windows 最短入口，可双击运行（自动定位 `../scripts/deploy.ps1`） |
| `../deploy.sh` | macOS / Linux 最短入口，转发给 `../scripts/deploy.sh` |
| `../scripts/deploy.ps1` | Windows 一键部署脚本（全量复制 + 规则落位） |
| `../scripts/deploy.sh` | macOS / Linux 一键部署脚本 |
| `standards/` | 需求、设计、测试、审查、上线、记录、测试执行日志等模板 |
| `reference/workflows/` | 快捷指令按需 workflow |
| `poc/` | AI 辅助任务过程产物沉淀目录 |
| `example/` | 麟览公司实际工程场景示例（1WEEK/3DAY/1DAY 三级） |
| `reference/` | 阶段复盘、度量口径、安全配置和 pre-commit 参考 |

## 3. 四工具快速上手

| 工具 | 生效方式 | 使用人员动作 |
|---|---|---|
| Trae | 自动读取 `.trae/rules/poc-rule.md` | 将 `rules/trae-poc-rule.md` 复制改名为 `.trae/rules/poc-rule.md` |
| CodeBuddy | 自动读取 `.codebuddy/rules/poc-rule.md` | 将 `rules/codebuddy-poc-rule.md` 复制改名为 `.codebuddy/rules/poc-rule.md` |
| Claude Code | 自动读取 `CLAUDE.md` | 解压后自动生效 |
| opencode | 自动读取 `AGENTS.md` | 解压后自动生效 |

## 4. 快捷指令分层

### 核心治理指令

| 指令 | 用途 |
|---|---|
| `初始化项目` | 扫描配置并预填 `AGENTS.md` 第 1-4 节 |
| `开始任务：{任务名称}` | 自动建任务、判断级别、生成模板；大型项目中只做最小必要扫描 |
| `完成任务` | 检查产物完整性，按 1WEEK/3DAY/1DAY 分级生成或更新 `ai-usage-record.md` |

### 按需能力指令

| 指令 | 用途 |
|---|---|
| `梳理需求` | 生成或更新 `requirement.md` |
| `开始设计` | 生成或更新 `design.md` |
| `编写测试用例` | 生成或更新 `test-cases.md` |
| `开始编码` | 基于任务上下文实现代码并补充测试 |
| `执行测试` | 运行最小必要测试集，生成 `test-execution-log.md` 并更新测试结论 |
| `审查代码` | 基于 diff 和任务上下文生成或更新 `review-summary.md` |
| `生成阶段汇总` | 负责人只基于任务产物生成 `_summary.md` |

按需能力指令只处理当前目标，不自动补跑整条任务链。

## 5. 任务复杂度与参考产物

| 级别 | 适用场景 | 建议生成文件 |
|---|---|---|
| 1WEEK | >3天，新功能、架构变更、跨系统改造 | context 完整版 + 8 个核心任务文件 + 涉及测试时的 test-execution-log |
| 3DAY | 1-3天，中等需求、接口开发 | context 精简版 + 5 个核心文件 + 涉及测试时的 test-execution-log |
| 1DAY | <1天，Bug fix、配置修改 | review-summary + ai-usage-record；context 极简版可按需补充 |

## 6. 参考资料

- `reference/quick-commands.md`：一页纸快速指令卡（含麟览场景）
- `reference/workflows/`：快捷指令按需 workflow
- `reference/summary-template.md`：阶段复盘参考模板
- `reference/metrics-definition.md`：效果评估参考口径
- `reference/gitignore.template`：安全 gitignore 参考
- `reference/pre-commit-config.yaml`：gitleaks pre-commit 参考

## 7. 负责人生成阶段汇总

`reference/summary-template.md` 不需要普通使用人员手工填写。它是负责人让 AI 生成阶段汇总时使用的参考模板。

负责人可在 AI 对话中输入：

```text
请基于 ai-pilot/poc 下所有任务生成阶段汇总
```

AI 会根据 `reference/workflows/generate-summary.md`，扫描各任务目录下的 `ai-usage-record.md`、`context.md`、`review-summary.md` 等任务产物，并聚合 `ai-usage-record.md` 第 12 节的自定义指令记录，默认生成：

```text
ai-pilot/poc/_summary.md
```

## 8. 使用边界

- 请勿在参考资料包中放置生产密钥、Token、连接串、真实个人信息或敏感业务数据。
- 不建议所有任务都生成完整 8 个文件，可按 1WEEK/3DAY/1DAY 任务复杂度裁剪。
- 1WEEK/3DAY级任务建议整理 context，1DAY级任务可按复杂度选择是否整理。
- AI 输出不建议直接进入交付，应按项目既有 Review、构建检查和测试验证流程确认。
- **麟览数据库设计规范**：字段和表名全大写，每表含七个标准字段（STATUS/CREATE_BY/CREATE_TIME/UPDATE_BY/UPDATE_TIME/DEL_FLAG/REMARK）。
