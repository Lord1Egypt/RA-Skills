---
name: agent-easy-http
description: >
  Deploy an HTTP(S) proxy that exposes OpenClaw agent capability as a REST API over your
  network IP (e.g. http://<your-server-ip>:7720). Use when asked to "start agent-easy-http",
  "expose openclaw agent as HTTP", "deploy openclaw agent HTTP service", "create internal HTTP
  API for agent", or "start the agent gateway". HTTP by default (zero-friction); optional HTTPS
  with self-signed SAN certificates for production / cross-host scenarios. Includes mandatory
  API Key auth, deny-list filter, prompt-injection hardening, and direct integration with
  OpenClaw native /hooks/agent (millisecond dispatch + automatic hook:<uuid> session isolation
  per request). Thin proxy layer; use skill-to-http-flash for per-skill API endpoints.
---

# agent-easy-http

- **Version**: 1.1.0
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/html-tool-suite (skill dir: `skills/agent-easy-http`)

把 OpenClaw 的 agent 能力通过 **HTTP(S) + 网络 IP** 暴露给其它系统调用。

> ## ⚠️ 安全须知（部署前必读）
>
> 本 skill 会启动一个常驻代理，把你的 **OpenClaw agent 暴露成可远程调用的 HTTP 接口**。agent 具备文件、shell、消息发送等本机能力，因此这是一个**对外开放的远程控制面**，请理解以下风险边界：
>
> - **`/agent/run` 是通用入口（v1.1.0 起默认关闭）**：开启后任何通过鉴权的调用方都能向 agent 发送**任意 prompt**，等价于完全交出 agent 控制权。默认 403，需在 config 显式 `enable_agent_run: true`。
> - **默认仅监听本机（v1.1.0 起）**：`listen_host` 默认 `127.0.0.1`。监听 `0.0.0.0` 且 TLS 未启用时**启动直接失败**，需 `AGENT_EASY_HTTP_ALLOW_INSECURE=1` 或 config `allow_insecure_public_bind: true` 显式豁免（跨主机务必启用 HTTPS，切勿生产 `curl -k`）。
> - **默认 HTTP 不加密**：默认模式下 `X-API-Key`、prompt、执行结果均**明文传输**。仅 `localhost` / 可信内网可接受。
> - **会修改全局配置**：init / watchdog 会写入并自愈 `~/.openclaw/openclaw.json` 的 hooks 配置（可选还会同步到 `OPENCLAW_CONFIG_SYNC_PATHS` 外部配置源）。这是平台级改动，管理员手动回退后 watchdog 可能重新应用，请知悉其持久化行为。
> - **保护好 API Key**：Key 是 bearer 凭证，泄露即等同交出 agent 调用权。注意别进入 shell history、日志、截图或权限过宽的文件。
>
> 一句话：**把它当作暴露内部 agent 服务来对待，务必配好鉴权、绑定与 TLS，而非零风险的便捷封装。**

> 🔒 **v1.1.0 安全加固摘要**：默认 `127.0.0.1`；`0.0.0.0`+HTTP 需显式豁免；`/agent/run` 默认 403；CORS 默认不挂载（`cors_origins` 按需配置）；`/result` 默认只返回 assistant 输出，完整对话需 `result_include_messages: true`。

> 📐 下文的 "v3.0 架构" 指本 skill 内部的**架构代号**（v3.0 = 基于 OpenClaw 原生 `/hooks/agent`
> 的轻代理实现，取代早期 v2.0 的 `openclaw agent` CLI 冷启动方案），与开源发布版本号 1.0.0 是两个维度。

**典型场景**：在 OpenClaw 容器/Pod 上部署，团队内其它服务通过 `http://<your-server-ip>:7720` 调用你的 OpenClaw agent 跑任务。

**默认 HTTP 模式（零门槛）**：v3.0 起 TLS 默认关闭，先跑通再升级。需要 HTTPS 时跑 `python3 scripts/gen_cert.py --san auto` + 改 config 即可切回。

---

## v3.0 重大重构

| 维度 | v2.0 | **v3.0** |
|---|---|---|
| 执行引擎 | `openclaw agent` CLI（embedded 启动 ~90s）| **OpenClaw 原生 `/hooks/agent`**（毫秒触发）|
| Session 隔离 | 🐛 多请求串入同一 session | ✅ **每请求自动 `hook:<uuid>`** |
| Job 管理 | 本地 JSON 持久化 + asyncio.Event | ❌ 删除（OpenClaw 自己管）|
| Callback HMAC | 自定义链路 | ❌ 删除（hooks fire-and-forget）|
| sub-agent 启动开销 | 每次冷启动 | ✅ 零开销 |
| 代码量 | ~1100 行 | **~1200 行**（server.py + 3 辅助脚本约 2600 行）|

### 仍然保留的核心层

- ✅ HTTP（默认）/ HTTPS（按需开启）+ SAN 证书
- ✅ API Key 强制鉴权（X-API-Key）
- ✅ deny_skills 黑名单（外层防火墙）
- ✅ Prompt 注入加固（分隔符 + 反注入指令）
- ✅ workspace 内持久化（PVC 安全）
- ✅ 环境变量覆盖（容器友好）

---

## 与 skill-to-http-flash 的定位区分

| 维度 | agent-easy-http | skill-to-http-flash |
|---|---|---|
| 调用方传入 | 自然语言 `message`（开放式 prompt） | skill name + structured params |
| 适用场景 | 让 agent 决定怎么干（"查 X 数据"）| 直接跑指定 skill |
| 入口 | `/agent/run` + `/skills/{name}/run`（兼容） | `/skills/{name}/run`（带参数 schema） |
| 隔离机制 | OpenClaw `/hooks/agent` 自动 | flash 自己管 |

→ 两个 skill 互补，不重叠。

---

## 快速开始

```bash
cd ~/.openclaw/workspace/skills/agent-easy-http

# 安装依赖（一次性）
pip install fastapi uvicorn pydantic httpx

# 交互式初始化（会引导启用 OpenClaw hooks）
python3 scripts/server.py init

# 启动服务（默认 https://0.0.0.0:7720）
python3 scripts/server.py start
```

init wizard 会：
1. 配监听端口
2. **自动检测 + 启用 OpenClaw hooks**（写 `~/.openclaw/openclaw.json`，热加载，无需重启）
3. 生成 API Key
4. 询问是否启用 HTTPS（**默认关闭**，需要时再生成证书）
5. 配 deny_skills 黑名单

---

## API 端点

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `/health` | 健康检查（无需鉴权）|
| GET | `/skills` | 列出已暴露的 Skill |
| GET | `/agents` | 列出可用 Agent + 当前路由策略（需鉴权）|
| GET | `/metrics` | 简版 metrics |
| GET | `/result/{run_id}` | 查询 agent 执行结果（pending/done/not_found + 完整对话）|
| POST | `/skills/{name}/run` | 触发指定 skill（自动注入 SKILL.md + 加固）|
| POST | `/agent/run` | 通用入口（**v1.1.0 起默认 403**，config `enable_agent_run: true` 开启）|
| POST | `/admin/reload` | 热重载 skill 列表 |

### `/agent/run` 响应

```json
{
  "success": true,
  "run_id": "6457f48c-78b0-4896-97e4-a55830d9a972",  // 用这个查 /result
  "agent_id": "(default)",
  "_openclaw": { "ok": true, "runId": "..." }       // OpenClaw 内部 cron job id
}
```

`run_id` 由 agent-easy-http 自生成（= hook session uuid 后缀），用它去 `/result/{run_id}` 拿 agent 输出。

### `/result/{run_id}` 响应

```json
{
  "status": "done",                    // pending | done | not_found
  "run_id": "6457f48c-...",
  "output": "agent 的完整回复文本",
  "messages": [{"role": "user", "text": "..."}, {"role": "assistant", "text": "..."}]
}
```

v1.1.0 起 `messages`（完整对话，含全部 user 输入）默认不返回，需 config `result_include_messages: true` 开启；默认只返回 `output`（assistant 输出），降低会话内容外泄面。

实测时序：触发 → 4-6s session 文件可读 → /result 返回 done。建议客户端 4s 后首次查询，每 1.5s 轮询。

### 请求示例

```bash
API_KEY=$(cat <workspace>/.http/secrets/api-keys/agent-easy-http.key)
CERT=<workspace>/.http/certs/server.crt

# 跑指定 skill
curl --cacert $CERT -H "X-API-Key: $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"message":"运行 hello-env"}' \
     https://192.168.1.10:7720/skills/hello-env/run

# 通用 agent 入口
curl --cacert $CERT -H "X-API-Key: $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"message":"帮我查下今天的天气"}' \
     https://192.168.1.10:7720/agent/run
```

### 响应

```json
{
  "success": true,
  "skill": "hello-env",
  "run_id": "acf07e6a-d792-434c-98c3-7d738c5d6e94",
  "_openclaw": {
    "ok": true,
    "runId": "acf07e6a-d792-434c-98c3-7d738c5d6e94"
  }
}
```

✨ **毫秒级返回**。agent 在后台跑（在 `agent:main:hook:<uuid>` session 里），完全隔离不影响你的主会话。

---

## 配置文件

默认位置：`<workspace>/.agent-easy-http/config.json`

| 字段 | 默认 | 说明 |
|---|---|---|
| `listen_host` | `127.0.0.1` | 监听地址（v1.1.0 起默认仅本机；`0.0.0.0`+HTTP 需显式豁免）|
| `port` | `7720` | 监听端口 |
| `tls_enabled` | `false` | HTTPS 开关（默认关闭，按需启用，见下文「切到 HTTPS」）|
| `api_key` | `""` | 必须 init 时生成 |
| `expose_skills` | `[]` | 白名单（空=全暴露）|
| `deny_skills` | `[]` | 黑名单（推荐配几个有副作用的）|
| `enable_agent_run` | `false` | `/agent/run` 通用入口开关（v1.1.0 起默认 403，开启=交出 agent 全权）|
| `allow_insecure_public_bind` | `false` | 允许 `0.0.0.0`+明文 HTTP 启动（强烈不推荐）|
| `cors_origins` | `[]` | CORS 允许来源（空=不挂 CORS；服务间调用不需要）|
| `result_include_messages` | `false` | `/result` 是否返回完整对话（默认仅 assistant 输出）|
| `max_concurrent_jobs` | `10` | 并发上限 |
| `hook_request_timeout` | `30` | POST /hooks/agent 超时（秒） |
| `hook_url` | `""` | hook 端点 URL（空=自动从 openclaw.json 推导）|
| `hook_token` | `""` | hook 鉴权 token（同上）|
| `default_agent_id` | `""` | 默认路由的 agent ID（空=OpenClaw 默认 main agent）|
| `allowed_agent_ids` | `[]` | 调用方可指定的 agent 白名单；`["*"]`=全允许；`[]`=禁止调用方指定 |

### Hook 端点解析优先级

```
1. AGENT_EASY_HTTP_HOOK_URL / AGENT_EASY_HTTP_HOOK_TOKEN  (env)
2. config.json 的 hook_url / hook_token
3. 自动从 ~/.openclaw/openclaw.json 推导（推荐）
```

用户**通常不需要配** hook_url/token——init wizard 会自动启用 OpenClaw hooks 并设置好。

---

## 子命令

```bash
python3 scripts/server.py init              # 交互式初始化
python3 scripts/server.py setup-hooks       # 只启用 OpenClaw hooks
python3 scripts/server.py start             # 启动
python3 scripts/server.py stop              # 停止
python3 scripts/server.py status            # 状态
python3 scripts/server.py paths             # 查看所有路径
python3 scripts/server.py restart           # 重启
python3 scripts/gen_cert.py --san auto      # 重新生成证书
```

### 检测 hooks 状态（独立工具）

```bash
python3 scripts/init_wizard.py --check-hooks    # 只检测不修改
python3 scripts/init_wizard.py --setup-hooks-only  # 只启用 hooks
python3 scripts/init_wizard.py --setup-hooks-only --force-new-token  # 重置 token
```

### 自愈守护（watchdog）

```bash
# 前台跑（容器场景推荐）
bash scripts/watchdog.sh run

# 后台跑
bash scripts/watchdog.sh start
bash scripts/watchdog.sh status
bash scripts/watchdog.sh stop
```

watchdog 每 30s 检查 server，挂了自动重启。

---

## 环境变量

| 变量 | 对应字段 |
|---|---|
| `AGENT_EASY_HTTP_PORT` | port |
| `AGENT_EASY_HTTP_HOST` | listen_host |
| `AGENT_EASY_HTTP_API_KEY` | api_key |
| `AGENT_EASY_HTTP_NO_TLS` | 关闭 TLS |
| `AGENT_EASY_HTTP_MAX_CONCURRENT` | max_concurrent_jobs |
| `AGENT_EASY_HTTP_HOOK_TIMEOUT` | hook_request_timeout |
| `AGENT_EASY_HTTP_DENY_SKILLS` | deny_skills（逗号分隔）|
| `AGENT_EASY_HTTP_HOOK_URL` | hook_url |
| `AGENT_EASY_HTTP_HOOK_TOKEN` | hook_token |
| `AGENT_EASY_HTTP_NO_WATCHDOG` | 设为任意非空值可跳过 `start` 时自动启动 watchdog |
| `OPENCLAW_HTTP_ROOT` | TLS/secrets 共享根 |
| `AGENT_EASY_HTTP_DATA_ROOT` | skill 私有数据根 |

---

## 数据路径（workspace 内，PVC 安全）

```
<workspace>/.agent-easy-http/   # 本 skill 数据
  config.json
  server.pid / server.port
  logs/server.log / watchdog.log

<workspace>/.http/              # 三个 HTTP skill 共享
  certs/server.{crt,key}        # TLS（SAN 支持多 IP）
  secrets/api-keys/agent-easy-http.key  # API Key
```

跑 `python3 scripts/server.py paths` 一键查所有路径 + 存在性。

---

## OpenClaw hooks 启用机制

agent-easy-http v3.0+ 依赖 OpenClaw 的原生 `/hooks/agent` 端点，需要 4 项配置：

| 配置项 | 值 | 用途 |
|---|---|---|
| `hooks.enabled` | `true` | 启用 hooks 端点 |
| `hooks.token` | `<32 字符随机>` | 鉴权 token |
| `hooks.allowRequestSessionKey` | `true` | 允许调用方自定义 sessionKey（v1.0.4+ /result 接口必需） |
| `hooks.allowedSessionKeyPrefixes` | `["hook:"]` | 限制自定义 sessionKey 前缀，安全兜底 |

init wizard 自动完成全部配置：

1. 读 `~/.openclaw/openclaw.json` 检测 4 项配置完整性
2. 缺失 → 询问用户是否启用（默认 Y）+ 提示影响范围
3. 写入 openclaw.json + **可选同步到 `OPENCLAW_CONFIG_SYNC_PATHS` 指定的外部配置源**（托管/容器环境防被外部 config 中心覆盖；普通部署无需设置）
4. 等待 Gateway 热加载（3s）+ POST 一个 ping 验证

⚠️ 如果发现 hooks 失效（外部 config 中心覆盖等情况）：
- **自动**：watchdog 30s 内检测到任一配置缺失，自动调 init_wizard 修复
- **手动**：跑 `python3 scripts/server.py setup-hooks`

⚠️ **安全说明**：`allowRequestSessionKey=true` 是 OpenClaw 全局配置，会影响所有 /hooks/agent 调用方（不只 agent-easy-http）。受 `allowedSessionKeyPrefixes=["hook:"]` 限制，外部只能用 `hook:` 前缀，无法污染其他 session（如 webui/cron）。

---

## 安全模型

| 层 | 防御 |
|---|---|
| **传输** | HTTP 默认 / HTTPS 可选（TLS + 自签 SAN 证书；0.0.0.0 跨主机场景强烈推荐启用，启动会 warning）|
| **接入** | API Key (`X-API-Key`，32 字符随机) |
| **暴露** | deny_skills 黑名单（推荐拒有副作用 / 会对外发消息的 skill） |
| **Agent 路由** | `allowed_agent_ids` 白名单控制调用方可指定的 agent 范围 |
| **Prompt 注入** | 分隔符 + 反注入指令包裹用户 message |
| **Session 隔离** | OpenClaw `/hooks/agent` 自动 `hook:<uuid>` 每请求独立 |
| **OpenClaw 内层** | OpenClaw 自动给 hook 消息加 `EXTERNAL_UNTRUSTED_CONTENT` 包装 |

> ⚠️ **`GET /agents` 信息披露**：该接口需 API Key 鉴权，但返回内部所有 agent 的 ID 与名称。
> API Key 泄露时外部可枚举所有 agent 存在。建议在不需要动态查询时，将 `allowed_agent_ids`
> 设为固定白名单而非 `["*"]`，以减小攻击面。

---

## 切到 HTTPS（按需）

默认 HTTP 模式跑通后，跨主机调用或暴露在不太信任的网络段时建议切到 HTTPS。三步：

```bash
# 1. 生成自签 SAN 证书（自动嗅探本机 IP 写入 SAN）
python3 scripts/gen_cert.py --san auto

# 2. 编辑 config，把 tls_enabled 改成 true
#    路径: <workspace>/.agent-easy-http/config.json

# 3. 重启服务
python3 scripts/server.py restart
```

调用方需要信任自签证书：

```bash
# 方式 A：curl --cacert 临时信任
curl --cacert <workspace>/.http/certs/server.crt -H "X-API-Key: $KEY" ...

# 方式 B：导入系统信任库（Linux 示例）
sudo cp <workspace>/.http/certs/server.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

详细客户端信任指引见 `references/deployment.md`。

---

## 文件结构

```
agent-easy-http/
├── SKILL.md
├── scripts/
│   ├── server.py            主服务（FastAPI + hook 代理）
│   ├── tls_auth.py          TLS/API Key/HMAC 模板（callback HMAC 保留备用）
│   ├── gen_cert.py          自签 SAN 证书生成
│   ├── init_wizard.py       交互式初始化 + hooks 自动启用
│   └── watchdog.sh          自愈守护脚本
└── references/
    ├── design.md            v2.0 架构设计（保留作历史参考）
    ├── tls-auth-standard.md 三 skill 共用规范
    └── deployment.md        客户端/反代/FAQ
```

---

## 与 skill-to-http(-flash) 后续对齐

skill-to-http 和 skill-to-http-flash 仍使用 `openclaw agent --local`（embedded 90s+ 启动）。后续可以参考本 skill 的改造把它们也切到 `/hooks/agent`，但作为独立项目（Phase 5）评估。
