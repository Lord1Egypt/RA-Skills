# 滴答清单 MCP 设置引导

检测到你还没有连接滴答清单，请按下面步骤完成配置。

默认先看 [`references/mcp-client-setup.md`](../references/mcp-client-setup.md)，按你当前使用的客户端走远程 MCP 最短路径。
如果用户明确说“想像 Getnote 一样自动生成授权链接并落盘凭证”，再切到 [`references/openapi-auth-setup.md`](../references/openapi-auth-setup.md)。

## 第一步：OpenClaw 优先半自动接入

如果当前环境是 OpenClaw，并且用户允许修改本地配置，优先自动把 dida365 写入 OpenClaw 的 `mcpServers`，不要只停留在口头指导。

推荐写入结构：

```json
{
  "mcpServers": {
    "dida365": {
      "transport": {
        "type": "http",
        "url": "https://mcp.dida365.com"
      }
    }
  }
}
```

写入后，优先引导用户在 OpenClaw 的 MCP / Tools / 依赖面板中点击一次 `Connect`、`Authorize`、`Sign in` 或 `Enable`，再继续后续任务。

如果当前运行环境支持浏览器自动化，可以帮助把 OpenClaw 或浏览器切到前台，并跟随普通网页按钮；但账号登录、通行密钥、验证码和 2FA 必须由用户本人完成。

不要尝试把 `/mcp` 当成 shell 命令执行。`/mcp` 只在 Claude Code 会话里有效，不是终端里的普通命令。

## 第二步：优先直接授权

如果你当前用的是 OpenClaw、ClawHub 或其他带 MCP 依赖面板的客户端，优先找页面里的 `dida365` 连接按钮：

- `Connect`
- `Authorize`
- `Sign in`
- `Enable`

直接点一次，浏览器完成 OAuth 授权后再回来即可。这个场景下，不要默认要求用户先执行 Claude 命令，也不要裸打开 `https://mcp.dida365.com/oauth/authorize` 这类缺少客户端上下文的地址。

## 第三步：如果没有内置按钮，再手动添加 MCP

通用配置如下：

- 服务名：`dida365`
- URL：`https://mcp.dida365.com`
- 传输方式：`HTTP` 或 `streamable_http`

如果你用的是 Claude Code，本地兜底命令是：

```bash
claude mcp add --transport http dida365 https://mcp.dida365.com
```

添加完成后，再按客户端提示打开浏览器完成授权。

## 可选路线：滴答开放平台本地 OAuth

如果用户不想完全依赖远程 MCP 客户端授权，而是想像 Getnote 一样“点链接授权后自动写本地凭证”，可以改走滴答开放平台路线：

1. 让用户去开放平台创建应用
2. 回调地址填写：`http://localhost:38000/callback`
3. 让用户提供 `client_id` 和 `client_secret`
4. 使用本地 helper 生成授权链接并监听 callback
5. 授权成功后自动写入 `~/.dida-coach/dida-openapi.env`

对应脚本：

```bash
python3 scripts/dida_openapi_oauth.py \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET \
  --open-browser
```

如果你用的是下面这些客户端，优先按它们的原生入口配置，不要自己猜：

- `Claude Desktop`: `Customize > Connectors > Add Connector`
- `ChatGPT`: `设置 > 应用 > 高级设置 > 开发人员模式 > 创建应用`
- `Cursor`: `Settings > Tools & MCP > Add Custom MCP`
- `VS Code`: 命令面板运行 `Add Server`

## 第四步：回到教练流程

授权完成后，告诉我“已连接”或“继续”，我会自动重新检测，并进入以下任一流程：

- 拆长期目标
- 安排时间盒
- 建立本地生产力系统
- 做日复盘
- 做周复盘
- 处理延期或改时间

## 常见问题

Q: 为什么不能只弹浏览器授权？
A: 浏览器授权只能解决 OAuth，不能凭空替客户端注册 MCP 服务器。OpenClaw 这类客户端通常要先有本地 `mcpServers` 配置，再通过浏览器把 dida365 账号授权给这个已注册的服务器。

Q: 能不能直接用命令行执行 `/mcp`？
A: 不能。`/mcp` 是 Claude Code 会话里的 slash command，不是 shell 命令。能自动化的是“写 MCP 配置 + 打开或引导授权页面”，不是把 `/mcp` 直接当终端命令跑。

Q: 怎么最快判断自己该走哪条路？
A: 先看当前页面里有没有 `Connect`、`Authorize`、`Sign in`。有就直接点；没有再看你用的是 Claude Desktop、ChatGPT、Cursor、VS Code 还是 Claude Code，对照速查表操作。

Q: 授权页面打不开怎么办？
A: 先检查网络，必要时把客户端弹出的链接复制到浏览器手动打开。

Q: 能不能做得像 Getnote 一样，一点授权就自动写配置？
A: 对远程 MCP 路线不完全行，因为 OAuth/token 由 MCP 客户端接管。要接近 Getnote 的体验，需要改走滴答开放平台本地 OAuth 路线，用自己的 `client_id/client_secret` 和 `localhost` 回调完成自动落盘。

Q: 明明配过但还是提示未连接？
A: 常见原因是授权过期，或者当前客户端没有把 dida365 注册到本地配置。优先重新点一次浏览器授权；如果还是不行，再检查客户端的 MCP 配置里是否真的存在 dida365，尤其是 OpenClaw 的 `transport.type=http` 和 `transport.url` 是否正确。
