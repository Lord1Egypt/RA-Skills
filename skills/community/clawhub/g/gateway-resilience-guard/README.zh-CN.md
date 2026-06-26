# OpenClaw Gateway Resilience Guard

OpenClaw Gateway 外部恢复守护脚本，面向 `openclaw-weixin` 这类需要长期在线的通道。

这个项目解决的是一个很具体的运维问题：OpenClaw Gateway 进程还活着，但通道、长轮询、WSL/系统网络或 session 状态已经坏掉，导致消息收不到、发不出，最后只能手动 `openclaw gateway restart`。

## 问题背景

OpenClaw Gateway 和通道插件是长连接系统。电脑睡眠、切换 Wi-Fi、WSL 网络重建、iLink 长时间空闲、配置热加载，都可能让“进程存活”和“通道可用”变成两件事。

以官方 `Tencent/openclaw-weixin` 为例，源码和 issue 里能看到几个已知边界：

- `monitor.ts` 里 `MAX_CONSECUTIVE_FAILURES = 3`，失败后 `BACKOFF_DELAY_MS = 30_000`，也就是插件内部主要是 3 次失败后的 30 秒退避。
- `session-guard.ts` 里 `SESSION_PAUSE_DURATION_MS = 60 * 60 * 1000`，`SESSION_EXPIRED_ERRCODE = -14`，session 过期会进入 60 分钟暂停窗口。
- [Tencent/openclaw-weixin#141](https://github.com/Tencent/openclaw-weixin/issues/141) 记录了配置热加载后 Monitor 结束但不再启动，临时处理方式是手动重启 gateway。
- [Tencent/openclaw-weixin#155](https://github.com/Tencent/openclaw-weixin/issues/155) 记录了 `errcode=-14` 后进入 60 分钟循环暂停、出站消息被阻塞的问题。

所以这个项目不是替换官方插件，而是在外面加一层独立 watchdog：当通道或 gateway 进入“看起来还活着，实际上已经不能工作”的状态时，用更保守的探测和熔断策略自动恢复。

## 工作原理

看门狗使用分层健康检查，从浅到深判断是否真的需要重启：

| 层级 | 检查对象 | 作用 |
| --- | --- | --- |
| Gateway 本机状态 | `openclaw gateway status --json --require-rpc`、本机 health URL、本机 TCP 端口、服务/进程兜底 | 判断 OpenClaw Gateway 是否已经挂掉或本机不可达。 |
| 通道状态 | `openclaw health --json --verbose`、`openclaw status --deep`、可选 `openclaw channels status --probe`，最后才是 URL 兜底 | 优先使用 OpenClaw 自己的全通道健康模型；CLI 不支持时再退回 URL 探测。 |
| 运行时诊断 | `openclaw models status --json`、`openclaw logs --plain`、WARN/ERROR 分类 | 在动作前区分 provider、代理/网络、鉴权/限流、gateway、通道 session、配置热加载和任务运行时证据。 |
| 模型 API，可选 | 使用 `openclaw agent --json` 走 OpenClaw 当前配置的模型 provider | 判断 Gateway 和通道都健康时，真正卡住的是不是模型 API 链路。默认关闭，因为它会真实消耗模型调用。 |
| 外部网络状态 | 百度、QQ、微信 API 等多个独立 URL | 排除全局断网，避免电脑没网时误重启 gateway。 |

核心策略是：gateway 真挂了就立即重启；通道不通时先确认不是全局断网；网络正常但通道持续失败，才进入退避等待和重启流程。
模型探针默认只记录证据日志；如果你显式配置，也可以在连续失败后重启 gateway 或执行自定义命令。

## 恢复策略

- Gateway 本机健康检查失败：立即重启。
- 通道 URL 失败：累计失败次数，进入故障流程。
- 外部网络全部失败：认为是全局断网，只等待，不重启。
- 外部网络正常但通道仍失败：指数退避后再次确认，再重启 gateway。
- OpenClaw 日志出现 WARN/ERROR：先分类和记录证据，默认只写日志。
- 连续 5 次通道探测成功后，清空失败状态。
- 每小时最多重启固定次数，防止网络抖动时形成重启风暴。
- 深夜可以降低检查频率，减少无意义日志。

## 文件说明

| 文件 | 作用 |
| --- | --- |
| `gateway-watchdog.sh` | 主守护脚本，负责探测、退避、熔断、日志、单实例锁和重启决策。 |
| `gateway-watchdog.ps1` | Windows 原生守护脚本，用于 Task Scheduler。 |
| `dashboard/` | 独立本地 Web UI 和 API，由 watchdog 自己提供，不依赖 Gateway。 |
| `openclaw-plugin/` | 可选 OpenClaw 原生插件桥接入口，把 `/resilience-guard` 跳转到独立 dashboard。 |
| `install-watchdog.sh` | Linux/WSL/macOS 安装脚本，自动复制文件、生成配置、创建 systemd 用户服务或 macOS LaunchAgent。 |
| `install-watchdog.ps1` | Windows 安装脚本，创建配置和计划任务。 |
| `uninstall-watchdog.sh` | 卸载脚本，停止服务并删除安装目录。 |
| `uninstall-watchdog.ps1` | Windows 卸载脚本。 |
| `SKILL.md` | ClawHub/OpenClaw 技能元数据和使用说明。 |
| `README.md` | 英文文档。 |

## 安装

通过 ClawHub 安装：

```bash
clawhub install gateway-resilience-guard
```

也可以直接使用本仓库。

Linux、WSL 或 macOS：

```bash
bash install-watchdog.sh
```

无人值守安装：

```bash
bash install-watchdog.sh --yes
```

指定自己的通道探测地址：

```bash
bash install-watchdog.sh --channel-url "https://你的通道地址/health"
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File .\install-watchdog.ps1
```

## 图形化 Dashboard

安装后会启用一个独立本地 dashboard：

```text
http://127.0.0.1:18790/
```

这个页面由 watchdog 自己提供，不依赖 OpenClaw Gateway。所以 Gateway 挂掉时，它仍然可以打开，看到最后一次诊断证据。

它包含：

- Gateway、通道、外部网络、OpenClaw 日志、模型 provider 的分层状态。
- provider timeout、代理/网络、限流、鉴权、通道 session、Gateway degraded、配置热加载、任务运行时异常的分类图表。
- 侧边栏分页：总览、趋势、策略、日志、配置分开呈现，避免把监控、操作和明细堆在一个长页面里。
- 本地设计系统控件：下拉框、按钮、状态标签使用原生语义控件加统一样式，不依赖 CDN 或组件脚本升级。
- 重新分配每页信息密度：趋势页有摘要和最新信号，策略页有策略矩阵和手动操作，配置页有运行地图。
- 事件趋势图，把 API 失败、日志 WARN、模型探针成功、健康诊断分成不同泳道，并保留清晰的时间刻度。
- 中英文语言切换，以及 Light、Dark、Ocean、Forest 四套主题。
- 状态文件新鲜度，避免把过期快照误认为当前状态。
- 快速策略按钮：观察模式、夜间诊断、通道恢复、保守熔断。
- 带解锁流程的受保护操作：立即诊断、重启 Gateway、应用策略、导出诊断 JSON。

Dashboard 操作只绑定 localhost，并使用安装时生成的 `DASHBOARD_TOKEN` 保护。token 只注入同源页面，不会写入日志。

可选 OpenClaw 插件桥接入口：

```bash
openclaw plugins install ./openclaw-plugin
openclaw plugins enable resilience-guard
openclaw gateway restart
```

Gateway 正常时可以打开：

```text
http://127.0.0.1:18789/resilience-guard
```

这个路由会跳转到外部 dashboard。它只是方便入口；真正救急的入口仍然是 `http://127.0.0.1:18790/`。

安装后会生成：

- 脚本目录：`~/.local/share/openclaw-gateway-watchdog`
- 配置文件：`~/.config/openclaw-gateway-watchdog/watchdog.env`
- 日志文件：`~/.local/state/openclaw-gateway-watchdog/watchdog.log`
- Linux/WSL systemd 用户服务：`~/.config/systemd/user/gateway-watchdog.service`
- macOS LaunchAgent：`~/Library/LaunchAgents/ai.clawhub.gateway-resilience-guard.plist`
- Windows 计划任务：`OpenClaw Gateway Resilience Guard`

如果当前环境没有 user systemd，安装脚本会退回到后台进程模式，并把 pid 写到状态目录。

## 管理命令

```bash
systemctl --user status gateway-watchdog
journalctl --user -u gateway-watchdog -f
systemctl --user restart gateway-watchdog
bash ~/.local/share/openclaw-gateway-watchdog/uninstall-watchdog.sh
```

macOS：

```bash
launchctl print gui/$(id -u)/ai.clawhub.gateway-resilience-guard
tail -f ~/.local/state/openclaw-gateway-watchdog/watchdog.log
bash ~/.local/share/openclaw-gateway-watchdog/uninstall-watchdog.sh
```

Windows：

```powershell
Get-ScheduledTask -TaskName "OpenClaw Gateway Resilience Guard"
Get-Content "$env:LOCALAPPDATA\openclaw-gateway-watchdog\watchdog.log" -Wait
powershell -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\openclaw-gateway-watchdog\uninstall-watchdog.ps1"
```

连配置和日志一起删除：

```bash
bash ~/.local/share/openclaw-gateway-watchdog/uninstall-watchdog.sh --purge
```

## 配置

普通用户一般不用改。高级配置在：

```text
~/.config/openclaw-gateway-watchdog/watchdog.env
```

常用项：

```bash
GATEWAY_SERVICE="openclaw-gateway"
GATEWAY_HEALTH_URL="http://127.0.0.1:18789/healthz"
GATEWAY_HOST="127.0.0.1"
GATEWAY_PORT="18789"
CHANNEL_URL="https://ilinkai.weixin.qq.com"
NETWORK_URLS="https://www.baidu.com https://www.qq.com https://api.weixin.qq.com"
RESTART_COMMAND="systemctl --user restart openclaw-gateway"
OPENCLAW_NATIVE_PROBES="auto"
OPENCLAW_HEALTH_TIMEOUT_MS="12000"
OPENCLAW_GATEWAY_STRICT="0"
OPENCLAW_CHANNELS_PROBE="1"
OPENCLAW_DIAG_ENABLED="1"
OPENCLAW_DIAG_INTERVAL="300"
OPENCLAW_LOG_SCAN_ENABLED="1"
OPENCLAW_LOG_LIMIT="200"
OPENCLAW_LOG_SIGNAL_LIMIT="40"
OPENCLAW_LOG_TIMEOUT_MS="15000"
OPENCLAW_LOG_WARN_PATTERNS="fetch failed|fetch timeout|LLM idle timeout|model silent|..."
OPENCLAW_DIAG_ACTION="log"
OPENCLAW_DIAG_FAILURES_BEFORE_ACTION="2"
OPENCLAW_DIAG_COMMAND=""
DASHBOARD_ENABLED="1"
DASHBOARD_HOST="127.0.0.1"
DASHBOARD_PORT="18790"
DASHBOARD_ACTIONS_ENABLED="1"
DASHBOARD_TOKEN="安装时生成"
DASHBOARD_DIR="~/.local/share/openclaw-gateway-watchdog/dashboard"
MODEL_PROBE_ENABLED="0"
MODEL_EDGE_PROBE_ENABLED="1"
MODEL_PROBE_INTERVAL="1800"
MODEL_PROBE_TIMEOUT="120"
MODEL_PROBE_FAILURES_BEFORE_ACTION="2"
MODEL_PROBE_ACTION="log"
MODEL_PROBE_COMMAND=""
MODEL_PROBE_MODEL=""
MODEL_PROBE_THINKING="off"
MODEL_PROBE_SESSION_ID="watchdog-model-probe"
MODEL_PROBE_MESSAGE="Reply with exactly OK."
BASE_INTERVAL="60"
NIGHT_INTERVAL="300"
MAX_INTERVAL="1800"
CHANNEL_FAILURES_BEFORE_RESTART="2"
SUCCESS_COUNT_TO_RESET="5"
MAX_RESTARTS_PER_HOUR="6"
```

如果你的 OpenClaw 不是 systemd 用户服务管理，可以显式指定重启命令：

```bash
RESTART_COMMAND="openclaw gateway restart"
```

Windows 的配置是 JSON：

```text
%APPDATA%\openclaw-gateway-watchdog\watchdog.json
```

如果你的 OpenClaw CLI 版本太旧，不支持 `openclaw health` 或 `openclaw status --deep`，可以把 `OpenClawNativeProbes` 设为 `false`。

### OpenClaw 诊断和日志信号

这个 watchdog 不只是 ping 一个 URL。它会每隔 `OPENCLAW_DIAG_INTERVAL` 秒采集一组 OpenClaw 运行快照：

```text
~/.local/state/openclaw-gateway-watchdog/last-openclaw-gateway-status.json
~/.local/state/openclaw-gateway-watchdog/last-openclaw-health.json
~/.local/state/openclaw-gateway-watchdog/last-openclaw-model-status.json
~/.local/state/openclaw-gateway-watchdog/last-openclaw-status-deep.txt
~/.local/state/openclaw-gateway-watchdog/last-openclaw-logs.txt
~/.local/state/openclaw-gateway-watchdog/last-openclaw-log-signals.txt
~/.local/state/openclaw-gateway-watchdog/last-openclaw-log-signal-categories.txt
~/.local/state/openclaw-gateway-watchdog/last-openclaw-diagnostics.jsonl
```

`last-openclaw-log-signals.txt` 来自 `openclaw logs --plain` 的过滤结果，会把常见异常归类成 `provider_timeout`、`proxy_or_network`、`provider_rate_limit`、`provider_auth`、`abort_stuck`、`memory_dream_timeout`、`channel_session`、`gateway_degraded`、`config_reload`、`task_runtime` 等类别。

默认策略是 `OPENCLAW_DIAG_ACTION="log"`，因为 WARN 是证据，不一定等于“应该马上重启”。如果你显式改成 `restart` 或 `command`，也必须连续多次出现诊断异常，并且外部网络探测正常，才会执行动作。

排查时可以这样判断：

| 证据 | 更可能的问题范围 | 默认策略 |
| --- | --- | --- |
| Gateway status/health 挂了 | Gateway 进程或 RPC 链路 | 走原本的 Gateway 策略，立即重启。 |
| 通道探测失败，但外部网络正常 | 通道或 session 链路 | 退避、复查，仍失败再重启 Gateway。 |
| OpenClaw 日志显示 provider timeout，模型探针也失败 | 模型 provider/API 链路 | 先记录证据；可选自定义动作。单纯重启 Gateway 未必有用。 |
| OpenClaw 日志显示 provider timeout，但模型探针成功 | OpenClaw 运行时、任务、session 或特定请求路径 | 继续保留证据，不把锅直接甩给 provider。 |
| 日志显示 proxy/DNS/TLS 错误 | 本机代理、DNS、TLS 或运营商路由 | 记录证据，避免重启风暴，优先修代理/网络路由。 |
| 日志显示 session expired 或 monitor stopped | 通道插件/session | 确认后重启 Gateway 往往有价值。 |

### 可选模型探针

如果你想判断问题到底出在 Gateway/通道，还是模型 provider 链路，可以显式开启：

```bash
MODEL_PROBE_ENABLED="1"
```

开启后，看门狗会先读取 OpenClaw 当前模型 provider 的 `baseUrl`，做一次不带凭据、不消耗 token 的入口连通性探测。然后再执行端到端模型探针：

```bash
openclaw agent --session-id "$MODEL_PROBE_SESSION_ID" \
  --thinking "$MODEL_PROBE_THINKING" \
  --timeout "$MODEL_PROBE_TIMEOUT" \
  --json \
  --message "$MODEL_PROBE_MESSAGE"
```

如果 `MODEL_PROBE_MODEL` 为空，就使用 OpenClaw 当前配置的默认模型。结果会写入主日志，以及：

```text
~/.local/state/openclaw-gateway-watchdog/model-probe-history.jsonl
~/.local/state/openclaw-gateway-watchdog/last-openclaw-model-probe.json
~/.local/state/openclaw-gateway-watchdog/last-model-api-edge-probe.txt
```

排查凌晨模型 provider 超时，可以先用这组设置：

```bash
MODEL_PROBE_ENABLED="1"
MODEL_EDGE_PROBE_ENABLED="1"
MODEL_PROBE_INTERVAL="600"
MODEL_PROBE_TIMEOUT="120"
MODEL_PROBE_ACTION="log"
MODEL_PROBE_THINKING="off"
MODEL_PROBE_MESSAGE="Reply with exactly OK."
```

`MODEL_PROBE_ACTION` 支持：

- `log`：只记录证据，默认策略。
- `restart`：连续失败达到 `MODEL_PROBE_FAILURES_BEFORE_ACTION` 后重启 gateway，但会先确认外部网络不是全局断网。
- `command`：连续失败后执行 `MODEL_PROBE_COMMAND`。

这个功能会真实调用模型，可能消耗额度或费用。日志不会打印 API key，但会记录 provider/model 名称、耗时、退出状态和第一行错误摘要。
`MODEL_EDGE_PROBE_ENABLED` 不使用凭据，也不调用 `/chat/completions`；它只检查 provider API 入口，比如 `https://api.deepseek.com`，是否能快速完成 DNS/TLS/HTTP 连接。

## 安全边界

这个项目不修改 OpenClaw 配置、不改微信插件源码、不处理消息内容。默认情况下它只做三件事：

1. 探测本机 gateway 和外部 URL。
2. 写自己的日志和状态文件。
3. 在满足保护条件后执行配置好的 gateway 重启命令。

可选模型探针只有在你显式开启后才会发起真实模型请求。

分享日志前，请检查里面是否包含本机路径、服务名或私有通道地址。

## 开源许可

MIT-0。这个许可证符合 ClawHub skill 发布要求，也方便别人直接复用、改造和分发。

## 发布到 ClawHub

已发布包：

- ClawHub：<https://clawhub.ai/zc-kama/gateway-resilience-guard>
- Slug：`gateway-resilience-guard`

本仓库带 `SKILL.md`，也可以重新发布为 OpenClaw skill：

```bash
clawhub publish . \
  --slug gateway-resilience-guard \
  --name "OpenClaw Gateway Resilience Guard" \
  --version 1.4.4 \
  --changelog "Make dashboard controls robust with native semantic buttons/selects, fixed hover states, centered brand mark, and non-overlapping config rows"
```

发布前需要先执行 `clawhub login` 完成 CLI 登录。
