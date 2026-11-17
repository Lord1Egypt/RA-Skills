# 安装、权限与迁移

以下命令在安装后的 skill 目录执行，即同时包含 `SKILL.md`、`package.json` 的目录。需要 Node.js 22+ 和 npm。运行代码及锁定依赖清单随包提供，不从游戏服务器下载代码执行。

```bash
npm ci --ignore-scripts
node tools/doctor.mjs
node tools/setup.mjs --locale zh-CN
```

`npm ci` 从 npm 仓库下载锁定的 MCP SDK、JSON Schema 校验器、WebSocket 客户端及其依赖，并禁用安装脚本。doctor 启动本机 stdio MCP 子进程，检查工具清单和坐标换算，不登录、不进入角色、不执行游戏操作。

setup 需要玩家自己的交互终端，密码输入不回显。它在 `~/.earth2037-agent/` 生成私有凭据 `credentials.json`，POSIX 文件权限 600、目录权限 700；同时生成 `mcp.json`、`hermes-mcp.yaml`、`dsh-mcp.patch.yaml`。已有凭据保留，生成的配置文件会被替换。只把其中 Earth2037 条目合并到所用助手配置，不覆盖其他 MCP。setup 不自动修改助手全局配置、不启动后台服务。

通用 MCP 使用 `node /绝对路径/src/main.mjs`，传输方式是 stdio，不是公开 HTTP 服务，不需要开放端口。

## 凭据、网络与本地存储

凭据文件保存玩家用户名、密码及登录后轮换的令牌，仅发送到选定的 HTTPS 账号中心。默认地址为 `https://new2037.earth2037.com/account-api`。入服票据发送到该账号中心返回的 WSS 地址，当前国内 `s1` 使用 `new2037.9235.net`，国际 `en1` 使用 `new2037.earth2037.com`。不要把账号地址改成未经核实的站点。

密码与认证令牌不进入工具返回值、游戏缓存或操作回执。一个凭据文件只供一个网关进程使用。缓存与回执保存在本机私有目录，不上传到 ClawHub，也没有额外统计服务。

私有凭据 JSON 未加密。严格文件权限可限制其他本机用户访问，但不能抵御当前系统账号被入侵；不要分享或上传该文件。

| 环境变量 | 用途 |
|---|---|
| `EARTH2037_CREDENTIAL_FILE` | 本机私有凭据 JSON 的绝对路径 |
| `EARTH2037_ACCOUNT_URL` | 默认使用上面的独立账号地址 |
| `EARTH2037_STATE_DIR` | 私有缓存与回执；setup 配置为 `~/.earth2037-agent/state` |
| `EARTH2037_READ_ONLY` | 默认只读，只有显式设 `0` 才开放写操作 |
| `EARTH2037_LOCALE` | 语言，例如 `zh-CN` 或其他已支持语言 |
| `EARTH2037_CHANNEL` | 默认 `direct`，不用于绕过渠道限制 |
| `EARTH2037_RUNTIME_PLATFORM` | 自动识别 macos、windows；Linux 使用 web |

离线清单、参数说明、坐标换算不需要账号。公开服务器目录也不需登录。查询角色实时游戏状态需要进入角色，即使只读也可能替换手机或网页连接，须符合玩家的接管意图。

## 启用已授权的游戏操作

玩家授权操作后，在自己的终端运行：

```bash
node tools/setup.mjs --locale zh-CN --config-only --allow-writes
```

合并生成的配置后重启对应 MCP 进程。已配置的条目也可只把 `EARTH2037_READ_ONLY` 设为 `0`。此开关开放玩家权限内的游戏操作、注册和建角，不授予后台管理权限；仍须遵守目标、预算和操作范围。设为 `1` 可恢复只读。

账号注销/重置和充值流程不在此开关范围内。`resetaccount`、`paypal`、`paypalerr`、`googlebilling`、`gfan_pay`、`joincard` 在发送报文、写入回执前一律返回 `official_client_required`，请在官方客户端操作。没有配置开关可在网关中解锁这些协议；原始参数执行和直接 socket 发送同样受限，正常玩法流程不变。另一个内部诊断 `test` 在同样两层固定返回 `unsupported_command`，不随写入开关解锁；连接状态使用 `earth2037_status` 查询。

## 不配置 MCP，直接使用 CLI

命令行不会自动读取生成的 MCP 配置，需显式传入路径：

```bash
export EARTH2037_CREDENTIAL_FILE="$HOME/.earth2037-agent/credentials.json"
export EARTH2037_STATE_DIR="$HOME/.earth2037-agent/state"
export EARTH2037_READ_ONLY=1
node src/cli.mjs describe arrivalheroexplore
node src/cli.mjs run < requests.ndjson
```

玩家已授权接管国服角色时，`requests.ndjson` 示例：

```json
{"tool":"earth2037_enter","arguments":{"serverId":"s1","acceptSessionTakeover":true}}
{"tool":"earth2037_show","arguments":{"section":"city"}}
{"tool":"earth2037_disconnect","arguments":{}}
```

国际服选择 `en1`，不自动替换玩家选择。相关调用放在同一进程内。prepare 的 planId 需要读取实际返回值，不能提前写一个假 ID 到完整输入文件：执行这种流程时优先 MCP，或保持 CLI 进程打开，检查前一条响应后再写下一行。密码不放到 NDJSON、命令参数或聊天中。CLI 写操作同样需要显式设置 `EARTH2037_READ_ONLY=0`。

## 从 1.x 升级

先保留旧配置，再在干净安装目录使用新版运行文件。旧 Python 命令、SK-key、`EARTH2037_API_BASE` 和 `EARTH2037_TOKEN` 不会自动导入。使用新版账号中心的用户名和密码；游客或第三方登录账号先在官方客户端绑定密码，避免另建账号而看不到已有角色。

已有 `EARTH2037_ACCOUNT_URL` 会覆盖默认值，要把其中旧入口改成独立地址，并合并新版运行路径。国内网页域名的切换不再改变此包默认账号入口，但账号中心和对应游戏服务器本身仍须可用。

`2037` 中文版和 `earth2037` 英文版功能一致，选择一种语言即可，避免重复 MCP 条目和抢占登录。升级不删除旧凭据文件，也不修改玩家存档。
