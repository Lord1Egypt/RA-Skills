# Agent compatibility / Agent 兼容性

Read this reference when installing the package outside WorkBuddy or diagnosing an MCP client.

仅在 WorkBuddy 之外安装，或排查 MCP 客户端兼容性时读取。

## Runtime contract / 运行契约

- Runtime: Node.js 18 or newer / Node.js 18 或更高版本。
- Transport: local MCP over stdio using newline-delimited JSON-RPC. The server writes protocol messages only to stdout / 使用 stdio 的本地 MCP，协议为按行分隔的 JSON-RPC；服务端仅向 stdout 写协议消息。
- Entrypoint: `dist/550w-mcp.cjs`; set the package root as `cwd` or use an absolute entrypoint path / 入口是 `dist/550w-mcp.cjs`；将包根目录设为 `cwd`，或使用入口绝对路径。
- Credentials: `SUBTITLE_REMOVER_USER_NO` and `SUBTITLE_REMOVER_API_KEY`. The package selects its service region; users do not need a region setting / 凭据使用上述两个环境变量；发行包已决定服务区域，用户无需设置地区。
- Network access: allow HTTPS access to `www.550wai.cn`; local-file tools also need read access to the selected media / 需要允许访问 `www.550wai.cn`；本地文件工具还需获得所选媒体的读取权限。

## Client families / 客户端类型

- WorkBuddy: use the bundled `mcp.json`, `token-schema.json`, and connector metadata. Its token form maps credentials into the MCP process environment / 使用包内 WorkBuddy 配置，由凭据表单注入环境变量。
- Claude Desktop, Cursor, Windsurf, and clients using the common `mcpServers` shape: launch `node` with the absolute `dist/550w-mcp.cjs` path and pass credentials through `env` / 使用常见 `mcpServers` 结构的客户端，以 `node` 启动绝对入口路径并通过 `env` 传入凭据。
- Codex desktop, CLI, and IDE: configure a local stdio server with command, args, cwd, and forwarded environment variables / 使用本地 stdio 配置，提供 command、args、cwd 与环境变量。
- VS Code and GitHub Copilot: use the `servers` configuration shape rather than `mcpServers`; prefer secure input variables for credentials / 使用 `servers` 结构，并优先使用安全输入变量保存凭据。
- OpenClaw and other Agent Skills clients: install the `ai-subtitle-remover` package directory and discover its root `SKILL.md`; the bundled MCP server remains the source of callable tools / 安装 `ai-subtitle-remover` 目录并读取根目录的 `SKILL.md`，可调用工具仍由包内 MCP 服务提供。

## Portability boundaries / 可移植性边界

- Global MCP tools accept an optional `locale` for localized messages. The global package defaults to English; the domestic package responds in Chinese. Neither package asks for a region parameter / 全球版 MCP 工具可选传入 `locale`，默认英语；国内版使用中文。两版都不要求设置地区。
- Tool schemas are JSON-Schema compatible and expose MCP safety annotations. Read-only tools are marked read-only; task deletion is marked destructive / 工具 schema 兼容 JSON Schema，并提供 MCP 安全标记；查询类工具为只读，删除任务标记为破坏性操作。
- This package is a local stdio server. Browser-only or SaaS agents that accept only remote Streamable HTTP MCP cannot connect to the ZIP directly; deploy a separately secured HTTP MCP gateway instead / 本包是本地 stdio 服务。仅接受远程 Streamable HTTP MCP 的浏览器或 SaaS Agent 不能直接连接 ZIP，需要另行部署带鉴权的 HTTP MCP 网关。
- Do not translate one client's configuration file directly into another without changing its top-level schema (`mcpServers` versus `servers` or TOML) / 不要在未调整顶层结构时直接复制不同客户端的配置。
