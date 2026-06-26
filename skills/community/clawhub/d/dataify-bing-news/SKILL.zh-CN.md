---
name: dataify-bing-news
description: "当用户需要运行 Bing 新闻搜索时，使用此 skill。"
---

# Bing News 中文版

这个 skill 用于将用户的搜索请求转化为 Dataify Scraper API 调用，并返回结构化搜索结果。

## 调用前确认（必须）

每次真正调用 API 之前，必须遵循以下确认流程：

1. 将用户请求解析为 API 参数字段和固定的 `engine` 值。
2. 仅在参数描述明确标注默认值时才使用默认值。不要将示例值、占位符或样例数据作为默认值。
3. 如果必填参数没有默认值且无法从用户请求中推断，先询问用户。
4. 调用 API 前展示 Markdown 参数表。不要包含 `Authorization`。表格必须包含以下列：`参数名`、`当前值`、`默认值`、`说明`。
5. 展示表格后询问用户是否需要修改参数。用户确认后才能调用 API。
6. 如果用户修改了参数，重新生成表格并再次确认。
7. 如果 token 缺失，提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 获取 `DATAIFY_API_TOKEN`。

## 工作流程

1. 解析用户请求，提取搜索参数。
2. 如果 token 缺失，提示用户前往 [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) 获取 `DATAIFY_API_TOKEN`。
3. 构建请求参数，仅包含用户请求的字段和必要的默认值。
4. 使用 `python3` 运行脚本。

```bash
python3 scripts/bing_news.py --params-json '{"q":"搜索关键词"}'
```

如果用户在对话中提供了 token，使用 `--token` 传递：

```bash
python3 scripts/bing_news.py --token "USER_TOKEN" --params-json '{"q":"搜索关键词"}'
```

5. 将脚本输出直接返回给用户。不要对 API 响应进行总结、提取、清理、翻译或重新格式化。

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

## 参考文件

- `references/` 目录下的 API 文档包含完整的字段列表和说明。
- 当字段行为、允许的值或响应格式不明确时，请查阅参考文档。
## 注意事项

- 始终使用 `Content-Type: application/x-www-form-urlencoded` 提交 API 请求。
- 保持请求值为字符串类型。
- 省略用户未请求的可选字段。
- 除非用户另有要求，否则不要对返回结果进行任何加工处理。
