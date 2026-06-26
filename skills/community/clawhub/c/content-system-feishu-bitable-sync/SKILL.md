---
name: feishu-bitable-sync
description: Sync a local `wechat-report` result into Feishu Bitable after the user has reviewed the report and confirmed the sync.
---

# feishu-bitable-sync

本 skill 不会自动触发，只有在用户明确确认“发送到飞书”后才运行。

支持输入：

- `content-production/inbox/YYYYMMDD-{slug}-wechat-report.md`
- `content-production/inbox/raw/wechat-report/YYYY-MM-DD/{slug}.json`

运行前需要配置环境变量：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_BITABLE_APP_TOKEN`
- `FEISHU_BITABLE_TABLE_ID`
- 可选：`FEISHU_SYNC_AUTH_MODE`，默认 `user`
- 可选：`FEISHU_OAUTH_REDIRECT_URI`，默认 `http://127.0.0.1:14578/callback`

默认行为：

- 优先读取本机缓存的飞书 `user_access_token`
- 若还未授权，会落一份 `auth_required` 回执，并提示先运行 `feishu-user-auth`
- 若 token 刷新失败或飞书写入失败，会额外导出 CSV 兜底文件

输出：

- `content-production/published/YYYYMMDD-{slug}-feishu-sync.md`
- 失败兜底时：`content-production/published/YYYYMMDD-{slug}-feishu-import.csv`

同步策略：

- 每篇文章一行
- 使用 `source_url` 去重
- 重复同步会更新已有行，而不是重复新增
