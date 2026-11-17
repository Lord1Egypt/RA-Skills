# Agent 客户端兼容性

仅在安装本地 OpenAPI 包或排查工具连接时读取。

- 运行环境：Node.js 18 或更高版本。
- 本地 MCP 入口：`dist/550w-mcp.cjs`，使用标准输入输出传输；将包根目录设为工作目录，或使用入口的绝对路径。
- 必需凭据：`SUBTITLE_REMOVER_USER_NO` 和 `SUBTITLE_REMOVER_API_KEY`。国内发行包已固定国内服务，不要求用户设置区域。
- 网络：允许访问 `www.550wai.cn`；本地文件操作还需要读取用户所选媒体的权限。
- WorkBuddy：使用单独发布的远程 OAuth 连接器，不使用此 API Key 包。
- Claude Desktop、Cursor、Windsurf 等使用 `mcpServers` 结构的客户端：以 `node` 启动入口并安全注入两个凭据变量。
- Codex 桌面版、命令行和 IDE：配置本地标准输入输出 MCP 服务、入口路径、工作目录与凭据变量。
- VS Code/GitHub Copilot：使用其 `servers` 配置结构，并通过安全输入变量保存凭据。
- OpenClaw 等 Agent Skills 客户端：安装 `ai-subtitle-remover` 目录并读取根目录的 `SKILL.md`；可调用工具仍由包内 MCP 服务提供。
- 本包使用本地标准输入输出连接。只支持远程 HTTP MCP 的浏览器或 SaaS Agent 需要单独部署带鉴权的网关。

只发布到国内技能商店时使用此包。国外或面向全球的技能商店使用全球发行包。
