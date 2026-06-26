---
name: feishu-user-auth
description: Complete one-time Feishu browser authorization and cache a local `user_access_token` so later `feishu-bitable-sync` runs can write Bitable rows as the current user instead of app identity.
---

# feishu-user-auth

在当前租户下，如果 `tenant_access_token` 不能稳定写多维表，先运行这个 skill。

它会：

- 打开浏览器进入飞书授权页
- 通过本地回调地址接收授权码
- 换取 `user_access_token + refresh_token`
- 缓存在本机 `~/.codex/feishu-auth/content-system-sync.json`

运行前请确认：

- 已配置 `FEISHU_APP_ID`
- 已配置 `FEISHU_APP_SECRET`
- 飞书应用已开通网页应用能力
- 飞书应用回调地址已包含 `http://127.0.0.1:14578/callback`

输出：

- `content-production/published/YYYYMMDD-feishu-user-auth.md`

授权成功后，再运行 `feishu-bitable-sync` 即可按用户身份写多维表。
