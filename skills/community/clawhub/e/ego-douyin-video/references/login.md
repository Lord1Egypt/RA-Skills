# 抖音创作者中心登录（Ego Lite）

本技能**每次发布前**必须先跑 `scripts/check-login.mjs`。技能自己检查登录，不要另搞 cookie-healthcheck。

在 Ego 里登录抖音之后效果更好。Agent 要把 `login_tip` 告诉用户。

## soft-fail

`login_required: true`、退出码 `2`，并带 `how_to_login` / `how_to_login_zh`。Agent **立刻停**，把说明给人，**不要**填密码、不要自动化扫码、不要粘贴 Cookie。

`ego-browser` 不在 PATH 上，或本机没装 Ego Lite 时，同样是退出码 `2`（soft-fail），并告诉人去装。不要把缺浏览器当成硬错误去重命令。

判定信号（看正文，不看文档标题）：

- 未登录：正文出现「扫码登录」「二维码登录」或「请登录」，或 URL 在 `/login`、`passport.douyin.com`、`sso.douyin.com`。
- 已登录：离开登录墙，并且正文出现上传页（「点击上传」「上传视频」）或发布表单（「作品描述」「添加作品简介」）。
- 文档标题里的「抖音」**不算**已登录。空白页先重画一次，再判断。Cookie 只记在 signals 里，不能单独当成已登录。

## 人要做的事

1. 打开 **Ego Lite**（`ego-browser` 用的同一个配置档）。
2. 打开 https://creator.douyin.com/creator-micro/content/upload ，用抖音 App 扫二维码。
3. 确认创作者账号无误后，让 Agent **重新**跑 `check-login`；exit 0 再继续上传。

可选：`--keep` 把标签留在登录页并 `handOff()`，方便人当面扫码。默认 `finish({ keep: [] })`。

发布脚本如果自己撞上登录墙，会 `handOff()` 并以退出码 `2` 结束，**不**调用 `finish`，这样扫码后可以带 `spaceId` 续跑。Agent 仍然要先跑 check-login，不要靠发布脚本的失败来发现未登录。
