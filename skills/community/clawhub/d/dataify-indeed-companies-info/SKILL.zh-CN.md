---
name: dataify-indeed-companies-info
description: "通过 Dataify Scraper API 采集 Indeed 公司信息。当用户请求 gather/scrape/crawl/fetch/extract/collect Indeed company、company profile、company information 数据，或提出 Indeed company info scrape、Indeed companies collect、Indeed 公司信息采集/抓取，或使用 Indeed company list URL、company keyword、industry and state/location、company URL 时使用。此 skill 将请求映射到 spider IDs indeed_companies-info_by-company-list-url、indeed_companies-info_by-keyword、indeed_companies-info_by-industry-and-state 和 indeed_companies-info_by-company-url。"
---

# Dataify Indeed Companies Info 中文版

## 采集模式

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `company-list-url` | `indeed_companies-info_by-company-list-url` | `company_list_url` | `[{"company_list_url":"https://www.indeed.com/companies/browse-companies"}]` |
| `keyword` | `indeed_companies-info_by-keyword` | `keyword` | `[{"keyword":"openai"}]` |
| `industry-and-state` | `indeed_companies-info_by-industry-and-state` | `industry` | `[{"industry":"All","state":"United States"}]` |
| `company-url` | `indeed_companies-info_by-company-url` | `company_url` | `[{"company_url":"https://www.indeed.com/cmp/Allstate-Insurance"}]` |

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
python3 scripts/indeed_companies_info.py --help
```

## 注意事项

- 提交成功后不要下载结果文件，告诉用户前往 [Dataify](https://dashboard.dataify.com?utm_source=skill) 查看。
- 始终以 Markdown 表格展示参数确认，不要使用纯文本或项目列表。
- 如果用户已经提供了部分参数，在表格中显示这些值，只询问是否修改剩余参数。
