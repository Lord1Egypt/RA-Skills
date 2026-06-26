# Site Setup

## When to read this file

在下面场景读取本文件：

- 当前环境尚未验证 Archtree MCP 是否可用
- 需要登录、注册或生成 token
- 需要在网站上确认写入结果是否可见
- MCP 返回认证错误，需要回站点检查登录状态或 token

以下流程基于默认实例 `archtree.cn` 的当前界面；若目标实例的界面文案、入口位置或 token 获取流程不同，以实际页面为准。

## Default instance

Unless the user specifies another instance, assume:

- Site: `https://archtree.cn`
- MCP endpoint: `https://archtree.cn/mcp`
- Auth: Bearer Token

推荐 MCP 配置示例：

```json
{
  "mcpServers": {
    "archtree": {
      "type": "http",
      "url": "https://archtree.cn/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

## Website flow

1. 打开目标 Archtree 站点首页或用户指定页面。
2. 如果未登录，点击右上角“登录 / 注册”。
3. 没有账号时进入注册面板；已有账号时进入登录面板。
4. 登录后点击右上角用户名，进入“帐号中心”。
5. 在“API 访问”区域生成、复制或检查 token。
6. 将 token 配置到 MCP 连接中；如果环境支持自定义请求头，使用 `Authorization: Bearer <token>`。

## Verification rules

- 如果已经可以成功列出 Archtree tools，说明 MCP 基本连通。
- 如果读取类工具也能正常返回结果，说明连接不只是握手成功，而是可实际工作。
- 如果工具列表为空、返回认证错误或写入报权限问题，先回网站检查账号状态和 token。
- 只有在需要可视化确认、登录管理或 token 管理时，才回到网站流程；不要在 MCP 已可用时强行改用浏览器写入。

## Security notes

- 不要把完整 token 直接写进聊天、日志、截图、提交或公开文档。
- 只有在用户明确要求时，才展示完整 token。
- 如果要举例配置，优先使用占位符而非真实密钥。
