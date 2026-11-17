---
name: exportdou
description: 粘贴抖音视频链接，用抖评岛（ExportDou）导出评论和回复，保存为 CSV 或 Excel，也可先预览少量评论，分析用户反馈、产品问题和选题。用户需要抖音评论导出、评论采集、评论分析或继续已有导出任务时使用。需要抖评岛账号和可用积分。
---

# 抖音评论导出 · 抖评岛

把用户提供的公开抖音视频链接或分享文案交给抖评岛（ExportDou），导出评论供用户下载或分析。只处理公开可访问的视频，不索要抖音 Cookie 或抖音账号登录状态。

需要 Node.js 18.17 及以上版本和 `npx`。下面的命令固定使用已发布的 `exportdou@1.0.3`，默认 API 为 `https://api.exportdou.cn/v1`。若用户明确配置了 `EXPORTDOU_API_URL`，尊重该设置。用用户的语言解释结果，命令、任务 ID 和错误码保持原样。

## 先确认账号

本次会话第一次操作前检查登录状态：

```bash
npx exportdou@1.0.3 whoami --json
```

未登录时运行：

```bash
npx exportdou@1.0.3 login --json
```

把 CLI 打印的授权地址交给用户，在抖评岛网页完成确认。登录命令会等待授权，应保留这次进程并读取后续输出，不要反复启动登录。授权成功后 CLI 会保存凭证。用户主动通过安全环境变量提供 API Key 时，可使用 `EXPORTDOU_API_KEY`；不要让用户把 Key 发到对话中，也不要输出 Key。

## 确认要导出哪些评论

- 用户指定数量，就按该数量导出；只想先看样本或做初步分析时，默认取 100 条。
- 正式导出但没有说明数量，也没有要求全部时，先问需要多少条。
- 默认导出一级评论；用户需要楼中楼回复时再加 `--replies`。一级评论和回复共用一个总行数上限。
- “全部一级评论”：先查看视频信息，再使用 `--all`。CLI 会检查公开评论数、20 万条上限和可用积分。
- **`--all` 不能和 `--replies` 一起使用。** 公开计数不能覆盖每条回复。需要“全部评论和回复”时，说明这一限制，让用户确定总行数，再用 `--limit N --replies`，不要承诺一定采全。
- 默认 CSV；用户要求 Excel 时使用 `--format xlsx`。回复和 Excel 功能可能需要对应套餐，以服务返回的权限为准。

查看视频信息、公开评论数和少量样本：

```bash
npx exportdou@1.0.3 inspect "<抖音链接或分享文案>" --json
```

## 提交一次，保存任务 ID

下面的 1000 是示例，实际使用用户确定的数量：

```bash
EXPORTDOU_CLIENT_NAME=exportdou-skill npx exportdou@1.0.3 export "<抖音链接或分享文案>" --limit 1000 --json
```

若需要回复和 Excel，在同一条创建命令里加上 `--replies --format xlsx`。`--limit` 允许 1 至 200000；不要同时传 `--all` 和 `--limit`。

保存输出中的 `taskId`。创建命令立即返回，任务在云端继续执行。**不要重复提交原链接来查询进度。** CLI 在安全重试时会复用同一个请求标识，并尝试找回网络中断时已受理的任务。若仍未拿到任务 ID，先查历史记录，不要套重试循环重新创建。

等待返回的建议间隔后，用同一个 ID 查进度：

```bash
npx exportdou@1.0.3 status "<task-id>" --json
```

`queued`、`processing`、`rendering` 表示仍在进行；按 `retryAfterSeconds` 再查。`completed`、`partial`、`failed`、`cancelled` 表示本轮已结束，停止轮询。默认不要加 `--wait`；只有用户明确希望终端持续等待时才使用它。

## 只导出了一部分怎么办

`partial` 表示已有文件可用，但采集没有完成。先说明实际导出了多少，以及未完成的原因。用户仍需要余下结果时，继续原任务：

```bash
npx exportdou@1.0.3 resume "<task-id>" --json
```

此命令从保存的断点继续，仅预留剩余行数所需积分。之后仍用同一个任务 ID 查进度。如果断点已过期或任务不允许继续，说明原因，保留已有结果；不要擅自重建一个收费任务。

## 查看样本、下载文件

用户要分析时，先取少量结构化评论：

```bash
npx exportdou@1.0.3 preview "<task-id>" --limit 20 --json
```

每次最多预览 50 条。分析时说明样本数量和范围，不要把小样本结论说成全部评论的结论，也不要把整个大型导出文件塞进对话上下文。

下载完整文件：

```bash
npx exportdou@1.0.3 download "<task-id>" --output comments.csv --json
```

Excel 任务使用 `.xlsx` 文件名；下载不会改变创建时选定的文件格式。CLI 会校验文件大小和 SHA-256，再将临时文件改名为最终文件。目标文件已存在时，换一个文件名；只有用户同意覆盖该文件后才加 `--force`。

交付时提供本地文件，并说明实际行数、是否包含回复、是否只完成了一部分。不要把临时签名下载地址、API Key、服务商原始响应或内部游标发到对话中。

## 积分、历史和多个链接

```bash
npx exportdou@1.0.3 credits --json
npx exportdou@1.0.3 history --limit 20 --json
npx exportdou@1.0.3 cancel "<task-id>" --json
```

创建时预留请求行数对应的积分，结束后按实际导出行数结算并释放差额。积分不足时说明缺口，给出[充值页面](https://exportdou.cn/pricing)，停止重复提交。

多个链接按顺序逐个处理，分别保存任务 ID。不要用 shell 循环、`xargs`、后台进程或并行 CLI 提交；遇到并发上限时等待已有任务结束，不要为腾出名额擅自取消用户的任务。

## 常见问题怎么处理

保留 JSON 标准输出和标准错误输出，先看实际错误码再决定下一步：

| 情况 | 处理方式 |
| --- | --- |
| `authentication_required` / `unauthorized` | 重新登录并让用户完成网页授权。 |
| `conflicting_options` | 检查是否混用了 `--all`、`--replies` 或 `--limit`，按上面的数量规则修正。 |
| `comment_count_unavailable` | 无法确定全部数量，改用用户确定的 `--limit`。 |
| `video_unavailable` | 说明链接当前不可用，请用户提供另一个公开链接。 |
| `paid_feature_required` | 说明回复或 Excel 的套餐要求；按用户选择升级，或改用一级评论 CSV。 |
| `rate_limited` / `concurrency_limit` | 等待建议间隔或已有任务结束，再查询；不要重建任务。 |
| 创建时 `network_error` / `request_timeout` | 先查历史找回可能已创建的任务，不要盲目重提。 |
| `resume_already_active` | 原任务已在继续，直接查询同一个 ID。 |
| `resume_pages_missing` 或其他 `resume_*` 拒绝原因 | 说明断点过期或不可继续，交付已有文件。 |
| `export_not_ready` | 按建议间隔查询原任务。 |
| `checksum_mismatch` / `size_mismatch` | 重新下载同一个结果，不要重新导出。 |

其他参数可运行 `npx exportdou@1.0.3 --help` 查看。抖评岛不是抖音官方服务，实际可导出范围取决于公开视频和服务返回结果。

## 相关链接

- [抖评岛官网](https://exportdou.cn)
- [CLI 使用说明](https://exportdou.cn/developers#agent)
- [API 文档](https://exportdou.cn/developers)
- [套餐和积分](https://exportdou.cn/pricing)
- [CLI 源码](https://github.com/wegoft/exportdou-agent-tools)
