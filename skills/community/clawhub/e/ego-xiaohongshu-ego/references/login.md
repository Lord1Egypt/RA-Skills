# 小红书创作者登录（Ego Lite）

本技能**每次发布前**必须先跑 `scripts/check-login.mjs`。技能自己检查登录，不要另做 cookie-healthcheck。

`www.xiaohongshu.com` 和 `creator.xiaohongshu.com` 可以不是同一个账号。只认创作者页眉上的昵称。

## soft-fail

`login_required: true` 或 `account_mismatch: true` 都是退出码 `2`，并带 `how_to_login` / `how_to_login_zh`。Agent **立刻停**。不要填密码，不要粘贴 Cookie，不要改用 Playwright。

`ego-browser` 不在 PATH 上时同样是退出码 `2`。

判定：

- 未登录：URL 在 `/login`，或正文出现「扫码登录」「二维码登录」「请使用小红书App扫码」。
- 已登录：人在 `creator.xiaohongshu.com`，离开登录墙，并且能看到创作者后台（发布笔记、笔记管理、上传视频、设置封面）或页眉昵称。
- `--expect-account`：页眉昵称必须与参数完全一致。页眉是别的账号时，即使正文里出现了期望昵称，也算不匹配。

## 人要做的事

1. 打开 **Ego Lite**（`ego-browser` 用的同一个配置档）。
2. 打开 https://creator.xiaohongshu.com/ ，登录要发布的创作者账号。
3. 看页眉昵称。不对就在 Ego 里换到正确账号。
4. 让 Agent 重新跑 `check-login`。退出码 0 之后，先看计划，确认后再加 `--yes`。

可选：`--keep` 把标签留着并 `handOff()`。默认 `finish({ keep: [] })`。

check-login 使用任务空间 `xiaohongshu-ego-login`。发布使用 `xiaohongshu-ego`。改封面使用 `xiaohongshu-ego-edit`。
