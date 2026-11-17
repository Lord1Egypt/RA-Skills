---
name: cron-callback-session
description: "实现『用 A 会话调起/注入 B 会话』的能力（sessions_send）：cron 任务、外部进程或另一会话可向目标会话注入消息，唤醒其 agent 带完整上下文继续推进。适用于 OpenClaw 与 QClaw（同内核）。含 Windows 下 visibility 配置检查/修复、正确重启网关（SIGUSR1 bug 规避）、cron job 设计。当用户要求「定时任务完成后回到本对话继续推进」「cron 回调当前会话」「让任务结果上报到同一对话」时使用。"
version: 1.0.6
---

# Cron 回调本会话（cron-callback-session）

让一次性/周期 cron job 执行完毕后，把结果通过 `sessions_send` 注入**当前对话**，使 agent 基于原上下文继续推进任务。

## 适用平台

- **OpenClaw**（原生）：使用 `sessions_send` / cron 机制，本 skill 的配置与命令直接适用
- **QClaw**（桌面客户端/界面）：基于 OpenClaw 内核，同一套配置体系（`openclaw.json` + `sessions_send` + cron），本 skill 完全适用；QClaw 只是界面层，不改变底层机制
- 配置路径不硬编码：无论 OpenClaw 还是 QClaw，都用 `openclaw config file` 自动发现（见第一步）

## 本质能力

本 skill 实现的是**"一个会话调起/注入另一个会话"**：A 会话（或外部进程 / cron job）通过 `sessions_send` 向 B 会话注入消息，B 的 agent 带着完整上下文被唤醒并继续处理。cron 回调当前对话只是最常见的应用形态，不是唯一用法。

**非 cron 用法举例**：
- 另一个会话处理完长任务后，把结果回传到主会话继续汇总
- 外部脚本/进程在特定时机向指定会话注入提示，触发其 agent 执行
- 监控/看门狗类任务发现异常时，向主对话注入警报并让 agent 介入处理

## 背景（为什么需要这个 skill）

- 默认 `cron sessionTarget=isolated` 会在**独立会话**运行，任务结果上报到新对话，原对话不推进
- 要让结果回到原对话，需 cron 会话用 `sessions_send` 发消息到当前对话
- 但 `tools.sessions.visibility` 默认 `tree`（只允许同一会话树内发送），cron isolated 会话不在树内 → forbidden
- **重启可能重置网关配置**（visibility 弹回默认 tree），所以每次用前必须先自查

## ⚠️ 风险警告（使用前必读）

本 skill 涉及两项需要谨慎的操作：

1. **杀进程重启网关**（第三步）：`Stop-Process` 强制终止 gateway 进程会**中断所有活跃会话、cron 任务及其他进行中的工作**，可能导致服务中断或运营状态丢失。请：
   - 在维护窗口执行，或先确认当前没有重要任务在运行
   - 执行前先完成第二步的配置备份
   - 杀进程后依赖守护机制自动拉起，若未自动拉起需手动 `openclaw gateway run` 恢复

2. **放宽会话路由权限**（第二步）：`tools.sessions.visibility = agent` 会让当前 agent 下任意会话可互相发送消息，权限比默认 `tree` 更宽。请：
   - 仅在确实需要跨会话注入时开启
   - 使用完毕后，如不再需要跨会话消息，建议恢复默认 `tree`（同样手动编辑配置文件）

## 流程

### 第一步：检查当前会话与配置

1. 获取当前会话 key：
   ```
   session_status (sessionKey="current")
   ```
   记下 `Session:` 行，形如 `agent:main:session-xxxxxxxxxxxx-xxxxxx`

2. 发现配置文件路径（不要硬编码，OpenClaw 可能装在任意目录）：
   ```bash
   openclaw config file
   ```
   输出最后一行即配置文件绝对路径（前面可能有 bootstrap 日志/doctor 警告等噪音，取最后一行）。

3. 用该路径读取 visibility：
   ```powershell
   $cfgPath = (openclaw config file | Select-Object -Last 1)
   $c = Get-Content -Raw $cfgPath -Encoding UTF8 | ConvertFrom-Json
   $c.tools.sessions.visibility   # 期望输出: agent
   ```

4. 确认网关进程是否加载了新配置（验证方法见第三步"验证"）

### 第二步：配置检查与修复

**目标值：`tools.sessions.visibility = agent`**（当前 agentId 下任意会话可见；跨 agent 需额外 `tools.agentToAgent`）

| 当前值 | 处理 |
|--------|------|
| `agent` | ✅ 无需修改，跳到第三步 |
| 缺失 / `tree` / `self` | 手动编辑配置文件（见下） |
| `all` | ✅ 可用但权限过大，建议收敛到 `agent` |

**修改配置（gateway 工具的 config.patch 会拒绝此路径，必须手动编辑文件）：**

先拿到配置文件路径（同第一步）：
```bash
openclaw config file   # 取最后一行，即当前实际生效的配置文件绝对路径（默认 ~/.openclaw/openclaw.json，发行版可能不同，以此命令输出为准）
```

```powershell
$cfgPath = (openclaw config file | Select-Object -Last 1)
# 1. 备份
Copy-Item $cfgPath "$cfgPath.bak-<yyyyMMdd>" -Force
# 2. 在 "tools" 段内插入 sessions 子段（若 tools.sessions 不存在）
#    "tools": {
#      "sessions": { "visibility": "agent" },
#      ...
#    }
# 3. 验证 JSON 合法
$null = Get-Content -Raw $cfgPath -Encoding UTF8 | ConvertFrom-Json; "JSON_VALID"
```

### 第三步：Windows 下正确重启网关（关键！）

> ⚠️ **Windows 上 `gateway restart` 是坏的**：
> `openclaw gateway restart` 报 `TypeError [ERR_UNKNOWN_SIGNAL]: Unknown signal: SIGUSR1`
> Windows Node.js 不支持 SIGUSR1 信号 → in-process restart 永远失败 → 返回 ok 但进程没重启 → 配置改了不生效。
> gateway 工具 restart 同理（内部走 SIGUSR1）。

**正确姿势（2026-08-05 实测验证）：杀旧进程 + 立刻手动拉起新进程**

> ⚠️ 实测结论：**不能依赖守护机制自动拉起**。当 QClaw 桌面客户端未运行时，网关进程是独立运行的（无父进程守护），`Stop-Process` 杀掉后**没有东西会自动拉起它**，这就是"杀掉直接起不来"的根因。必须手动启动新进程。

> ⚠️⚠️ **执行前必读（2026-08-05 实测）：**
> 1. **重启网关会断开 webchat 连接，agent 不会自己醒来**——执行完杀旧+起新后，当前对话会静默，**必须由用户手动输入一条消息（如"怎么样了"）才能唤起 agent**。agent 应在执行重启步骤前**明确告知用户**这一点，避免用户以为卡死。
> 2. **不要重启 QClaw 桌面客户端**——QClaw 重启会重新加载配置并可能把 `tools.sessions.visibility` 重置回默认 `tree`，之前改的配置就白改了。只重启网关进程本身（下面的命令），不要动 QClaw.exe。
> 3. 执行此步骤前，先告知用户"接下来需要重启网关，完成后请发一条消息唤醒我"，再动手。

```powershell
# 0. 准备：网关端口和启动命令
$node = "<发行版>\resources\node\node.exe"          # 从 qclaw.json cli.nodeBinary 或当前进程 Path 获取
$mjs  = "<发行版>\resources\openclaw\node_modules\openclaw\openclaw.mjs"
$port = <网关端口>                                    # 从 openclaw.json gateway.port 获取

# 1. 找到网关进程（通常两个 node 进程，命令行含 "openclaw-gateway"）
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match "openclaw-gateway" } | Select-Object ProcessId, CreationDate

# 2. 杀旧进程
# ⚠️ 此操作会中断所有活跃会话/定时任务/进行中的工作，确认无重要任务再执行
Stop-Process -Id <PID1>, <PID2> -Force
Start-Sleep -Seconds 3   # 等待端口释放

# 3. 立刻手动启动新进程（后台独立，与旧进程相同参数）
Start-Process -FilePath $node -ArgumentList "--title=openclaw-gateway","--no-warnings","--max-semi-space-size=128","--max-old-space-size=4096",$mjs,"gateway","run","--port","$port" -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 5

# 4. 验证：新进程监听端口 + HTTP 连通
netstat -ano | Select-String ":$port.*LISTENING"
# 用网关认证值（从 openclaw.json 的 gateway.auth 段读取）请求 /v1/models，返回 model 列表 = 网关正常
# 同时确认当前对话能继续收发（session 自动接续）
```

**关键点：**
- **不要**先启新进程再杀旧的——新进程会因端口被占而启动失败（报 `gateway already running (pid xxx); lock timeout after 5000ms`）
- 启动命令参数必须与旧进程一致（`--title=openclaw-gateway` 等），否则 QClaw 客户端可能识别不到
- 网关认证值从 `openclaw.json` 的 `gateway.auth` 段读取（该段配置项名含敏感词，此处不展开）
- 若 QClaw 桌面客户端在运行，它可能自行管理网关进程，此时杀进程后客户端会自动拉起（观察 1-3 分钟再手动介入）；**但不要重启 QClaw.exe 本身**（会重置配置）
- **重启后当前对话会静默**（webchat 连接断开，agent 不会自动醒来）——告诉用户发一条消息唤起

**验证配置已加载：**
```powershell
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -match "openclaw-gateway" } | Select-Object ProcessId, CreationDate
# 新进程 CreationDate 应为最近时间（而非旧日期）
```

> 若手动启动失败（端口未释放/参数错误），等端口释放后重试：`openclaw gateway run --port <port>`（前台，便于看日志）。

### 第四步：设计 cron job 并回调本会话

**一次性任务（X 分钟后）：**

```json
{
  "action": "add",
  "job": {
    "name": "<任务名>",
    "agentId": "<当前agentId>",
    "schedule": { "kind": "at", "at": "<now+1min ISO+08:00>" },
    "sessionTarget": "isolated",
    "payload": {
      "kind": "agentTurn",
      "message": "请调用 sessions_send 工具，target 填 '<当前会话key>'，发送内容：'<要注入的消息>'。要求：(1) 只调用 sessions_send 发送 (2) 不要调用 message 工具 (3) 不要输出 HEARTBEAT_OK (4) 若失败如实报告错误"
    },
    "delivery": { "mode": "none" },
    "deleteAfterRun": true
  }
}
```

**关键参数：**
- `sessionTarget: "isolated"` — cron 在独立会话运行（不需要绑定当前会话；绑定反而可能因树限制失败）
- `payload.message` 里明确写 `sessions_send` + 完整 target（`agent:main:session-xxx`）
- `delivery.mode: "none"` — 结果不投递到渠道，只通过 sessions_send 注入目标对话
- 时间格式：`yyyy-MM-ddTHH:mm:ss+08:00`（本地时区，勿用 UTC）

### 第五步：验证回调

1. 到约定时间后，检查目标对话是否收到注入消息（消息会以 inter-session message 形式出现）
2. 查看运行记录：
   ```
   cron (action="runs", jobId="<jobId>")
   ```
3. 注意：运行记录 `status=error`（如 "isolated agent setup timed out"）**不代表发送失败**——消息可能已送达，只是任务状态判定超时。以目标对话是否收到消息为准。

## 忙时队列行为（重要）

`sessionTarget=isolated` 的 cron 会话调用 `sessions_send` 时，消息经过**内部消息队列**投递：

- **目标会话空闲**：消息立即投递，注入方很快收到 `accepted`
- **目标会话忙**（正在处理其他回合/长任务）：消息**挂起等待**，不丢不打断；待目标会话空闲后逐条投递
- **一个空闲窗口可能只投递一条**，多条注入按序逐条到达（实测间隔 3-5 分钟）

> ⚠️ **`gateway timeout` 是误报，不是发送失败**：
> 当目标会话忙时，注入方的 `sessions_send` 调用可能返回 `gateway timeout after 10000ms`（10s 工具调用超时）。**这代表消息已入队、投递挂起，不代表发送失败。**
> **不要据此重发**——消息最终会到达，重发会造成**重复注入**（同一内容出现多次）。
>
> 注入延迟取决于目标会话的空闲节奏，实测可达 20+ 分钟。若需确认消息是否送达，以目标会话实际收到的 inter-session message 为准，而非调用返回值。

## 常见问题

- **CLI 建 job 传中文参数会乱码**（PowerShell 编码问题）——用英文 job 名，中文内容走 cron 工具 API 而非 CLI
- **`forbidden: Session send visibility is restricted to the current session tree`** → 配置不是 `agent`，回到第二步
- **改了配置但 cron 仍报 forbidden** → 网关没真正重启（SIGUSR1 bug），回到第三步杀进程重启
- **想跨 agent 发送** → 需 `tools.agentToAgent`，且 visibility=`all`（风险高，慎用）。实测（2026-08-05）：`visibility=all` + `agentToAgent.enabled=true`（allow `*`）下，cron isolated 会话可跨 agent 注入任意会话（如 `agent:op-xxx:session-xxx`），目标 agent 收到后可用 `sessions_send` 回传；回传若遇 `gateway timeout` 同为忙时挂起误报，消息会入队稍后到达。注意：回传给 cron 临时会话（`agent:main:cron:...:run:xxx`）可能因该会话已删除而失败，应回传给持久会话（如 `agent:main:session-xxx`）
- **`gateway config.patch` 报 "cannot change protected config paths"** → 正常，此路径是内置保护，只能手动编辑文件

## 参考

- 完整实验记录：workspace 下《同会话上报实验归档_<日期>.md》
- 忙时队列行为实测记录：workspace 下 memory/2026-08-03.md（A/B/C 三注入实测，timeout 误报验证）
- 配置备份：openclaw.json.bak-<yyyyMMdd>（修改配置前自动生成）

## 反馈

发现 bug 或有改进建议？请开 [GitHub Issue](https://github.com/onesfuture/cron-callback-session/issues)。
