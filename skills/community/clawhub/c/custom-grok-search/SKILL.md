---
name: custom-grok-search
description: 使用 xAI Grok 的 Responses API 进行网页搜索与 X/Twitter 搜索；支持官方 xAI 接口，也支持通过公益站或其他第三方 Grok 兼容代理来使用 web_search / x_search。
---

# custom-grok-search

这个 Skill 用来调用 Grok 的服务端搜索工具：

- `web_search`：网页搜索
- `x_search`：X / Twitter 搜索

适用场景：

- 用户想搜索网页信息，但希望走 Grok / xAI 能力
- 用户想搜 X / Twitter 上的帖子、账号、讨论串
- 运行环境没有直接使用官方 xAI 接口，而是改走公益站或其他第三方 Grok 兼容代理

## 支持的两种模式

### 1. 官方 xAI 模式

如果环境里提供的是官方 xAI 凭证，脚本会直接请求官方接口。

适合：
- 你自己有官方 xAI Key
- 不需要第三方代理

### 2. 公益站 / 第三方代理模式

如果检测到 `CUSTOM_GROK_APIKEY`，脚本会自动切换到第三方 Grok 兼容代理模式。

适合：
- 通过公益站使用 Grok Search
- 使用自建或第三方兼容 OpenAI / xAI Responses API 的代理
- 需要自定义 base URL、模型名、User-Agent

如果你需要配置代理相关变量，请读取：
- `references/config.md`

如果你需要官方文档入口，请读取：
- `references/xai-tools-links.md`

## 运行方式

使用 `{baseDir}` 来引用 Skill 目录，避免因为工作目录不同导致路径失效。

### 搜索

- 网页搜索：
  - `node {baseDir}/scripts/grok_search.mjs "<query>" --web`

- X / Twitter 搜索：
  - `node {baseDir}/scripts/grok_search.mjs "<query>" --x`

### 对话

- 文本对话：
  - `node {baseDir}/scripts/chat.mjs "<prompt>"`

- 图像对话：
  - `node {baseDir}/scripts/chat.mjs --image /path/to/image.jpg "<prompt>"`

### 其他

- 列出可用模型：
  - `node {baseDir}/scripts/models.mjs`

- 运行轻量自检：
  - `node {baseDir}/scripts/selftest.mjs`

## 常用参数

搜索脚本支持这些常用参数：

### 输出控制

- `--links-only`：只输出引用链接
- `--text`：输出精简文本，不展示 citations 段
- `--raw`：把原始 Responses API 返回写到 stderr，便于排错

### 通用参数

- `--max <n>`：限制结果数，默认 8
- `--model <id>`：本次调用临时指定模型

### X / Twitter 搜索过滤

- `--days <n>`：限制最近 N 天
- `--from YYYY-MM-DD`
- `--to YYYY-MM-DD`
- `--handles @a,@b`：只看这些账号
- `--exclude @bots,@spam`：排除这些账号

## 输出格式

默认输出为便于 agent 消费的 JSON，大致结构如下：

```json
{
  "query": "...",
  "mode": "web" | "x",
  "results": [
    {
      "title": "...",
      "url": "...",
      "snippet": "...",
      "author": "...",
      "posted_at": "..."
    }
  ],
  "citations": ["https://..."]
}
```

## 使用建议

- 一般网页研究优先用 `--web`
- 查推文、帖子、线程时优先用 `--x`
- 如果你是通过公益站或第三方代理使用 Grok，先看 `references/config.md` 再调用脚本
- 如果模型偶发没有严格返回 JSON，脚本会尽量透传文本结果，而不是直接硬失败
