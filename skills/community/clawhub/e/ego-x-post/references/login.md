# X 登录（Ego Lite）

本技能**每次发帖之前**必须先跑 `scripts/check-login.mjs`。技能自己检查登录，不要另做 cookie-healthcheck。

在 Ego 里登录 x.com 之后才能发帖。Agent 要把 `login_tip` 告诉用户。

## soft-fail

`login_required: true`、退出码 `2`，并带 `how_to_login` / `how_to_login_zh`。Agent **立刻停**，把说明给人，**不要**填密码、不要粘贴 Cookie、不要改用 Playwright。

`ego-browser` 不在 PATH 上时，同样是退出码 `2`。不要把缺浏览器当成硬错误去重试命令。

判定信号（2026-11-04 在已登录的 x.com/home 上观察到）：

- 未登录：URL 落在 `/i/flow/login`、`/login`，或正文出现 “Sign in to X” / “登录 X”。
- 已登录：离开登录墙，并且浏览器 Cookie 罐里有 HttpOnly 的 `auth_token`。`document.cookie` 里通常能看到 `ct0`，但 **`ct0` 单独存在不算登录**（未登录访客也有）。
- Cookie 罐读不到时，才退回到主页壳：标题含「主页」或 “Home”，并且个人资料链接是 `/<screen_name>`。
- 文档标题单独一个 “X” **不算**已登录。空白页先重画一次 `https://x.com/home`，再判断。

Cookie 值不打印、不导出。`ct0` 只在 `page.fetch` 的 `x-csrf-token` 里使用，不进入 stdout。

## 人要做的事

1. 打开 **Ego Lite**（`ego-browser` 用的同一个配置档）。
2. 打开 https://x.com/home ，登录要发帖的账号。
3. 让 Agent **重新**跑 `check-login`；退出码 0 再继续。先看草稿，确认后再 `--yes`。

可选：`--keep` 把标签留在登录页并 `handOff()`。默认 `finish({ keep: [] })`。

check-login 使用任务空间 `x-post-login-check`。发帖使用 `x-post`。两者互不关闭。
