<div align="center">

# 🌐 DeepSeek Web Search（DeepSeek 联网搜索）

### 一个「DeepSeek API 里本来就有」的联网搜索超能力。

**你提问 → DeepSeek 官方服务端 agent 实时联网检索 → 直接给你一份带来源的合成回答。**

不用对接任何第三方搜索引擎，不用额外申请搜索接口密钥，不用写胶水代码。

一份标准 `SKILL.md` + 一个脚本 —— 任何主流 AI 工具都能立刻联网。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node](https://img.shields.io/badge/Node-%3E%3D18-brightgreen)](https://nodejs.org/)
[![DeepSeek](https://img.shields.io/badge/Powered%20by-DeepSeek%20Responses%20API-purple)](https://platform.deepseek.com)
[![Harnesses](https://img.shields.io/badge/Works%20in-Claude%20Code%20%E2%80%A2%20Codex%20%E2%80%A2%20Gemini%20CLI%20%E2%80%A2%20Copilot%20CLI-lightgrey)]()

**简体中文** · [English](README.md)

</div>

---

## ⚡ 一句话卖点

**DeepSeek 官方把联网搜索直接内置进了 API。** 只要用 `Responses` 格式接口调用 `deepseek-v4-flash` 模型，在请求参数里声明 `web_search` 工具——剩下的一切都交给 DeepSeek 服务端的 **agent**：它自己搜索、打开页面、多轮核实、交叉验证，最后直接给你一份**有依据的合成回答**。不是一坨链接，而是一份成品答案。

这个 skill 把这股力量打包成通用的 `SKILL.md` 格式，任何工具都能加载即用：Claude Code、Codex、Gemini CLI、Copilot CLI……

---

## 😮 为什么这件事很牛

其他「联网搜索」方案，全是一堆脏活：

| | 传统做法 | DeepSeek Web Search |
|---|---|---|
| **搜索引擎** | 注册 Bing / Brave / Serper / Tavily…… | **DeepSeek API 内置，零集成** |
| **密钥** | 再申请一个搜索 key，配置额度、计费 | **零额外密钥**，用已有的 DeepSeek key 就行 |
| **胶水代码** | 写适配器抓结果、翻页、拼 JSON | **零胶水**，一个干净的 HTTP 调用 |
| **拿到的结果** | 一堆原始链接，还得再喂给大模型 | **一份可直接使用的合成回答 + 来源** |
| **搜索质量** | 死板的关键词匹配 | **一个会搜索、会翻页、会核实、会追问的 agent** |

> 真正的杀手锏：**它不是一个简单的搜索 API。** DeepSeek 的 agent 能力把「你的问题」和「搜索结果」一起做了封装——它会自己判断结果是否可信、发现你问题里的错误前提、最终整合成一份完整、有依据的答案。这就是「给你 10 条链接」和「告诉你到底发生了什么」的区别。

---

## ✨ 功能特性

- 🔥 **官方原生搜索** —— 由 DeepSeek 官方 API 驱动，不是第三方包装
- 🤖 **Agent 级研究能力** —— 多轮搜索循环（`搜索 → 打开页面 → 再次搜索`），服务端一次 API 调用完成
- 🎯 **合成回答** —— 返回一份连贯答案 + 参考来源 URL，而不是原始结果轰炸
- 🌏 **中英双语覆盖** —— 同时覆盖中文和英文网络，用你的语言回答
- 🪶 **零依赖** —— 一个自包含的 `search.mjs`，只用到 Node 内置的 `fetch`
- 🔒 **密钥留在本地** —— key 存在 `config.json` 或 `DEEPSEEK_API_KEY` 里，永不离开你的机器
- 📦 **通用格式** —— 符合规范的 `SKILL.md`，配合一键安装脚本，随处可装

---

## 🧠 工作原理

一次调用 DeepSeek Responses API：

```json
{
  "model": "deepseek-v4-flash",
  "input": "2026 年冬奥会在哪举办？",
  "instructions": "你是联网搜索助手。必要时多轮搜索、打开页面核实，然后给出准确、完整、有依据的回答。",
  "tools": [{ "type": "web_search" }],
  "tool_choice": { "type": "web_search" },
  "max_output_tokens": 8000
}
```

之后全部由 DeepSeek 服务端接管：

1. 🔎 发起 `web_search_call` 搜索
2. 📄 打开最相关的页面（`open_page`）
3. 🔁 信息不完整就继续搜索
4. ✅ 最终返回 `output_text` —— 一份有依据的合成回答

`search.mjs` 负责把响应解析成干净的 `{ answer, sources }` JSON。整个集成到此为止。

---

## 🚀 安装

### 方式 1 — 一行 npx 安装（推荐）

```bash
npx github:mingzeng21/deepseek-web-search
```

就这一句，不用 clone、不用手动操作。安装器会一次把 skill 装进**所有支持的 harness**——`~/.claude/skills/`（Claude Code）**和** `~/.agents/skills/`（Codex · Gemini CLI · Copilot CLI），然后引导你填入 DeepSeek API key（或读取 `DEEPSEEK_API_KEY` 环境变量）并写入本地 `config.json`。

只想装某一个，或先跳过 key 输入：

```bash
npx github:mingzeng21/deepseek-web-search --claude   # 只装 Claude Code
npx github:mingzeng21/deepseek-web-search --codex    # 只装 Codex / Gemini CLI / Copilot CLI
npx github:mingzeng21/deepseek-web-search --skip-key # 先不填 key（稍后自行配置）
```

### 方式 2 — 直接让你的 AI 助手装

不用 clone、不用敲命令。在 **Claude Code** 或 **Codex** 里，把 URL 粘贴进去说一句：

> 安装以下 skill：https://github.com/mingzeng21/deepseek-web-search.git

助手会自动 clone 仓库并放到对应的 skills 目录——Claude Code 读取 `~/.claude/skills/`，Codex、Gemini CLI、Copilot CLI 读取 `~/.agents/skills/`。重启（Claude Code 里也可用 `/reload-plugins`）即可生效。

> **注意：** `~/.agents/skills/` 是 Codex、Gemini CLI、Copilot CLI 共用的跨运行时目录——装一次，三个工具通用。

---

## 🔑 配置

去 [platform.deepseek.com](https://platform.deepseek.com) 申请一个 API key，然后：

```bash
cp config.example.json config.json
# 编辑 config.json，填入你的 key
```

也可以不建文件，脚本同样支持环境变量：

```bash
export DEEPSEEK_API_KEY="sk-..."
```

---

## 💻 使用

```bash
node ./search.mjs "2026 年冬奥会金牌榜第一是谁？" 8000
```

| 参数 | 说明 |
|---|---|
| `query`（必填） | 要研究的问题 |
| `maxOutputTokens`（可选） | 回答长度上限，默认 `8000`（最大 `16384`） |

输出 —— 一个 JSON 对象：

```json
{
  "answer": "2026 年冬奥会在意大利米兰与科尔蒂纳丹佩佐举行……",
  "sources": ["https://olympics.com/…", "https://zh.wikipedia.org/…"],
  "query": "2026 年冬奥会金牌榜第一是谁？",
  "model": "deepseek-v4-flash",
  "usage": { "input_tokens": 812, "output_tokens": 640, "total_tokens": 1452 },
  "engine": "deepseek-web-search"
}
```

`answer` 是可以直接使用的成品。`sources` 是 agent 参考过的页面——**展示答案时一定要注明来源。**

---

## ⚙️ 环境要求

- **Node.js 18+**（使用内置 `fetch`，无任何依赖）
- 一个 **DeepSeek API key**（见上方 [配置](#-配置)）

---

## 📌 注意事项

- 多轮搜索在服务端进行，单次调用需要 **15–70 秒**。这是 agent 在工作，不是卡死（脚本允许最长 120 秒）。
- `sources` 是「参考过的页面」，不是逐句引用。关键信息请对照来源核实后再采信。
- agent 会发现并纠正你问题里的**错误前提**（例如「2026 巴黎奥运会」→ 实际是 2026 米兰–科尔蒂纳冬奥会）。
- 向用户展示结果时，请始终附上来源 URL。

---

## ❤️ 喜欢它？

点个 Star，分享给你的团队，并把它发布到你喜欢的 skill 平台。重活 DeepSeek 已经干完了——这个 skill 只是让它离你一步之遥。

---

## 📄 License

[MIT](LICENSE) © MingZeng
