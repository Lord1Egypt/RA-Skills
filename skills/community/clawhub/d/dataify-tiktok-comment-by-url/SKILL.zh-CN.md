---
name: "dataify-tiktok-comment-by-url"
description: "为 tiktok.com 上以 tiktok_comment_by-url 为根的 scraper 系列准备 Dataify builder 请求。当需要处理成功的 Dataify scraper detail 条目 tiktok_comment_by-url、让用户选择可用工具、读取已保存的 getToolParams 选项，并使用 DATAIFY_API_TOKEN 生成 scraperapi.dataify.com/builder curl 请求时，使用此 skill。"
---

# Dataify Builder Skill 中文版

这个 skill 用于为 `tiktok.com` 下、以 `tiktok_comment_by-url` 为入口的 Dataify scraper 工具族生成 builder 请求。

## 工作流程

1. 先检查环境变量中是否存在 `DATAIFY_API_TOKEN`。
2. 如果 token 缺失，提示用户前往 <a href="https://dashboard.dataify.com?utm_source=skill">dataify&#23448;&#32593;</a> 获取。
3. 先让用户从下面的中文工具列表中明确选择一个工具：
- 通过URL采集 (tiktok_comment_by-url)
- 通过URL采集 (tiktok_shop_by-url)
- 通过列表URL采集 (tiktok_posts_by-listurl)
- 通过URL采集 (tiktok_profiles_by-url)
- 通过搜索网址采集 (tiktok_profiles_by-listurl)
4. 再读取 `references/tool-params.json`，根据 `tool_sign` 或中文工具名找到对应工具。
5. 对所选工具的每个参数分别处理：
   - 如果 `input_mode` 是 `user_input`，让用户提供值。
   - 如果 `input_mode` 是 `select`，把已保存的可选项展示给用户，让用户选择。
6. 默认优先使用 `scripts/build-dataify-request.py`，因为它是跨平台版本。
7. Windows 下也可以使用 `scripts/build-dataify-request.ps1`。
8. `spider_parameters` 必须是一个 JSON 数组。
9. `spider_name` 固定取 `tiktok.com`。
10. `spider_id` 固定取用户所选工具的 `tool_sign`。
11. 始终包含 `spider_errors=true` 和 `file_name={{TasksID}}`。

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

## 脚本用法

Python：

```bash
python scripts/build-dataify-request.py --tool-sign <selected_tool_sign> --values-file values.json
```

PowerShell：

```powershell
& ".\scripts\build-dataify-request.ps1" -ToolSign "<selected_tool_sign>" -ValuesFile ".\values.json"
```

`values.json` 可以是单个对象，也可以是对象数组。

## 输出格式

最终 `curl` 命令应为：

```bash
curl -X POST 'https://scraperapi.dataify.com/builder' \
  -H "Authorization: Bearer $DATAIFY_API_TOKEN" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'spider_name=tiktok.com' \
  -d 'spider_id=<selected_tool_sign>' \
  -d 'spider_parameters=[{"param":"value"}]' \
  -d 'spider_errors=true' \
  -d 'file_name={{TasksID}}'
```

## 参考文件

- `references/tool-params.json` 保存了这个 skill 下所有工具及参数选项。
- `scripts/build-dataify-request.py` 是首选的跨平台实现。
- `scripts/build-dataify-request.ps1` 是 Windows PowerShell 版本。
- 如果参数没有预设选项，必须向用户要值。
- 如果参数有预设选项，先把选项展示给用户，再生成最终请求。
- 不要假设 `spider_parameters` 永远只有一个对象；多值工具可能需要按索引生成多个对象。
- `url_example` 仅作为参考，不要默认用户就要用示例值，除非用户明确确认。
