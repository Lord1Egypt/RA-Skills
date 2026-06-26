---
name: free-model-router
description: 为 OpenClaw 提供免费模型智能路由服务，支持本地代理、自动配置、自动轮询、故障切换和配置零侵入。在需要设置免费模型路由、配置 Provider、切换模型或诊断模型可用性问题时使用。
---

# free-model-router

> 免费模型智能路由 — 本地代理,自动配置,自动轮询,故障切换,配置零侵入

引导注册免费模型,永久在线,实现token自由。自动同步、自动检测、自动切换、自动救援。

## 数据流向说明

本技能的数据流向分为三层，所有行为均透明可控：

```
Layer 1: 用户 → OpenClaw → 127.0.0.1:5678 本地 Router
         （数据不离开本机）

Layer 2: 本地 Router → 外部模型 Provider（OpenRouter、NVIDIA NIM 等）
         （提示词和模型响应经过 Provider 服务器）

Layer 3: 本地 Router ↔ freemodel 控制服务器
         （仅同步 provider 列表、模型 ID、健康状态，不含对话内容）
```

| 行为 | 说明 | 用户控制 |
|------|------|----------|
| **外部通信** | 向 `freemodel.eu.org` 等服务器注册匿名 API Key、拉取 provider 列表和模型元数据 | 仅同步 provider 配置，**不含任何用户对话内容** |
| **数据上报** | 可选的匿名健康状态上报（模型延迟、可用性） | **默认关闭**，可随时通过 `reporting off` 命令或管理面板开启/关闭 |
| **设备指纹** | SHA256(hostname + homedir + platform + arch) 不可逆哈希 | 仅用于区分设备，**无法反推原始信息** |
| **配置修改** | 仅在 setup 时向 `openclaw.json` 添加 free-model-router provider | 自动备份（最多3份）+ 失败自动回滚，幂等设计 |
| **本地代理** | `127.0.0.1:5678` 仅监听本地回环 | **不暴露公网**，仅接收 OpenClaw 内部请求 |
| **推荐码** | 完全自愿的推荐试用系统 | 不参与不影响任何免费功能 |

> **重要提示**：你的提示词和模型响应会被转发到外部模型 Provider（如 OpenRouter、NVIDIA NIM 等），请知悉。本技能不收集、不传输、不存储任何用户对话内容、提示词或模型响应数据。所有外部请求仅涉及模型配置元数据。

## 核心架构

- **OpenClaw 配置只改一次** — 仅在 setup 时写入 `free-model-router` provider 指向本地 Router (127.0.0.1:5678)
- **所有模型切换在 Router 层透明完成** — 运行期间不再触碰 openclaw.json,避免 Gateway 宕机
- **Round-Robin 轮询** — 默认策略在各 provider 主模型间轮询
- **自动故障切换** — 主模型故障自动切换到备模型,所有 provider 不可用时自动降级
- **事件通知系统** — 模型切换、故障等事件写入 events.json,由 cron 任务推送

## 安装幂等性

**本技能支持幂等安装 — 多次触发 setup 不会产生副作用。**

详见 [references/idempotency.md](references/idempotency.md)

核心要点:
- Router 已运行则跳过,OpenClaw 已配置则跳过
- 重复执行时仅同步 provider 列表,**不会覆盖用户手动设置的主备模型**
- 用户手动配置的 API Key 和主模型值始终保留

## ⚠️ 版本更新后必须重启 Router

**Skill 更新只会替换磁盘文件，不会自动重启正在运行的 Router 进程。** 旧进程仍在使用旧代码，新功能/修复不会生效。

**必须在 skill 更新后执行以下操作：**

```bash
# 1. 停止旧进程
node <skill_dir>/scripts/free-model-cli.js stop

# 2. 重新启动（setup 会自动启动 Router 并完成初始化）
node <skill_dir>/scripts/free-model-cli.js setup
```

> **注意：** `stop` + `setup` 是安全的——Router 配置、API Key、主备模型等用户数据均持久化在 `~/.free-model-router/data/router-config.json` 中，重启不会丢失。

## 配置流程触发

安装/识别技能后,向用户展示:

**选项 A:现在设置(推荐)** — 回复 "现在设置"/"开始配置"
**选项 B:延后设置** — 回复 "延后设置"/"稍后再说"

配置完成后,Router 注册两个定时任务(北京时间 UTC+8):
- **事件通知检查**: 每天 10:00、15:00、20:00 检查一次(避免夜间打扰)
- **每日状态汇报**: 每天 9:00 自动汇报各 provider 运行状态

> **注意:** 如果已安装(Router 运行 + OpenClaw 已配置),setup 命令会输出当前状态摘要而非重新配置。

> **CLI 路径:** 下文所有命令中的 `<skill_dir>` 指技能安装目录。默认路径为 `~/.openclaw/skills/free-model-router`，具体路径取决于当前 OpenClaw 变种的安装目录和技能名称（例如 `~/.kimi-openclaw/skills/free-model-router`）。

## 命令执行约束

**禁止复合命令:** OpenClaw 的 exec 工具不支持 `cd ... && node ...` 或 `bash -c "..."` 等复合命令。所有命令必须使用直接调用格式:

```bash
node <skill_dir>/scripts/free-model-cli.js <command>
```

其中 `<skill_dir>` 的完整路径取决于当前 OpenClaw 变种的安装目录（例如 `~/.openclaw/skills/free-model-router` 或 `~/.kimi-openclaw/skills/free-model-router`）。如需切换目录,应使用 OpenClaw 的 `workingDirectory` 参数指定,而不是在命令中使用 `cd &&`。

## 常用命令

查看完整命令列表:
```bash
node <skill_dir>/scripts/free-model-cli.js help
```

## 意图匹配

| 用户说 | 动作 |
|--------|------|
| `/free-model-router setup`、"开始配置"、"安装免费模型路由" | Setup 流程 |
| `/free-model-router`、`/free-model-router status` | 运行 providers 查看状态 |
| `/free-model-router providers`、"有哪些免费模型provider" | 运行 providers |
| `/free-model-router models`、"有哪些免费模型" | 运行 models |
| `/free-model-router models xxx`、"xxx 有哪些模型" | 运行 models xxx |
| `/free-model-router providerApiKey xxx yyy` | 设置 provider API Key |
| `/free-model-router switchProviderPrimaryModel xxx yyy`、"换成 yyy" | 切换主模型 |
| `/free-model-router disableProvider xxx`、"禁用 xxx" | 禁用 provider |
| `/free-model-router enableProvider xxx`、"启用 xxx" | 启用 provider |
| `/free-model-router configureModelRole primary`、"设为主模型"、"作为主模型" | 设为 OpenClaw 主模型 |
| `/free-model-router configureModelRole fallback`、"设为备用模型"、"作为备用模型" | 设为 OpenClaw 备用模型 |
| `/free-model-router stop`、"停止 Router" | 停止 Router 进程 |
| `/free-model-router uninstall`、"卸载技能" | 卸载 free-model-router |
| "openclaw 挂了"、"模型不可用" | 检查 provider 状态 → 诊断 → 引导修复 |

## 意图识别规则

### 1. 用户主动切换模型

用户说 "换成/切换到/换用 + 模型名" → 解析后在已配置 Provider 中查找并调用 switchProviderPrimaryModel

**歧义处理:**
- 用户提供了完整模型 ID(如 `qwen/qwen3-coder:free`) → 直接切换
- 用户只说了模型名(如 "qwen3-coder") → 在已配置 Provider 中查找匹配:
  - 仅一个 Provider 有 → 自动使用该 Provider 的完整 ID
  - 多个 Provider 都有 → 请用户确认使用哪个 Provider
  - 找不到匹配 → 提示用户输入完整 ID 或先运行 models 查看
- 用户未指定 Provider → 先运行 models 列出各 Provider 的主模型,请用户确认

### 2. 用户引导配置(首次)

触发 Setup 流程逐步引导,详见 [references/setup-guide.md](references/setup-guide.md)

### 3. 兜底机制

openclaw 无法回复时:1) 检查 Router 状态 → 2) 检查各 provider 状态 → 3) 如有故障切换,汇报结果

## Setup 流程

> **核心原则:** 多 Provider 优于单 Provider。引导用户尽可能提供多个 Key。

完整 6 步流程详见 [references/setup-guide.md](references/setup-guide.md)

**流程概览:**
1. 运行 `setup` 命令 — 启动 Router + 初始化 + OpenClaw 配置
2. 注册定时任务 — 事件检查(北京时间 08:00~22:00 每30分钟) + 每日状态汇报(北京时间每天9:00)
3. 展示 Provider 列表,引导设置 API Key
4. [重要]主动询问用户将free-model-router设为主模型还是备用模型，否则技能将不会生效
5. 展示各 Provider 主备模型,可选择切换
6. 完成配置

## 事件通知系统

Router 内置事件通知系统,自动推送模型切换、故障等事件。

详见 [references/event-system.md](references/event-system.md)

**核心机制:**
- 事件状态: `pending`(待推送) → `notified`(已推送) → `read`(已读)
- Cron 在北京时间 08:00~22:00 期间每 30 分钟读取 `status=pending` 且 `shouldNotify=true` 的事件
- 推送后调用 `mark-notified` 标记,避免重复推送
- **无事件时保持静默**: 如果没有待推送事件,Cron 不会向用户发送任何消息

**公告事件超链接:**
- 公告事件可能包含 `metadata.url` 链接
- 推送时使用 Markdown 格式展示: `[🔗 {action}]({url})`
- 详见 [event-system.md 公告格式](references/event-system.md#公告事件格式)

## 停止与卸载

### 停止 Router

```bash
node <skill_dir>/scripts/free-model-cli.js stop
```

- 读取 PID 文件并发送 SIGTERM 信号
- 自动清理 PID 文件
- 如果 Router 未运行，输出提示信息

### 卸载

```bash
node <skill_dir>/scripts/free-model-cli.js uninstall
```

- 自动停止 Router 进程
- 移除 OpenClaw 配置中的 free-model-router provider
- 卸载后请在 OpenClaw 技能管理界面中移除 free-model-router 技能以清理 cron 任务

## 注意事项

1. **API Key 安全:** 仅存本地 router-config.json,不发送到外部
2. **模型可用性:** 免费模型随时可能下架/收费
3. **配置安全:** 所有修改自动备份,失败自动回滚
4. **配置零侵入:** OpenClaw 配置仅在 setup 和配置模型角色时修改,运行期间不再触碰

## 📚 参考文档

| 文档 | 内容 |
|------|------|
| [references/setup-guide.md](references/setup-guide.md) | Setup 完整 6 步流程 |
| [references/event-system.md](references/event-system.md) | 事件通知系统详解 |
| [references/idempotency.md](references/idempotency.md) | 安装幂等性说明 |
