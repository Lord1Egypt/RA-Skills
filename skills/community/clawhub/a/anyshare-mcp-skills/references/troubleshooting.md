# AnyShare MCP — 常见错误与排查

> 按需查阅。完整流程与配置以技能根目录 **`SKILL.md`** 为准。  
> 认证通过写入 **`~/.mcporter/mcporter.json`** 的 `headers.Authorization` 字段完成。见 **`../SKILL.md`** **「首次配置」**。

---

## 初始化与 mcporter 配置

| 现象 | 可能原因 | 处理 |
| --- | --- | --- |
| 首次使用不知道填什么地址 | 技能包默认仅为占位；**企业客户**应向运维索取**本企业** **MCP 服务地址** | 按 **`SKILL.md`**「首次配置」：写入后无论成败都请用户确认是否为本企业正式端点 |
| 找不到 `asmcp` 或 `mcporter list` 无 asmcp | 未配置或未重载 daemon | 按 **`SKILL.md`** 写入 `~/.mcporter/mcporter.json`，执行 `mcporter daemon restart` 后再 `mcporter list` |
| 换网关后工具全失败 | **MCP 服务地址**已变但配置未更新 | 按 **`SKILL.md`「首次配置」** 更新 `asmcp.url` 并重启 daemon |
| `mcporter list` 有 `asmcp` 但请求返回 **503** | 默认官方 URL 在你网络/部署下不可达，或需私有化网关 | 向运维索取实际 MCP 端点并更新 `asmcp.url`；非技能文档错误 |
| 配置写入后仍连不上 MCP | **MCP 服务地址**（`url`）错误或服务未监听 | 核对 **MCP 服务地址**与端口；确认服务端 HTTP 可达 |

---

## 凭证与令牌

| 现象 | 可能原因 | 处理 |
| --- | --- | --- |
| 401 / 业务接口报未授权 | token 失效、吊销或无权访问该资源 | 按 **`SKILL.md`**「首次配置」Step 4：用户重新获取 token → 更新 `~/.mcporter/mcporter.json` 的 `headers.Authorization` → `mcporter daemon restart` |
| 换账号后仍是旧用户 | 配置中仍是旧账号的 token | 用新账号 token 更新 `headers.Authorization`，重启 daemon |
| daemon 重启后工具报认证失败 | `headers.Authorization` 中 token 已过期 | 用户重新获取 token → 更新配置 → `mcporter daemon restart` |

---

## 工具发现与调用

| 现象 | 可能原因 | 处理 |
| --- | --- | --- |
| 不知道有哪些工具 / 参数 | 与主技能约定不一致 | 以 **`mcporter list asmcp`** 返回的 schema 为准（`SKILL.md` 核心注意第 5 条） |
| `mcporter call` 报错或参数无效 | 使用了 `--key value` 风格 | 使用 **`key=value`**，例如：`mcporter call asmcp.file_search keyword="文档" type="doc" start=0 rows=25` |
| `Call to asmcp.* timed out after 60000ms`（或类似） | **mcporter** 对单次 `call` 的默认超时（约 60s），非 MCP 网关配置 | **运行 OpenClaw 的设备**：将技能包 **`openclaw.skill-entry.json`** 合并进 **`~/.openclaw/openclaw.json`** → **`skills.entries["anyshare-mcp-skills"].env`**（见 **`SKILL.md`「首次配置」Step 2**）；兜底：单次命令加 **`--timeout 600000`**；daemon 变更后建议 **`mcporter daemon restart`** |
| 直连 HTTP `tools/list` 无响应 | 未先 initialize 或地址错误 | 备选：按 `SKILL.md`「工具调用方式」③；日常优先 mcporter |

---

## 文件与搜索

| 现象 | 可能原因 | 处理 |
| --- | --- | --- |
| 技能要求**勿用** `file_upload`（见 `SKILL.md` **C11**） | 误选一键上传 | 上传仅用 **`file_osbeginupload` → PUT → `file_osendupload`** |
| `file_search` 分页/范围与预期不符 | 参数与实现不一致 | 仅传 `SKILL.md` 场景一允许的字段；以 `mcporter list asmcp` 中 `file_search` 的 schema 为准 |
| 搜索结果为空 | 关键词不匹配或路径/标签过滤过严 | 放宽关键词，或减少 `range`、标签限制 |
| `file_convert_path` 失败或 **`namepath` 为空** | `docid` 非完整 gns、无权限、或 `/efast/v1/file/convertpath` 报错 | 核对传入 **完整 `gns://…` docid** 与登录态；仍失败时**仅展示完整 docid**，路径展示可省略，**不阻塞**搜索/上传/下载主流程 |

---

## 上传 / 下载

| 现象 | 可能原因 | 处理 |
| --- | --- | --- |
| `file_osbeginupload` / `file_osendupload` 失败或参数无效 | `docid`/`rev`/`length`/`name` 与流程不一致，或 docid 无权限 | **begin** 用目标**目录** docid（**C3**）；**end** 的 `docid`/`rev` 须与 **begin 响应**一致；`length` 须等于实际文件字节数 |
| 对象存储 **PUT** 失败 | URL/鉴权过期、网络、或请求体与 `length` 不符 | 重试 begin；检查 `authrequest` 头与文件体；**PUT 成功前不要调用** `file_osendupload` |
| `file_osdownload` 失败 | 文件删除、无权限或 docid 错误 | 重新 `file_search` 并由用户确认 |

---

## `smart_assistant`（场景四全文写作）

| 现象 | 可能原因 | 处理 |
| --- | --- | --- |
| 流式返回截断 / 空答 | `query` 过长或网络问题 | 缩短 `query` 或拆多轮 |
| `mcporter call asmcp.smart_assistant` 超时 | 服务端推理久于 mcporter 默认 **call** 超时 | 优先确认 **`~/.openclaw/openclaw.json`** 已合并 **`openclaw.skill-entry.json`**（`skills.entries.anyshare-mcp-skills.env`）；沙箱会话另配 **`agents.defaults.sandbox.docker.env`**（见 **`SKILL.md`**）；兜底 **`--timeout 600000`** |
| 多轮中断 | 未回传 `conversation_id` | 从上一轮响应补传；`version` / `temporary_area_id` 不传（见 `SKILL.md` 场景四） |
| `source_ranges` 无效 | 传了文件夹 ID 或格式错误 | 按 `SKILL.md` 核心概念与 C5：`smart_assistant` 的 `id` 为 docid **最后一段**，`type` 为 `"doc"` |

---

## 网络与 TLS（测试环境）

| 现象 | 可能原因 | 处理 |
| --- | --- | --- |
| TLS 证书错误 | 自签名或内网证书 | 测试环境按部署说明处理；生产环境使用有效证书 |
| `connection refused` | **MCP 服务地址**或端口错误、防火墙 | 检查 **MCP 服务地址** URL 与网络连通性 |
