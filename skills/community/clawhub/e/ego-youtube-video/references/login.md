# YouTube Studio 登录（Ego Lite）

本技能**每次发布前**必须先跑 `scripts/check-login.mjs`。技能自己检查登录，不要另搞 cookie-healthcheck。

在 Ego 里登录 YouTube 之后效果最好。Agent 要把 `login_tip` 告诉用户。

## soft-fail

`login_required: true`、退出码 `2`，并带 `how_to_login` / `how_to_login_zh`。Agent **立刻停**，把说明给人，**不要**填密码、不要自动化过登录、不要粘贴 Cookie。

`ego-browser` 不在 PATH 上，或本机没装 Ego Lite 时，同样是退出码 `2`（soft-fail），并告诉人去装。不要把缺浏览器当成硬错误去重试命令。

判定信号：

- 未登录：URL 在 `accounts.google.com`、`/signin` 或 `ServiceLogin`，或正文出现 “Sign in to YouTube”“Choose an account”“使用 Google 账号登录”“选择账号”。
- 已登录：离开登录墙，并且正文出现 Studio 后台（“YouTube Studio”“Upload videos”“Analytics”“Dashboard”“上传视频”“YouTube 工作室”“数据分析”），或有登录 Cookie（`LOGIN_INFO` / `SAPISID` / `__Secure-3PSID`）。
- 文档标题里的 “YouTube Studio” **不算**已登录。空白页先重画一次，再判断。

## 人要做的事

1. 打开 **Ego Lite**（`ego-browser` 用的同一个配置档）。
2. 打开 https://studio.youtube.com/ ，登录要发布的 YouTube 频道。
3. 确认频道无误后，让 Agent **重新**跑 `check-login`；exit 0 再继续上传。

可选：`--keep` 把标签留在登录页并 `handOff()`，方便人当面登录。默认 `finish({ keep: [] })`。

发布脚本如果自己撞上登录墙：没带 `--keep` 时关掉 space 并以退出码 `2` 结束；带了 `--keep` 才 `handOff()`。Agent 仍然要先跑 check-login，不要靠发布脚本的失败来发现未登录。
