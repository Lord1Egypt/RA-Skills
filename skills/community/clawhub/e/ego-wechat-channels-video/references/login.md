# 视频号助手登录（Ego Lite）

视频号登录态**过期很快**。本技能**每次发布前**必须先跑 `scripts/check-login.mjs`。技能自己检查登录，不要另搞 cookie-healthcheck。

## soft-fail

`login_required: true`、退出码 `2`，并带 `how_to_login` / `how_to_login_zh`。Agent **立刻停**，把说明给人，**不要**填密码、不要自动化扫码、不要粘贴 Cookie。

判定信号：

- 未登录：URL 含 `login.html`，或页面主要是扫码登录。
- 已登录：离开 login 页，且出现「内容管理 / 发表视频 / 草稿」等平台壳，或常见登录 Cookie 名可见。

## 人要做的事

1. 打开 **Ego Lite**（`ego-browser` 用的同一个配置档）。
2. 打开 https://channels.weixin.qq.com ，用微信扫二维码。
3. 「加载失败，点击重试」可忽略：那是探本地微信客户端失败，二维码在跨域 iframe 里。
4. 确认账号无误后，让 Agent **重新**跑 `check-login`；exit 0 再继续上传/填表。

可选：`--keep` 把标签留在登录页并 `handOff()`，方便人当面扫码。
