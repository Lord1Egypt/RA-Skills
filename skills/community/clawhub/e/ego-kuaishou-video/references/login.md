# 快手创作者平台登录（Ego Lite）

本技能**每次发布前**必须先跑 `scripts/check-login.mjs`。技能自己检查登录，不要另搞 cookie-healthcheck。

## soft-fail

`login_required: true`、退出码 `2`，并带 `how_to_login` / `how_to_login_zh`。Agent **立刻停**，把说明给人，**不要**填密码、不要自动化扫码、不要粘贴 Cookie。

`ego-browser` 不在 PATH 上时同样是退出码 `2`（soft-fail），并告诉人去装 Ego Lite。不要把缺浏览器当成硬错误去重试命令。

判定信号：

- 未登录：正文出现「扫码登录」「二维码登录」或「请登录」，或 URL 在登录 / passport 页。
- 已登录：离开登录墙，正文出现创作者后台（「上传视频」「发布作品」「作品管理」「评论管理」「创作者服务平台」）。文档标题里的产品名不算登录。

## 人要做的事

1. 打开 **Ego Lite**（`ego-browser` 用的同一个配置档）。
2. 打开 https://cp.kuaishou.com/article/publish/video ，用快手 App 扫二维码。
3. 确认创作者账号无误后，让 Agent **重新**跑 `check-login`；exit 0 再继续上传。

可选：`--keep` 把标签留在登录页并 `handOff()`，方便人当面扫码。默认 `finish({ keep: [] })`。

发布或评论脚本如果自己撞上登录墙，会 `handOff()` 然后以退出码 `2` 结束。Agent 仍然要先跑 check-login，不要靠发布脚本的失败来发现未登录。
