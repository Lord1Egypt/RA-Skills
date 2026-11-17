# MCP schema 实测与 shim 探针

## 1 已测结果（2026-11-09 s2）

| server | 状态 | 工具数 | tools 字节 | 备注 |
|---|---|---:|---:|---|
| github | measured | 46 | 126,805 | HTTP；最大单工具 `issue_write` 5,768 B |
| node_repl | measured | 4 | 2,400 | stdio；`js` 1,187 B |
| lis-skill-bus | measured | 6 | 1,276 | stdio |
| computer-use | disabled | 0 | 0 | CLI disabled；App 侧是否存在未知 |
| cua_repl | disabled | 0 | 0 | 同上 |
| codex_app | **unmeasurable** | 31（声明） | 上界 12,400 | App tools 管道拒绝外部客户端；31 × 400 B |

- 原始 schema 已知三项合计：**130,481 B**；加 codex_app 上界：**142,881 B**。
- 隔离 `CODEX_HOME` 抓包：首请求只有 12 个内置工具、19,144 B，无任何 `mcp__` 工具 → 存在按需发现/延迟下发。
- `codex_app` 配置 `omit_tools_from=[deferred]`；当前 App 会话实际工具只有 `mcp__codex_app__*` 与 `mcp__node_repl__*`，github/lis-skill-bus 未下发。
- 结论：**原始 schema 口径 FAIL；App 实际注入口径 UNMEASURED**。不得把 130,481 B 当每请求成本。

## 2 独立探针（安全）

### stdio server

```bash
python3 scripts/mcp_probe.py --stdio --name example-server -- \
  ${CODEX_HOME}/mcp_servers/example-server/serve.py serve
python3 scripts/mcp_probe.py --stdio --name node_repl -- \
  /path/to/node_repl_entrypoint
```

### HTTP server（token 只从环境变量读，不打印）

```bash
# 先在当前 shell 设置 GITHUB_PAT_TOKEN，值不写进命令或日志
python3 scripts/mcp_probe.py \
  --http https://api.githubcopilot.com/mcp/ --name github --bearer-env GITHUB_PAT_TOKEN
```

### 已知禁用

```bash
python3 scripts/mcp_probe.py --disabled --name computer-use
python3 scripts/mcp_probe.py --disabled --name cua_repl
```

探针只统计 `tools/list` 返回的 `tools` 数组 compact JSON 字节；不记录 messages、请求体、token。

## 3 shim 探针（仅在做整体定论时）

目标：在 `127.0.0.1:18765` Responses 转发链路上临时统计真实请求里的 tools schema 字节，然后**透明转发**。

前置：

1. 记录现有 shim 的 PID 与 cmdline：`lsof -nP -iTCP:18765 -sTCP:LISTEN`、`ps -p <PID> -o command=`。
2. 备份 shim 脚本与启动配置；不备份/不记录对话正文。
3. 只在用户明确同意、且当前对话可中断的窗口执行。

执行：

1. 停旧 shim，启动统计型 shim：解析请求 JSON，只累加 `tools` 数组 compact 字节、工具数、`mcp__` 前缀计数；随后原样转发到上游。
2. 发一条最小请求（如 `codex debug prompt-input "x"` 或 App 新会话首问）。
3. 记录 `tools_bytes`、`tool_count`、`mcp_tool_count`、时间戳；**不落请求体**。
4. 立即恢复原 shim，确认 `curl -sS http://127.0.0.1:18765/health` 返回 200，App 请求恢复正常。
5. 若恢复失败：先按备份原样启动旧 shim，再排查；不得带着临时 shim 继续对话。

红线：

- 不改 `${CODEX_HOME}/config.toml`、不改 MCP 正式配置、不改 provider/认证/计费。
- 不把请求体、对话内容、token 写入日志或证据。
- 未完成恢复前，不宣称“已实测”。

## 4 恢复与回滚

- shim：`cp -p <备份的 shim 脚本> <原路径>`，按记录的 cmdline 重启，`/health` 200 为恢复标志。
- 探针：无副作用；输出 JSON 由调用方指定路径。
- 若 App 请求异常：先停统计 shim、恢复旧 shim，再重启 App；不要反复重试。
