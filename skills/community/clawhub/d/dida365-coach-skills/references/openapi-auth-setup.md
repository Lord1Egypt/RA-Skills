# 滴答开放平台本地 OAuth 配置

如果你希望接入体验更像 Getnote，可以走这条“本地 OAuth + 本地 `.env` 落盘”路线。

## 适用场景

- 你愿意在滴答开放平台创建自己的应用
- 你希望 Agent 生成授权链接、监听本地 callback，并自动写入凭证
- 你接受这条路线使用的是滴答 Open API，而不是 `mcp.dida365.com` 远程 MCP 的内置授权

## 方式一：本地 OAuth 授权

1. 打开滴答开放平台文档入口：
   - `https://developer.dida365.com/docs#/openapi`
2. 创建一个应用
3. 在应用设置里把 OAuth Redirect URL 填成：
   - `http://localhost:38000/callback`
4. 复制 `client_id` 和 `client_secret`
5. 让 Agent 执行本地 OAuth helper：

```bash
python3 scripts/dida_openapi_oauth.py \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET \
  --open-browser
```

这个 helper 会：

- 生成授权链接
- 可选自动打开浏览器
- 在本地监听 `localhost:38000/callback`
- 授权成功后自动换 token
- 把凭证写入 `~/.dida-coach/dida-openapi.env`

## 方式二：手动配置

如果你已经拿到了凭证，也可以直接写入：

- `DIDA_OPENAPI_CLIENT_ID`
- `DIDA_OPENAPI_CLIENT_SECRET`
- `DIDA_OPENAPI_REDIRECT_URI`
- `DIDA_OPENAPI_ACCESS_TOKEN`
- `DIDA_OPENAPI_REFRESH_TOKEN`

默认文件位置：

- `~/.dida-coach/dida-openapi.env`

## 和远程 MCP 的区别

- 远程 MCP 路线：配置的是 `https://mcp.dida365.com`，OAuth 和 token 由客户端自己处理
- 本地 Open API 路线：配置的是你自己的开放平台应用，OAuth 由本地 helper 完成，并把凭证写到 `.env`

如果你只是想在 OpenClaw / ClawHub 里最快上手，优先继续用远程 MCP 路线。
如果你想做更像 Getnote 的“授权后自动写本地凭证”，再走这里的 Open API 路线。
