# 传输：浏览器会话和 Open API token

浏览器传输负责 testcase 的读和 Phase 2a 单条写。Open API 传输仍是钩子，调用会失败。testcase 模块不要传 Open token。

| | 浏览器会话 | Open API token（未实现） |
|--|-----------|-------------------------|
| 谁在用 | `testcase` 的读命令，以及 `create` / `update` / `set-status` / `delete` | 预留给以后的 task / project。**不要**拿来读或写测试用例 |
| 地址 | `https://www.teambition.com/testcase/api/`。移到回收站是 `https://www.teambition.com/api/testcases/{id}/archive` | `open.teambition.com`（本技能不调用） |
| 凭据 | Ego 里 teambition.com 的登录会话。`page.fetch` 带上会话。写请求额外声明 `credentials: "include"` 和 JSON body | `teambition_cli` / MCP token。测试计划模块不认 |
| 代码 | `scripts/lib/session.mjs` 的 `createTransport("browser")` | `createTransport("open")` 抛 `TRANSPORT_NOT_IMPLEMENTED` |
| 写操作 | 仅 Phase 2a 白名单。GET 以外的方法由 `page.fetch` 转发。`cleanup` 只关本机空间 | 没有。Open 文档里的 create / flowStatus 未当作这些路径的等价实现 |

`scripts/tb.mjs` 的 domain 注册表目前只有 `testcase`。`task` 和 `project` 写在 `FUTURE_DOMAINS` 里，命令会拒绝执行。以后要加域，只注册新的 `run`，不要重写路由器。

登录检查不走这两套 API。它打开 https://www.teambition.com/ ，看登录墙、应用正文和 Cookie **名字**。不打印 Cookie 值。
