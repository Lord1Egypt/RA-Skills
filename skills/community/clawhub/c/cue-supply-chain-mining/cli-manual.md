# Omni Reader Bridge CLI 手册 / 命令参考

**适用版本：v1.8.0**（`@cueai/omni-reader-mcp`）
**适用环境：PC 本地运行。VM 暂不支持。**
最后更新：2026-09-16

---

## 0. 概述

| 项 | 值 |
| --- | --- |
| npm 包名 | `@cueai/omni-reader-mcp` |
| 可执行文件名 | `omni-reader-mcp` |
| 运行时 | Node.js **>= 20.12** |
| 附带要求 | `npm` / `npx`（随 Node.js 分发） |
| 程序类型 | 本地 stdio MCP Server（Bridge），同时提供管理子命令 |
| 默认行为 | **不带任何参数执行即启动 stdio MCP Server** |

Bridge 是 Omni Reader 的本地形态，与远程 MCP 端点属同一提供方，不是第二个连接器。本地文件解析在 Bridge 内完成，不经 Cue 服务端。

---

## 1. 安装

### 1.1 前置条件

Node.js >= 20.12：

```bash
node -v
```

### 1.2 安装命令（推荐，无交互）

```bash
npx -y @cueai/omni-reader-mcp@1.8.0 setup --client generic --yes --json
```

- `-y`：自动确认 npx 的包下载，全程无交互
- `--yes`：跳过同意确认
- `--json`：输出结构化结果，**其中含安装后的版本号**，可用于确认安装成功与定位版本问题

成功输出（单行 JSON）：

```json
{"status":"configured","target":"generic","package":"@cueai/omni-reader-mcp","version":"1.8.0","config_path":"<写入的配置文件绝对路径>","allowed_roots":0,"reload":"<重载提示>"}
```

`status` 取值：

| 值 | 含义 |
| --- | --- |
| `configured` | 已写入 Agent 的 user-scope 配置文件 |
| `manual_configuration` | 未识别到可写入的 Agent 配置，改为输出待手工粘贴的配置片段 |

### 1.3 安装命令（headless / pty 环境）

在经 pty 运行的环境中，用 `--headless` 显式声明无交互：

```bash
npx -y @cueai/omni-reader-mcp@1.8.0 setup --client generic --allowed-root <绝对路径> --headless --json
```

### 1.4 全局安装（可选）

```bash
npm i -g @cueai/omni-reader-mcp@1.8.0
omni-reader-mcp setup --client generic --yes --json
```

### 1.5 安装写入行为

| Agent | 配置文件 |
| --- | --- |
| Hermes | `~/.hermes/config.yaml` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Desktop | macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`<br>Windows：`%APPDATA%\Claude\claude_desktop_config.json` |
| generic / other | 不写文件，向标准输出打印配置片段 |

- 配置中只写入 `${CUE_API_KEY}` 引用，不落明文 Key
- 写入后立即执行一次控制面连通性检查；若失败，会自动回滚已写入的配置并给出明确报错
- `setup` 幂等，可重复执行

---

## 2. 登录 / 鉴权

**需要鉴权。不是浏览器登录，无 OAuth，无账号密码流程。**

| 项 | 值 |
| --- | --- |
| 鉴权方式 | Cue API Key |
| 注入方式 | 环境变量 `CUE_API_KEY` |
| 传输格式 | 请求头 `Authorization: Bearer <key>` |
| Key 获取地址 | https://cuecue.cn/hub/api-key |
| 是否必须 | **是** |

说明：

- 未配置 `CUE_API_KEY` 时，`setup` 会失败并提示获取 Key 的地址；`doctor` 显示 `Cue API Key: absent` 并输出同样的指引。
- **请勿将 API Key 粘贴到对话中**，应在 Agent 的安全密钥或环境设置中配置。
- Bridge 仅访问用户指定的文件或目录，不扫描其他位置。

---

## 3. 命令与参数

```
Usage: omni-reader-mcp [setup|doctor|clean|uninstall|--help|--version]

No arguments start the stdio MCP server.
setup   Configure a supported user-scope Agent
doctor  Check local configuration and protocol health
        [--json] [--config-path <absolute-json-path> --server-name <entry>]
clean   Delete Bridge-created local artifacts and expired records
uninstall Restore a trusted URL-only Agent entry without deleting artifacts
```

### 3.1 `setup`

配置受支持的 user-scope Agent。

| 参数 | 取值 | 说明 |
| --- | --- | --- |
| `--client <name>` | `hermes` \| `cursor` \| `claude-desktop` \| `generic` \| `other` | 目标 Agent。非交互场景必填 |
| `--allowed-root <绝对路径>` | 绝对路径 | 设置允许解析的根目录 |
| `--add-root <绝对路径>` | 绝对路径 | 追加允许解析的根目录。**不可与 `--allowed-root` 同时使用** |
| `--yes` | 布尔 | 跳过同意确认，直接写入 |
| `--headless` / `--non-interactive` | 布尔 | 声明无交互运行，跳过同意确认 |
| `--json` | 布尔 | 以单行 JSON 输出结果 |

运行方式与是否阻塞：

| 场景 | 结果 |
| --- | --- |
| 交互式终端，且未指定 `--yes` / `--headless` | **交互**：预览变更，需输入 `yes` 才写入 |
| 交互式终端 + `--headless` | 非交互，直接写入 |
| 非交互环境 + `--yes` | 非交互，直接写入 |
| 非交互环境，且未指定 `--yes` / `--headless` | 报错退出（`Non-interactive setup requires --yes.`） |
| `--headless` 但未指定 `--client` | 报错退出 |

### 3.2 `doctor`

检查本地配置与协议健康状态。只读，不修改任何配置。

| 参数 | 说明 |
| --- | --- |
| `--json` | 以单行 JSON 输出完整报告 |
| `--silent-check` | 仅做「本地版本 ↔ 最新发布版本」比对；结果缓存 24 小时，供 Agent 会话启动时低成本探测更新 |
| `--config-path <绝对路径>` | 额外检查指定的 MCP 配置文件。**必须与 `--server-name` 成对出现** |
| `--server-name <条目名>` | 指定配置文件中的条目名。**必须与 `--config-path` 成对出现** |

输出字段说明：

| 字段 | 取值 |
| --- | --- |
| `inspection_scope` | 检查范围，固定为 `current_process_env` |
| `package_version` | 当前安装版本 |
| `node_version` / `npm_version` | 运行时版本 |
| `version_check.status` | `current` / `outdated` / `ahead` / `unavailable` |
| `client_adapters.*.status` | `configured` / `not configured` / `invalid or unreadable` |
| `api_key.status` | `present` / `absent` |
| `allowed_roots` | 已授权根目录数量与合法性 |
| `endpoints.url_control` | 控制面协议版本；或 `unavailable or incompatible`；未配置 Key 时为 `skipped (Cue API Key absent)` |
| `endpoints.direct_upload` | 本地文件解析链路的可用性状态，由首次真实解析验证 |
| `artifacts` | 本地结果缓存的文件数与占用字节数，含最早过期时间 |
| `cache.mode` | `default` / `fallback` |
| `onboarding` | 新手积分策略，不可达时为 `unavailable` |

输出样例（该环境未配置 Cursor 与 Claude Desktop）：

```
inspection_scope=current_process_env
Node: v24.15.0
npm: 11.12.1
Package: 1.8.0 (up to date)
Cue API Key: present
Allowed roots: 0 (safe)
Hermes config: invalid or unreadable
Cursor config: not configured
Claude Desktop config: not configured
Omni control protocol: omni.parse_grant.v1
Omni granted data plane: not probed (validated on the first real local-file parse)
Artifacts: 2 file(s), 3914 byte(s)
Artifact expiry: 2026-09-10T06:41:56.318Z
Cache: default
```

### 3.3 `clean`

清理 Bridge 产生的本地缓存与过期记录。**不接受任何参数。**

```bash
npx -y @cueai/omni-reader-mcp@1.8.0 clean
```

输出：`Removed <N> Bridge cache item(s).`

若缓存目录不安全（如为符号链接，或与当前项目目录相互包含），会报错且不删除任何文件。

### 3.4 `uninstall`

将 Agent 配置恢复为「可信 URL-only 条目」，**不删除本地结果缓存**。

```bash
npx -y @cueai/omni-reader-mcp@1.8.0 uninstall --yes --json
```

`--yes` 与 `--json` **均为必填**。

输出（单行 JSON）：

```json
{"status":"uninstalled","restored_remote":true,"artifacts_preserved":true,"source_files_unchanged":true}
```

未检测到任何已安装配置时：

```json
{"status":"not_installed","restored_remote":false,"artifacts_preserved":true,"source_files_unchanged":true}
```

### 3.5 `--version` / `-v`

```bash
npx -y @cueai/omni-reader-mcp@1.8.0 --version
```

输出单行版本号，如 `1.8.0`。

### 3.6 `--help` / `-h` / `help`

```bash
npx -y @cueai/omni-reader-mcp@1.8.0 --help
```

输出上文 Usage 文本。无副作用、不联网。

### 3.7 无参数（MCP Server 模式）

```bash
npx -y @cueai/omni-reader-mcp@1.8.0
```

启动 stdio MCP Server，通过标准输入输出与 Agent 通信，不输出人类可读日志。

---

## 4. 退出码

| 退出码 | 含义 | 典型场景 |
| --- | --- | --- |
| `0` | 成功 | 所有命令正常完成 |
| `1` | 运行失败 | 鉴权失败（缺少或无效的 `CUE_API_KEY`）、控制面连通性检查失败、缓存目录不安全、命令参数不满足该命令的强制要求 |
| `2` | 参数错误 | 未知命令、未知或重复的参数、参数缺少取值、`--config-path` 与 `--server-name` 未成对、`--headless` 未指定 `--client`、非交互环境未指定 `--yes` |

补充：

- 退出码非 `0` 时，错误信息写入标准错误，格式为 `Error: <message>`
- 启动阶段的致命错误同样写入标准错误，并以 `1` 退出
- MCP Server 模式在收到 `SIGINT` / `SIGTERM` 时优雅关闭

---

## 5. 输出格式

| 场景 | 输出流 | 格式 |
| --- | --- | --- |
| 默认（未指定 `--json`） | 标准输出 | 人类可读多行文本 |
| `--json` | 标准输出 | **单行无缩进 JSON**，以换行结尾 |
| `--version` | 标准输出 | 单行版本号 |
| `--help` | 标准输出 | Usage 多行文本 |
| 任何错误 | **标准错误** | `Error: <message>` |
| MCP Server 模式 | 标准输入输出 | JSON-RPC |

约定：

- `--json` 输出始终为单行，便于用 `jq` 或正则解析；不同命令的字段集不同，见第 3 节各命令说明
- 命令失败时不输出 JSON，一律走标准错误
- 所有输出不含 ANSI 颜色码，可直接重定向到文件

---

## 6. 升级说明

### 6.1 版本发布渠道

| 项 | 值 |
| --- | --- |
| 渠道 | npm registry `https://registry.npmjs.org/` |
| 包名 | `@cueai/omni-reader-mcp` |
| 最新版本标签 | `dist-tags.latest`（当前为 `1.8.0`） |

### 6.2 是否支持自动升级

**不支持。客户端不会自动升级，必须显式执行升级命令。**

### 6.3 升级命令

```bash
npx -y @cueai/omni-reader-mcp@1.8.0 setup --client generic --yes --json
```

跟随最新版：

```bash
npx -y @cueai/omni-reader-mcp@latest setup --client generic --yes --json
```

全局安装场景：

```bash
npm i -g @cueai/omni-reader-mcp@latest
```

### 6.4 覆盖安装与版本兼容

- `setup` 为**幂等覆盖安装**：重复执行会更新既有条目，并保留 `CUE_API_KEY` 引用与已配置的 allowed roots
- 指定固定版本号（如 `@1.8.0`）可保证部署可复现；使用 `@latest` 则每次拉取最新发布版
- 升级只影响 Bridge 自身，本地结果缓存不受影响
- 降级：指定目标版本号重跑 `setup` 即可，如 `@1.7.3`
- 无法访问 npm registry 时，版本检查结果会显示为不可用，不会误报为已是最新

### 6.5 版本检查

| 目的 | 命令 |
| --- | --- |
| 查看完整版本与环境诊断 | `npx -y @cueai/omni-reader-mcp@1.8.0 doctor` |
| 仅做轻量版本比对（结果缓存 24 小时） | `npx -y @cueai/omni-reader-mcp@1.8.0 doctor --silent-check` |
| 确认当前安装版本 | `npx -y @cueai/omni-reader-mcp@1.8.0 --version` |

`doctor` 会在检测到新版本时给出明确升级指令，例如：

```
Package: 1.8.0 (latest published: 1.9.0 — npx -y @cueai/omni-reader-mcp@1.9.0 setup to upgrade)
```

### 6.6 卸载

```bash
npx -y @cueai/omni-reader-mcp@1.8.0 uninstall --yes --json
```

卸载后如需清理本地缓存，再执行 `clean`。

---

## 7. 远程依赖与网络要求

| 域名 | 接口路径 | 用途 | 协议 |
| --- | --- | --- | --- |
| `registry.npmjs.org` | `/` | 包下载（安装 / 升级） | HTTPS |
| `registry.npmjs.org` | `/@cueai/omni-reader-mcp/latest` | 版本比对（`doctor` 更新探测） | HTTPS |
| `mcp.cuecue.cn` | `POST /api/omni-reader/mcp/` | 解析主接口（远程 MCP 端点） | HTTPS |
| `mcp.cuecue.cn` | `/api/omni-reader/capabilities/v1` | 能力探测（v1） | HTTPS |
| `mcp.cuecue.cn` | `/api/omni-reader/capabilities/v2` | 能力探测（v2） | HTTPS |
| `mcp.cuecue.cn` | `GET /api/omni-reader/direct-upload/v1/health` | 控制面连通性检查（`setup` / `doctor` 调用） | HTTPS |
| `omni-upload.cuecue.cn` | `/omni/granted/` | 授权上传与结果流 | HTTPS |
| `cuecue.cn` | `/hub/api-key` | API Key 获取页（`/api-key` 为兼容路径） | HTTPS |
| `cuecue.cn` | `/api/v1/billing/public/onboarding-policy` | 新手积分策略查询 | HTTPS |
| `nodejs.org` | `/` | 仅当需安装 Node.js 运行时 | HTTPS |

说明：

- 全部远程接口均为 HTTPS，无明文 HTTP 依赖，无第三方 CDN，无登录页跳转
- **必要依赖**：`registry.npmjs.org`（安装 / 升级）与 `mcp.cuecue.cn` 的解析主接口及控制面检查接口。上述任一不可达，对应功能不可用
- `mcp.cuecue.cn/api/omni-reader/capabilities/v1`、`/v2` 与 `omni-upload.cuecue.cn/omni/granted/` 在解析过程中按需访问
- `cuecue.cn/api/v1/billing/public/onboarding-policy` 请求失败**不影响功能**（3 秒超时后忽略，仅影响新手提示文案）
- `registry.npmjs.org/@cueai/omni-reader-mcp/latest` 不可达时，版本检查结果降级为「不可用」，不影响其他功能
- 本地文件解析由 Bridge 在本机完成、不经服务端；但 `setup` 阶段需能连通控制面（会执行一次连通性检查，失败则自动回滚配置）
- 代理环境需放行上述 HTTPS 域名

---

## 8. 环境变量

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `CUE_API_KEY` | **是** | Cue API Key，用于鉴权 |
| `OMNI_ALLOWED_ROOTS` | 否 | 允许解析的本地目录，多路径以 `:`（Windows 为 `;`）分隔，须为绝对路径 |
| `OMNI_CACHE_DIR` | 否 | 覆盖本地结果缓存根目录 |

默认结果缓存目录：

| 平台 | 路径 |
| --- | --- |
| macOS | `~/Library/Caches/cue/omni-reader-mcp` |
| Windows | `%LOCALAPPDATA%\Cue\omni-reader-mcp\Cache` |
| Linux | `$XDG_CACHE_HOME/cue/omni-reader-mcp`（未设置时为 `~/.cache/cue/omni-reader-mcp`） |

结果缓存保留期 24 小时，可用 `clean` 手动清理。

---

## 9. 快速参考

| 目的 | 命令 |
| --- | --- |
| 安装 | `npx -y @cueai/omni-reader-mcp@1.8.0 setup --client generic --yes --json` |
| 无交互安装（pty 环境） | `npx -y @cueai/omni-reader-mcp@1.8.0 setup --client generic --allowed-root <绝对路径> --headless --json` |
| 版本检查 | `npx -y @cueai/omni-reader-mcp@1.8.0 --version` |
| 环境诊断 | `npx -y @cueai/omni-reader-mcp@1.8.0 doctor` |
| 轻量更新探测 | `npx -y @cueai/omni-reader-mcp@1.8.0 doctor --silent-check` |
| 帮助 | `npx -y @cueai/omni-reader-mcp@1.8.0 --help` |
| 升级 | `npx -y @cueai/omni-reader-mcp@1.8.0 setup --client generic --yes --json` |
| 清理缓存 | `npx -y @cueai/omni-reader-mcp@1.8.0 clean` |
| 卸载 | `npx -y @cueai/omni-reader-mcp@1.8.0 uninstall --yes --json` |
