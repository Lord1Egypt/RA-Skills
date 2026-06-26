---
name: dataify-instagram-comment-by-posturl
description: "提交 Dataify Instagram Post Comment by Post URL Builder 任务。当用户需要 Instagram post comment collection tool、采集/抓取/爬取 Instagram 帖子评论或评论数据、按 post URL 采集 Instagram comments、创建 ins_comment_by-posturl 任务，或表达 Instagram 帖子评论采集/抓取、Instagram 评论采集/抓取、帖子评论采集/抓取、帖子 URL 评论采集等含义时使用。也用于接收 task_id/status、配置 DATAIFY_API_TOKEN 或排查此 Dataify Builder 请求。"
---

# Dataify Instagram Comment By Post URL

通过 Dataify Builder 按帖子 URL 提交 Instagram 帖子评论采集任务。提交成功后，向用户提供 `task_id`、返回或推断的状态，并告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看结果。

## API TOKEN 处理

使用 `DATAIFY_API_TOKEN` 作为长期保存的 token 名称。

- 如果用户在请求中提供了 token，则在本次运行中使用该 token。
- 如果未提供 token，先检查环境变量中是否已保存 `DATAIFY_API_TOKEN`。
- 如果本地已保存 `DATAIFY_API_TOKEN`，则直接使用，无需要求用户重新输入。
- 如果本地没有可用的 token，告知用户需要提供 Dataify API TOKEN。
- 如果用户没有 API TOKEN，告知他们可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录以获取。
- 如果用户已有 API TOKEN，告知他们可以在 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角找到。
- 用户提供 API TOKEN 后，如果本地未保存 `DATAIFY_API_TOKEN`，询问是否将其保存为 `DATAIFY_API_TOKEN` 以供将来使用。
- 如果用户想要保存，提供适合其 shell 的命令并要求用户执行；不要在未经确认的情况下静默保存 token。
- 没有 token 不要调用 Builder 接口。
- 在面向用户的说明中始终称其为 `API TOKEN`。本地保存时优先使用环境变量名 `DATAIFY_API_TOKEN`。

PowerShell 当前会话保存 token 示例：

```powershell
$env:DATAIFY_API_TOKEN = "YOUR_DATAIFY_API_TOKEN"
```

Windows 永久用户级变量设置：

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "YOUR_DATAIFY_API_TOKEN", "User")
```

## 核心工作流程

1. 提交前，向用户展示参数清单中列出的必填值、可选值和默认值。
2. 询问用户在运行任务前是否要修改任何值。
3. 询问用户是否要采集多组 Instagram 帖子评论。如果是，要求提供多个 `posturl` 值。
4. 将最终值规范化为 `spider_parameters` 对象列表。
5. 从用户明确输入或已保存的 `DATAIFY_API_TOKEN` 中获取 Dataify token。
6. 如果没有可用的 token，要求用户输入 API TOKEN 并询问是否保存为 `DATAIFY_API_TOKEN`。
7. 验证帖子 URL 和文件名。
8. 使用 `spider_id=ins_comment_by-posturl` 提交 Builder 请求。
9. 从 Builder 响应中读取 `data.task_id`，并读取 `data.status` 或 `status`（如果存在）。
10. Builder 成功后停止。
11. 告知用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 参数清单

当用户调用此技能时，首先告知这些值的使用情况。始终以 Markdown 表格展示提交的参数；不要使用纯文本或项目列表进行参数确认。

| 字段 | 必填 | 默认值 | 位置 | 备注 |
| --- | --- | --- | --- | --- |
| `posturl` | 是 | `https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/` | `spider_parameters` | Instagram 帖子 URL。 |
| `file_name` | 否 | `{{TasksID}}` | Builder 表单字段 | 用户未修改时使用默认值。 |

然后询问："在我提交任务之前，您是否要修改这些值？"

同时询问："您是否要采集多组 Instagram 帖子评论？如果是，请提供多个 `posturl` 值。"

如果用户已提供部分值，在表格中显示这些值替代默认值，只询问是否修改剩余/默认的值。

## 参数处理

- `posturl` 为必填项。如果用户未提供，仅在参数确认表格中展示后使用默认值 `https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/`。
- 去除 `posturl` 前后的空格。
- `posturl` 不能为空。
- `posturl` 必须以 `https://www.instagram.com/` 开头。
- 多组采集仅在 `spider_parameters` 中重复 `posturl`。
- `file_name` 默认为 `{{TasksID}}`。如果用户修改，则提交用户提供的值。
- `file_name` 不能为空。

单组示例：

```json
spider_parameters=[{"posturl":"https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/"}]
```

多组示例：

```json
spider_parameters=[{"posturl":"https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/"},{"posturl":"https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/"}]
```

## Dataify Builder 请求

使用表单字段而非手动构建的 URL 编码字符串。

- URL：`https://scraperapi.dataify.com/builder?platform=1`
- 方法：`POST`
- 授权头：`Bearer DATAIFY_API_TOKEN`
- 内容类型：`application/x-www-form-urlencoded`
- 固定字段：
  - `spider_name=instagram.com`
  - `spider_id=ins_comment_by-posturl`
  - `spider_errors=true`
- 默认字段：
  - `file_name={{TasksID}}`
- 动态字段：
  - `spider_parameters` 必须是帖子 URL 对象的 JSON 字符串数组。

## 脚本

为了稳定执行，优先使用 Python 3.6 或更新版本运行 `scripts/submit_dataify_instagram_comment_by_posturl.py`，而不是重写 Builder 流程。

```powershell
python3 ".\scripts\submit_dataify_instagram_comment_by_posturl.py" --posturl "https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/"
```

覆盖已保存的环境 token 或文件名：

```powershell
python3 ".\scripts\submit_dataify_instagram_comment_by_posturl.py" --api-token "YOUR_DATAIFY_API_TOKEN" --posturl "https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/" --file-name "{{TasksID}}"
```

提交多个帖子 URL：

```powershell
python3 ".\scripts\submit_dataify_instagram_comment_by_posturl.py" --params-json '[{"posturl":"https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/"},{"posturl":"https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/"}]'
```

脚本会打印包含 `spider_id`、`task_id`、`status`、`parameters`、`file_name`、`dashboard_url` 和 `message` 的 JSON 摘要。

## 故障排除

`Missing Dataify API TOKEN` 表示未传递显式 token 且本地未保存 `DATAIFY_API_TOKEN`。告知用户需要提供 Dataify API TOKEN，询问是否保存为 `DATAIFY_API_TOKEN`，或告知可以在 [Dataify](https://dashboard.dataify.com/login?utm_source=skill) 注册或登录获取。如果已有 token，告知其位于 [Dataify](https://dashboard.dataify.com?utm_source=skill) 右上角。

`posturl cannot be empty` 表示缺少必填的 Instagram 帖子 URL。

`posturl must start with https://www.instagram.com/` 表示 URL 不在允许的 Instagram 域名范围内。

`File name cannot be empty` 表示未提供可用的 `file_name`。

`Necessary parameters is empty!` 通常表示 Builder 请求未以表单字段提交、`spider_parameters` 不是 JSON 字符串数组，或某个 `spider_parameters` 对象缺少 `posturl`。

缺少 `task_id` 通常表示授权头、token、`spider_name`、`spider_id` 或 `spider_parameters` 有误。

## 安全规则

- 不要将 `file_name` 放入 `spider_parameters` 中。
- 不要使用 `https://www.instagram.com/` 之外的 Instagram URL。
- 提及身份验证时仅使用 `API TOKEN` 和 `DATAIFY_API_TOKEN`。
- 不要硬编码本地 Python 路径。
- 不要编造结果字段。
- 任务创建成功后始终引导用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill)。
