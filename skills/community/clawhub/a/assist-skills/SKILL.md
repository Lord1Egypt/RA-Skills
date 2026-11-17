---
name: assist-skills
description: AI开发助手项目接入技能。功能：(1)内置 deploy.cmd/deploy.ps1/deploy.sh，支持双击、右键"发送到"、命令行、以及 -Vendor 把技能包内嵌进项目供团队分发，一键把参考资料包部署到目标项目并自动落地各工具规则 (2)配置Trae/CodeBuddy/Claude Code/opencode四款工具规则 (3)生成需求/设计/测试/审查标准模板 (4)10个快捷指令Workflow覆盖全流程 (5)1WEEK/3DAY/1DAY三级任务复杂度分级。当用户需要在项目中接入AI辅助开发流程、把技能包/参考资料包部署或拷贝到工程目录、让团队其他成员也能直接用上AI开发助手、配置AI工具规则、生成标准化模板时使用此技能。
---

# AI 开发助手项目接入技能

> 技能版本：v1.0.2
> 整理日期：2026-09-13
> 适配工具：Trae / CodeBuddy / Claude Code / opencode

## 定位

本技能解决"如何在项目中快速接入 AI 辅助开发流程"的问题。核心产出是一套标准化的参考资料包，包含项目级 AI 助手配置、需求/设计/测试/审查模板和快捷指令 Workflow，帮助团队在不改变既有研发流程的前提下降低 AI 开发助手的上下文准备成本。

## 1. 部署流程

### 1.1 一键部署（推荐）

技能包内置部署脚本，一次操作即可完成"把技能包全部文件复制到目标项目根目录 + 规则文件落地到 `.trae`/`.codebuddy` 点目录"。包**根目录**的 `deploy.cmd` / `deploy.sh` 是最短入口，它只做"定位技能包 + 调用 `scripts/` 下脚本"，参数完全一致。

按"傻瓜程度"从高到低排列，任选一种即可。

#### 方式 A：跟 AI 说一句话（最省事，强烈推荐）

在目标项目里对 AI 说 **"把 assist-skills 部署到当前项目"**（或"接入 AI 开发流程"），AI 会读取本说明并执行部署脚本。全程不需要记路径、不需要敲命令、不需要配别名。

> 前提：本机已安装过技能包一次（`clawhub install assist-skills`，全局生效），或目标项目里已内嵌技能包（见方式 D）。

#### 方式 B：Windows 双击（零输入）

- **技能包已内嵌在项目里**（如 `tools\assist-skills\`）：双击 `deploy.cmd` 即可，脚本自动识别项目根目录并部署，**不需要输入任何内容**。
- **技能包在全局安装位置**：双击 `deploy.cmd`，按提示输入目标项目目录（直接回车 = 当前目录）。

脚本自动优先使用 PowerShell 7（`pwsh`），未安装时回退 Windows PowerShell。

#### 方式 C：右键「发送到」（配一次，长期一键）

先执行一次：

```cmd
"%USERPROFILE%\.openclaw\workspace\skills\assist-skills\deploy.cmd" -Shortcuts
```

它会在 Windows 的**「发送到」菜单**和**桌面**创建"部署AI开发助手(assist-skills)"。之后：

> 在资源管理器中右键任意项目文件夹 → 发送到 → 部署AI开发助手(assist-skills) → 完成。

对完全不想碰命令的同事，这是最友好的一种。

#### 方式 D：团队分发——把技能包内嵌进项目（队友零依赖）

项目负责人执行一次：

```cmd
:: 部署 + 把技能包内嵌到 <项目>\tools\assist-skills
"%USERPROFILE%\.openclaw\workspace\skills\assist-skills\deploy.cmd" -Target "D:\your-project" -Vendor
```

提交后，项目自带部署入口。**队友克隆仓库后只需双击 `tools\assist-skills\deploy.cmd`** 即可零输入完成接入，完全不需要安装 ClawHub、不需要技能包、不需要任何命令。

内嵌位置可用 `-VendorDir` 调整（默认 `tools\assist-skills`）；内嵌时会自动排除 `_meta.json`、`.clawhubignore`、`.clawhub` 等安装元数据。

#### 方式 E：命令行一行

```cmd
:: Windows：包根目录的 deploy.cmd，自动定位 scripts\deploy.ps1
"%USERPROFILE%\.openclaw\workspace\skills\assist-skills\deploy.cmd" D:\your-project
```

```bash
# macOS / Linux
bash ~/.openclaw/workspace/skills/assist-skills/deploy.sh --target ~/my-project
```

也支持配别名（`function ai-deploy { & "$HOME\.openclaw\workspace\skills\assist-skills\deploy.cmd" @args }`）或直接调用 `scripts/deploy.ps1` / `scripts/deploy.sh`，两者参数与新入口完全一致。

> **给 AI 助手（重要）**：当用户说"部署 AI 开发助手""把 assist-skills 拷到项目里""接入 AI 开发流程""初始化 AI 开发流程"时，**不要逐个文件手工复制，也不要让用户自己敲命令**，按下面顺序自行完成：
>
> 1. 定位技能包目录：优先本机内嵌副本（项目下 `tools\assist-skills\`）；否则 ClawHub 安装位置 `~/.openclaw/workspace/skills/assist-skills`；再否则本地仓库中的 `assist-skills/`（以本 SKILL.md 所在目录为准）。
> 2. 执行部署：`deploy.cmd -Target <项目根>`（Windows）/ `bash deploy.sh --target <项目根>`（macOS、Linux）。**当前目录就是项目根时可省略 `-Target`**。
> 3. 用户提到"给团队/让队友也能用"时，追加 `-Vendor` 把技能包内嵌到项目。
> 4. 部署完成后提示用户在对话里输入"初始化项目"，以便预填 `AGENTS.md` 第 1-4 节。
>
> 已有的交付物不要重复覆盖：脚本默认跳过同名文件，只有用户明确要求覆盖时才加 `-Force`。

脚本参数：

| 参数（ps1 / sh） | 作用 |
|------------------|------|
| `-Target <目录>` / `--target <dir>` | 目标项目根目录，默认当前目录 |
| `-Force` / `--force` | 覆盖目标项目已存在的同名文件（默认跳过并提示） |
| `-DryRun` / `--dry-run` | 只预览将要写入的文件，不实际复制 |
| `-SkipRules` / `--skip-rules` | 跳过 `.trae`/`.codebuddy` 规则落地（只用 Claude Code / opencode 时可加） |
| `-IncludeSkillFiles` / `--include-skill-files` | 额外复制 `README.md`、`README.en.md`、`SKILL.md`、`scripts/` |
| `-Auto`（仅 ps1，`deploy.cmd` 无参数运行时自动带上） | 自动判定目标项目根：内嵌布局（技能包位于项目子目录且带 `.git`/`pom.xml` 等标记）直接取项目根，否则取当前目录，仍无法判定才提示 |
| `-Vendor` / `-VendorDir <相对路径>`（仅 ps1） | 部署的同时把技能包整体内嵌到项目（默认 `tools\assist-skills`），供团队分发 |
| `-Shortcuts`（仅 ps1，Windows） | 创建「发送到」菜单与桌面快捷方式，实现右键一键部署 |
| `-Pause`（仅 ps1） | 结束后等待回车再退出，便于双击查看结果 |

脚本行为：

- 目标目录不存在时自动创建
- 默认**不覆盖**已有文件，冲突时打印 `[跳过]`（确认可覆盖后再加 `-Force` / `--force` 重跑）
- **内嵌布局自动识别**：技能包位于项目子目录（如 `<项目>\tools\assist-skills`）且项目带 `.git`、`pom.xml`、`package.json` 等标记时，双击即按该项目根部署，零输入；缺少标记时只要求回车确认一次
- **安全边界**：拒绝把技能包自身、技能包内部、以及"技能包恰为其直属子目录的上级目录"当作目标（防止把 40+ 个文件误铺到技能包源码仓库根目录）
- **防不可见字符**：自动清洗路径首尾的 BOM / 零宽字符并忽略大小写比较，避免"看起来正确的路径"绕过上述校验
- 结束时打印"新写入 / 覆盖 / 跳过"统计

### 1.2 手工部署（不使用脚本时）

规则文件在技能包内放在**非点号目录** `rules/`（ClawHub 打包会过滤点号开头的条目，直接放 `.trae/`、`.codebuddy/` 会随包丢失），手工部署分两步：

```powershell
# 第 1 步：只复制本包自身文件到项目根目录（保留项目已有业务代码与测试）
Copy-Item "assist-skills\AGENTS.md","assist-skills\CLAUDE.md","assist-skills\VERSION.md" -Destination "D:\your-project"
Copy-Item "assist-skills\ai-pilot" -Destination "D:\your-project\ai-pilot" -Recurse

# 第 2 步：使用 Trae / CodeBuddy 时，把规则文件复制改名到项目点目录（工具只在项目根读取这两个路径）
New-Item -ItemType Directory -Force "D:\your-project\.trae\rules","D:\your-project\.codebuddy\rules" | Out-Null
Copy-Item "assist-skills\rules\trae-poc-rule.md" "D:\your-project\.trae\rules\poc-rule.md"
Copy-Item "assist-skills\rules\codebuddy-poc-rule.md" "D:\your-project\.codebuddy\rules\poc-rule.md"
```

> 手工部署**只新增文件，不删除项目内容**。目标目录会新增：`AGENTS.md`、`CLAUDE.md`、`VERSION.md`、`ai-pilot/`、`.trae/rules/poc-rule.md`、`.codebuddy/rules/poc-rule.md`；若上述同名文件已存在，请先确认内容再决定是否覆盖。
>
> 只使用 Claude Code 或 opencode 时，第 2 步可跳过（两者只读 `CLAUDE.md`、`AGENTS.md`）。

部署后目标项目新增以下目录和文件：

```
your-project/
  AGENTS.md                          项目级AI助手配置（opencode原生读取）
  CLAUDE.md                          Claude Code引用桥接
  VERSION.md                         版本与分发说明
  .trae/rules/poc-rule.md            Trae项目规则（由 rules/trae-poc-rule.md 落地）
  .codebuddy/rules/poc-rule.md       CodeBuddy项目规则（由 rules/codebuddy-poc-rule.md 落地）
  ai-pilot/
    README.md                        使用说明
    standards/                       15个标准模板
    reference/
      workflows/                     10个快捷指令Workflow
      metrics-definition.md          度量口径定义
      quick-commands.md              快捷命令参考
```

### 1.3 初始化项目

在 AI 对话中输入"初始化项目"，AI 扫描项目并预填 `AGENTS.md` 第 1-4 节（项目概览、技术栈、目录结构、构建与测试命令）。

### 1.4 补充确认

人工补充业务背景、确认 AI 推断结果后，开始使用 AI 工具。

## 2. 标准模板体系（15个）

`ai-pilot/standards/` 目录下，按研发流程排列：

| 编号 | 模板 | 用途 |
|------|------|------|
| 00 | ai-usage-rule | AI 使用规范（总纲） |
| 01 | requirement-spec-template | 需求规格模板 |
| 02 | design-template | 设计文档模板 |
| 03 | api-design-template | API 设计模板 |
| 04 | db-design-template | 数据库设计模板 |
| 05 | test-case-template | 测试用例模板 |
| 06 | code-review-template | 代码审查模板 |
| 07 | release-note-template | 发版说明模板 |
| 08 | ai-usage-record-template | AI 使用记录模板 |
| 09 | poc-evaluation-template | POC 评估模板 |
| 10 | prompt-guide | Prompt 编写指南 |
| 11 | context-1week-template | 1周任务上下文模板 |
| 12 | context-3day-template | 3天任务上下文模板 |
| 13 | context-1day-template | 1天任务上下文模板 |
| 14 | test-execution-log-template | 测试执行日志模板 |

## 3. 快捷指令 Workflow（10个）

`ai-pilot/reference/workflows/` 目录下，覆盖从项目初始化到任务完成的全流程：

| 编号 | 指令 | 触发词 |
|------|------|--------|
| 00 | init-project | 初始化项目 |
| 01 | start-task | 开始任务 |
| 02 | prepare-requirement | 准备需求 |
| 03 | prepare-design | 准备设计 |
| 04 | prepare-test-cases | 准备测试用例 |
| 05 | start-coding | 开始编码 |
| 06 | run-tests | 运行测试 |
| 07 | code-review | 代码审查 |
| 08 | finish-task | 完成任务 |
| 09 | generate-summary | 生成总结 |

## 4. 任务复杂度分级

按任务周期选择对应的上下文模板，避免过度或不足的文档产出：

| 级别 | 周期 | 适用场景 | 模板 |
|------|------|----------|------|
| 1WEEK | 1周+ | 大型功能、架构改造、跨模块重构 | context-1week-template |
| 3DAY | 2-3天 | 中等功能、接口开发、组件封装 | context-3day-template |
| 1DAY | 1天内 | Bug修复、小功能、配置调整 | context-1day-template |

## 5. 工具适配

| AI 工具 | 技能包内文件 | 目标项目落位路径 | 说明 |
|---------|--------------|------------------|------|
| Trae | `rules/trae-poc-rule.md` | `.trae/rules/poc-rule.md` | 由部署脚本自动改名落地，Trae 读取项目规则 |
| CodeBuddy | `rules/codebuddy-poc-rule.md` | `.codebuddy/rules/poc-rule.md` | 由部署脚本自动改名落地，CodeBuddy 读取项目规则 |
| Claude Code | `CLAUDE.md` | `CLAUDE.md` | 引用桥接文件，指向 AGENTS.md |
| opencode | `AGENTS.md` | `AGENTS.md` | 原生读取项目级配置 |

## 6. 检查清单

- [ ] 已按 1.1 的方式 A~E 之一完成部署（AI 一句话 / 双击 / 右键发送到 / 内嵌分发 / 命令行）
- [ ] 目标项目根目录已出现 `AGENTS.md`、`CLAUDE.md`、`VERSION.md`、`ai-pilot/`
- [ ] `-SkipRules` 未开启时，`.trae/rules/poc-rule.md`、`.codebuddy/rules/poc-rule.md` 已就位
- [ ] AGENTS.md 第 1-4 节已预填并确认
- [ ] 业务背景已补充
- [ ] 团队分发场景：已用 `-Vendor` 内嵌技能包，并确认 `tools\assist-skills\deploy.cmd` 可双击部署
- [ ] 团队成员已了解快捷指令用法（必要时先用 `-Shortcuts` 建好右键入口）
- [ ] 度量口径（`metrics-definition.md`）已阅读

## 核心文件

| 文件 | 用途 |
|------|------|
| `deploy.cmd` | Windows 最短入口：双击即可部署（自动定位 `scripts/deploy.ps1`，pwsh 优先、回退 PowerShell）；内嵌布局下零输入 |
| `deploy.sh` | macOS / Linux 最短入口：转发给 `scripts/deploy.sh` |
| `scripts/deploy.ps1` | Windows 一键部署脚本（全量复制 + 规则落位 + `-Vendor` 内嵌 + `-Shortcuts` 右键入口 + `-Auto` 自动识别） |
| `scripts/deploy.sh` | macOS / Linux 一键部署脚本 |
| `rules/` | 规则文件源（`trae-poc-rule.md` / `codebuddy-poc-rule.md`），部署时改名落到 `.trae`、`.codebuddy` 点目录（避免被 ClawHub 打包过滤） |
| `AGENTS.md` | 项目级 AI 助手配置模板（12KB，含完整填写指引） |
| `ai-pilot/standards/` | 15 个标准模板（需求/设计/测试/审查/记录） |
| `ai-pilot/reference/workflows/` | 10 个快捷指令 Workflow |
| `ai-pilot/reference/metrics-definition.md` | AI 辅助研发度量口径定义（17KB） |
