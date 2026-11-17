# Agent Guild

> 让多个本地 AI 助手复用同一份偏好、项目约定和工作交接。

[English](README_EN.md) | **中文**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/dqsjqian/agent-guild/blob/main/LICENSE)
[![Protocol](https://img.shields.io/badge/protocol-v4.0-green)](references/SPEC.md)

Agent Guild 面向**同一用户使用的多个、受信任且能够读写本地文件的 AI 助手**。
它把共享上下文放进 `~/.agent-guild/` 的 Markdown / JSON 文件：你能查看、修改、备份，
切换助手时也能继续使用。运行时 skill 提供读写约定，Python CLI 处理并发写入、检索和归档。

## 先验证一次：A 记住，B 找到

安装并让两个助手接入后，用一条没有敏感内容的演示约定测试：

1. 对助手 A 说：
   > 请记住这条长期演示约定：演示项目的交付说明必须包含验证结果。
   > 保存到协会的 `memory/shared/demo.md`，登记到 `memory/shared/INDEX.md`，并告诉我保存路径。
2. 切换到助手 B，说：
   > 在协会里查找“演示项目”的交付约定，复述内容并引用来源文件。
3. 确认 B 找到同一条内容和文件。测试结束后，可以删除这条演示约定及其索引项。

这才是共享记忆的验收结果；磁盘上出现 skill 文件只是接入的第一步。
长期偏好和项目约定放在身份、规则或共享记忆中；`log/daily/` 记录会话经过，不代替长期记忆。
助手仍需按协议读取相关上下文，Agent Guild 不会自动把所有历史塞进每一次回答。

## 跨会话接班：先问待办，再选任务

1. A 做到一半：保存独立任务包（日期 + 随机 ID + 短标题），包括完整上下文、JSON、脚本、图片与验证材料。
2. 打开 B 做其他事：不加载 A 的任务。默认启动只读身份、日常习惯与通用规则。
3. 问 B“我有哪些事没做完？”：只列元信息，生成该会话独立的序号快照。
4. 选择“继续第 2 个”：核对列表版本与任务所有权后，只读这一项。A 仍在处理则先确认转交或协作。
5. 任务验收闭环：整个目录由 `handoff/active/` 进入 `handoff/archive/`，移出待办；对话结束不等于任务结束。

版本检查拒绝迟到写入；接管会撤销旧会话写权。没有宿主结束钩子时，恢复保证仅到最近成功检查点。
任务上下文不是新的执行授权，附件脚本不会自动执行。历史迁移用 `ag migrate --dry-run` 预览；
旧焦点和消息不会自动猜成待办，旧数据不会在升级时被移动或删除。

## 适合谁，有哪些边界

| 你的需求 | Agent Guild 的做法 |
|---|---|
| 经常切换两个或更多本地助手，不想重复交代约定 | 共享身份、规则、项目状态和可检索的记忆文件 |
| 想看清助手记了什么，并自行修正 | 使用普通 Markdown / JSON 文件，不依赖专有数据库 |
| 想交接未完成的工作 | 每个任务一个目录；问待办只列元信息，选择后才恢复该任务 |
| 想把个人工作上下文搬到另一台设备 | 区分共享、平台和本机信息；文件搬运由你选择 |
| 还想统一 skills、工具及其数据位置 | 可选择完整共享中心模式；无需为了试用记忆而先迁移这些资产 |

它不提供多人权限隔离、自动跨设备同步或后台任务执行。没有本地文件访问能力的助手，
不能直接使用这个目录；有文件访问能力但不能加载自定义 skill 的助手，可以手动读取协议，
不过需要在会话中提醒它使用，不等同于自动触发。

核心取舍是：**少量基础设施、可检查的文件，换取助手遵守读写约定和用户管理文件访问范围。**
CLI 需要 Python 3.9+，只使用标准库；没有服务端或常驻进程。

## 安装与接入

### 1. 建立中央目录

**先下载、检查，再执行；不要把网络响应直接传给 shell。** 安装器与引导 CLI
必须来自同一已审查的固定提交，不从可变 `main` 逐文件拉取运行代码。
本工作树的安全修复尚未发布；已公开的 `4.0.0` 不因此自动获得修复。当前优先使用下方
“从源码安装”的已审查工作树；只有含全部运行模块且具有校验依据的 release 才能通过新安装器。

macOS / Linux / WSL / Git Bash（Bash、curl、Python 3.9+），在空目录中运行：

```bash
SOURCE_COMMIT="填入已审查的40位提交ID"
[[ "$SOURCE_COMMIT" =~ ^[0-9a-fA-F]{40}$ ]] || exit 1
BASE="https://raw.githubusercontent.com/dqsjqian/agent-guild/$SOURCE_COMMIT/scripts"
curl --proto '=https' --tlsv1.2 -fsSL "$BASE/install.sh" -o install.sh
curl --proto '=https' --tlsv1.2 -fsSL "$BASE/ag.py" -o ag.py
less install.sh ag.py
# 确认两份源码后，另行执行：
AGENT_GUILD_VERSION=4.0.0 bash ./install.sh
```

Windows（PowerShell 5.1+、Python 3.9+），同样先下载检查：

```powershell
$SourceCommit = '填入已审查的40位提交ID'
if ($SourceCommit -notmatch '^[0-9a-fA-F]{40}$') { throw '需要固定提交 ID' }
$Base = "https://raw.githubusercontent.com/dqsjqian/agent-guild/$SourceCommit/scripts"
Invoke-WebRequest -UseBasicParsing "$Base/install.ps1" -OutFile install.ps1
Invoke-WebRequest -UseBasicParsing "$Base/ag.py" -OutFile ag.py
Get-Content .\install.ps1
Get-Content .\ag.py
# 确认源码后另行执行，不绕过系统执行策略：
$env:AGENT_GUILD_VERSION = '4.0.0'
.\install.ps1
```

安装器复用已检查的本地 `ag.py`，从固定 tag 的 GitHub release ZIP 安装完整协议，
随后初始化缺失模板并打印接入口令；不会修改助手自己的目录。
`AGENT_GUILD_PYTHON` 可指定 Python 可执行文件，`AGENT_GUILD_DIR` 可指定运行目录。
本地引导脚本的信任来自你的源码检查与固定提交选择，不来自它自己声称的 hash。

### 2. 让每个助手接入

初次试用建议只接入共享记忆，对助手说：

> 请读 `~/.agent-guild/ONBOARDING.md`，仅接入共享记忆，保留现有 skills 和工具目录。

需要统一管理更多资产时，可以明确选择完整共享中心：

> 请读 `~/.agent-guild/ONBOARDING.md`，按完整共享中心模式接入，报告迁移的目录和使用的安装方式。

完整模式会把可迁移资产放进协会，并尝试用目录链接连接助手的 skills 目录；不兼容时使用
逐 skill 链接、拷贝或手动读取。详情见 [接入流程](references/ONBOARDING.md)。
接入后运行上面的两助手验证，确认记忆能被实际找到。

### 从源码安装

将**项目源码**与**私人协会数据**分开放置。在你选择的源码工作目录运行：

```bash
git clone https://github.com/dqsjqian/agent-guild agent-guild-source
# 先核对提交 ID 并检查源码；这条路径信任本地工作树，不进行 release 校验。
git -C agent-guild-source rev-parse HEAD
# 确认后另行执行：
python3 agent-guild-source/scripts/ag.py init demo-agent
```

`demo-agent` 可换成你的助手名称；Windows 若使用 `python` 命令，相应替换 `python3`。
`init` 会在 `~/.agent-guild/` 创建运行目录并安装 skill，然后按上面的口令让助手接入。
不要把源码仓库直接克隆到私人数据目录。

## 你能控制什么

- **记忆内容**：身份、规则和项目文件由用户控制。助手只记录任务所需的摘要；不要把密码、token 等凭据写进共享记忆。
- **网络与更新**：安装需要下载文件。运行时默认在 `bootstrap` 后按设备最多每 24 小时检查一次三个公开版本源，不上传记忆内容。`UPGRADE.md` 中 `mode = check` 只提示，`mode = apply` 会下载并安装新版本，`mode = off` 关闭自动检查；手动 `upgrade` 仍可使用。
- **只查看上下文**：`bootstrap <agent> --no-maintenance` 跳过本次自动整理和升级检查，不改变已有策略。
- **有界历史**：默认统一 1 GiB 预算、800 MiB 回落目标，计入归档、旧检查点、日志及受管备份/回收。启动与收尾限频检查，不自动删文件。`history status` 查容量，`history plan` 生成待审核清单；实际处理要求显式确认。受保护内容或备份空间不足时停止新增历史并报错，不绕过预算。保留期限在 `RETENTION.md` 配置，年龄只生成候选，不代表自动删除授权。
- **共享范围**：`memory/<agent>/` 和 `private/` 是组织约定，不是权限或加密边界。能访问这些文件的程序仍可能读取它们；加入的助手应当是你信任的。
- **模型与备份**：数据文件由 Agent Guild 保存在本机。助手读取后是否发送给模型服务，取决于该助手的运行方式；你选择的同步、备份工具也有自己的数据处理行为。

这些边界适用于 Agent Guild 本身；共享目录中的其他 skills / 工具有各自的权限和行为。
详见 [安全与能力说明](references/SECURITY.md)。

## 日常维护与升级

可以直接对已接入的助手说：“记住这个项目约定”“查一下上次的决定”“我有哪些待办”，再选择清单中的任务。新会话不会自动继续其他会话的工作。
完整命令见 [能力参考](references/CAPABILITIES.md)。CLI 的写入和检查都发生在调用时，不在后台运行。

检查、应用本项目的版本更新：

```bash
python3 "$HOME/.agent-guild/skills/agent-guild/scripts/ag.py" upgrade
python3 "$HOME/.agent-guild/skills/agent-guild/scripts/ag.py" upgrade --apply
```

Windows 使用 `python` 和 `$env:USERPROFILE` 对应路径。也可以重跑已检查的安装器。
新安装/更新路径绑定同一版本 tag 和资产名，优先校验 GitHub HTTPS release API 的
`digest = sha256:<64位十六进制>`；缺失时只接受同一 release 的同名 `.zip.sha256`，
且校验行必须指向目标 ZIP 的 basename。缺少校验依据、hash 不符或不安全 ZIP 均拒绝安装。
这是基于同一发布渠道的**完整性校验，不是签名，也不能抵御发布账号或渠道同时被攻破**。
解包拒绝路径逃逸、重复/大小写冲突、链接与压缩炸弹，展开总量上限 64 MiB。
交换失败会还原旧代码，最多保留一份 `.agent-guild.previous-code` 协议代码备份，
下一次经过校验的更新时轮换这份旧备份；它不是用户数据备份，不含身份、规则或任务材料。
`bash scripts/package.sh` 会在 ZIP 同目录生成完整 SHA-256 sidecar，上传 release 时需一起提供。
更新作用于 Agent Guild 自身的协议文件，不覆盖身份、规则和项目内容；链接安装随中央版本更新，
拷贝安装还需同步助手内的副本，见 [更新流程](references/ONBOARDING.md#step-7--update-protocol-how-to-stay-current-as-the-central-skill-evolves)。

## 文件结构与多设备

```text
~/.agent-guild/
├── identity/ rules/ projects/     用户身份、约定、项目状态
├── memory/shared/                跨助手的长期事实及 INDEX.md
├── memory/<agent>/               按助手组织的记忆
├── handoff/active/               未闭环任务包（元信息、快照、附件）
├── handoff/archive/              整包归档的已闭环任务
├── messages/inbox/ archive/      独立的 agent 间消息
├── log/ learnings/               会话日志、纠正与经验台账
├── hosts/<host-id>/              本机路径、平台和安装状态
├── skills/agent-guild/           Agent Guild 运行时 skill
├── RETENTION.md UPGRADE.md       保留与自动检查策略
└── registry.json                接入记录
```

完整共享中心还使用 `skills/`、`skills_data/`、`mcp/`、`plugins/`、`tools/`。
共享事实留在常规目录；只对一个 OS / 架构成立的工具用平台声明；只对本机成立的路径放在
`hosts/<host-id>/`。本机文件锁不能替代多设备文件同步的冲突处理。

搬迁时，用你选择的方式复制所需目录，在新设备执行 `init` 和 `port` 体检，再处理缺失的平台工具。
备份前检查包含的个人资料和凭据，不要把私人协会数据提交到公开仓库。
详见 [跨设备与备份](references/PORTABILITY.md)。

## 项目与文档

Agent Guild 是本地文件协议及其参考实现。它支持跨平台检测和多种链接降级方式；
实际能否加载 skill，取决于助手运行时的文件权限和扩展能力，接入时需要验证。

- [运行时 skill](SKILL.md) · [完整规范](references/SPEC.md) · [约定](references/CONVENTIONS.md)
- [接入流程](references/ONBOARDING.md) · [能力参考](references/CAPABILITIES.md) · [机器可读 manifest](manifest.json)
- [贡献接入指南](https://github.com/dqsjqian/agent-guild/blob/main/references/adapters/README.md)

许可证：[MIT](https://github.com/dqsjqian/agent-guild/blob/main/LICENSE)。作者：[@dqsjqian](https://github.com/dqsjqian)。
