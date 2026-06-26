---
name: dataify-google-maps-reviews
description: "通过 Dataify Scraper API 采集 Google Maps 评价/评论信息。当用户请求从 Google Maps URL gather/scrape/crawl/fetch/extract/collect Google Maps review/comment information，或 Google Maps review information、comments、URL reviews 的采集/抓取/爬取/获取/提取，或表达 Google 地图评论信息采集/抓取/爬取/获取、Google 地图评论 URL 提取，或使用 spider ID google_comment_by-url 时，使用此 skill。"
---

# Dataify Google Maps Reviews 中文版

## 采集模式

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `url` | `google_comment_by-url` | `url`, `days_limit` | `[{"url":"https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu","days_limit":"20"}]` |

## API TOKEN 处理

使用 `DATAIFY_API_TOKEN` 作为长期保存的 token 名称。

- 如果用户在请求中提供了 token，则使用该 token。
- 如果未提供 token，先检查环境变量中是否已保存 `DATAIFY_API_TOKEN`。
- 如果本地已保存 `DATAIFY_API_TOKEN`，则直接使用。
- 如果没有可用的 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取 API TOKEN。
- 没有 token 不要调用 Builder 接口。

## 设置 DATAIFY_API_TOKEN

推荐使用永久环境变量，而不是只在当前终端临时设置。

Windows PowerShell，当前用户永久设置：

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "your_token_here", "User")
```

然后重新打开 PowerShell。如果当前会话也要立即生效，再执行：

```powershell
$env:DATAIFY_API_TOKEN = "your_token_here"
```

macOS 或 Linux，bash 永久设置：

```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

macOS 或 Linux，zsh 永久设置：

```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```
## 核心工作流程

1. 从用户请求中识别采集模式。
2. 提交前，以 Markdown 表格展示必填参数、可选参数和默认值。
3. 询问用户是否需要修改参数。
4. 规范化并验证最终参数值。
5. 获取 Dataify token（用户提供或已保存的 `DATAIFY_API_TOKEN`）。
6. 如果没有 token，提示用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 获取。
7. 提交 Builder 请求创建任务。
8. 从响应中读取 `data.task_id`。
9. 提交成功后停止，告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看或管理结果。

## 脚本用法

使用 Python 运行：

```bash
python3 scripts/google_maps_reviews.py --help
```

## 注意事项

- 提交成功后不要下载结果文件，告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看。
- 始终以 Markdown 表格展示参数确认，不要使用纯文本或项目列表。
- 如果用户已经提供了部分参数，在表格中显示这些值，只询问是否修改剩余参数。
