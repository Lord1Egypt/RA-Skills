# AI Daily Digest

skill 制作详情可查看 ➡️ https://mp.weixin.qq.com/s/rkQ28KTZs5QeZqjwSCvR4Q

从 [Andrej Karpathy](https://x.com/karpathy) 推荐的 92 个 Hacker News 顶级技术博客及 3 个国内科技媒体（36氪、少数派、InfoQ中文）中抓取最新文章，通过 AI 多维评分筛选，生成一份结构化的每日精选日报。默认使用 OpenAI 兼容 API（DeepSeek、OpenAI 等），并支持自动降级到 Gemini。

![AI Daily Digest 概览](assets/overview.png)

> 海外信息源来自 [Hacker News Popularity Contest 2025](https://refactoringenglish.com/tools/hn-popularity/)，涵盖 simonwillison.net、paulgraham.com、overreacted.io、gwern.net、krebsonsecurity.com 等。国内信息源：36氪、少数派、InfoQ中文。

## 使用方式

作为 OpenClaw Skill 使用，在对话中输入 `/digest` 即可启动交互式引导流程：

```
/digest
```

Agent 会依次询问：

| 参数 | 选项 | 默认值 |
|------|------|--------|
| 时间范围 | 24h / 48h / 72h / 7天 | 48h |
| 精选数量 | 10 / 15 / 20 篇 | 15 篇 |
| 输出语言 | 中文 / English | 中文 |
| OPENAI_API_KEY | 手动输入（首次需要，之后自动记忆） | — |

配置会自动保存到 `~/.hn-daily-digest/config.json`，下次运行可一键复用。

### 直接命令行运行

```bash
export OPENAI_API_KEY="your-key"                     # 必填（DeepSeek / OpenAI 等）
export OPENAI_API_BASE="https://api.deepseek.com/v1" # 可选，默认 https://api.openai.com/v1
export OPENAI_MODEL="deepseek-chat"                  # 可选，不填会自动推断
export GEMINI_API_KEY="your-gemini-key"              # 可选，OpenAI 失败时兜底
npx -y bun scripts/digest.ts --hours 48 --top-n 15 --lang zh --output ./digest.md
```

## 功能

### 五步处理流水线

```
RSS 抓取 → 时间过滤 → AI 评分+分类 → AI 摘要+翻译 → 趋势总结
```

1. **RSS 抓取** — 并发抓取 95 个源（92 个海外 + 3 个国内，10 路并发，15s 超时），兼容 RSS 2.0 和 Atom 格式
2. **时间过滤** — 按指定时间窗口筛选近期文章
3. **AI 评分** — AI 从相关性、质量、时效性三个维度打分（1-10），同时完成分类和关键词提取（OpenAI 兼容 API 优先，失败自动降级到 Gemini）
4. **AI 摘要** — 为 Top N 文章生成结构化摘要（4-6 句）、中文标题翻译、推荐理由
5. **趋势总结** — AI 归纳当日技术圈 2-3 个宏观趋势

### 日报结构

生成的 Markdown 文件包含以下板块：

| 板块 | 内容 |
|------|------|
| 📝 今日看点 | 3-5 句话的宏观趋势总结 |
| 🏆 今日必读 | Top 3 深度展示：中英双语标题、摘要、推荐理由、关键词 |
| 📊 数据概览 | 统计表格 + Mermaid 饼图（分类分布）+ Mermaid 柱状图（高频关键词）+ ASCII 纯文本图 + 话题标签云 |
| 分类文章列表 | 按 6 大分类分组，每篇含中文标题、来源、相对时间、评分、摘要、关键词 |

### 六大分类体系

| 分类 | 覆盖范围 |
|------|----------|
| 🤖 AI / ML | AI、机器学习、LLM、深度学习 |
| 🔒 安全 | 安全、隐私、漏洞、加密 |
| ⚙️ 工程 | 软件工程、架构、编程语言、系统设计 |
| 🛠 工具 / 开源 | 开发工具、开源项目、新发布的库/框架 |
| 💡 观点 / 杂谈 | 行业观点、个人思考、职业发展 |
| 📝 其他 | 不属于以上分类的内容 |

## 亮点

- **零依赖** — 纯 TypeScript 单文件，无第三方库，基于 Bun 运行时的原生 `fetch` 和内置 XML 解析
- **中英双语** — 所有标题自动翻译为中文，原文标题保留为链接文字，不错过任何语境
- **结构化摘要** — 不是一句话敷衍了事，而是 4-6 句覆盖核心问题→关键论点→结论的完整概述，30 秒判断一篇文章是否值得读
- **可视化统计** — Mermaid 图表（GitHub/Obsidian 原生渲染）+ ASCII 柱状图（终端友好）+ 标签云，三种方式覆盖所有阅读场景
- **智能分类** — AI 自动将文章归入 6 大类别，按类浏览比平铺列表高效得多
- **趋势洞察** — 不只是文章列表，还会归纳当天技术圈的宏观趋势，帮你把握大方向
- **配置记忆** — API Key 和偏好参数自动持久化，日常使用一键运行

## 环境要求

- [Bun](https://bun.sh) 运行时（通过 `npx -y bun` 自动安装）
- 至少一个可用的 AI API Key：
  - `OPENAI_API_KEY`（可配合 `OPENAI_API_BASE` 使用 DeepSeek / OpenAI 等 OpenAI 兼容服务）
  - 或 `GEMINI_API_KEY`（[免费获取](https://aistudio.google.com/apikey)，OpenAI 失败时自动兜底）
- 网络连接

## 切换 AI 模型提供商

本项目默认使用 OpenAI 兼容 API（如 DeepSeek、OpenAI 等），Gemini 作为自动兜底。如果你希望替换为其他模型提供商（如 Anthropic、通义千问等），可以借助 AI 编码助手一键完成。

### 方法：让 AI 帮你改

在你使用的 AI 编码工具（如 Claude Code、Cursor、GitHub Copilot 等）中，直接发送以下 prompt：

```
请修改 scripts/digest.ts，将 AI 提供商从 OpenAI 兼容 API 替换为 [你想用的提供商]。

需要修改的部分：
1. 常量 OPENAI_DEFAULT_API_BASE（第 10 行）— 替换为目标 API 的 endpoint
2. 函数 callOpenAICompatible（约第 402 行）— 修改 request body 格式和 response 解析逻辑以适配目标 API
3. 函数 inferOpenAIModel（约第 447 行）— 更新模型自动推断逻辑
4. SKILL.md 和 README.md 中的相关说明文字

要求：
- 保持函数签名不变（输入 prompt 字符串，返回 string）
- 保持 temperature 等参数的语义等价
- 更新 CLI 帮助文本和错误提示中的 key 名称
```

### 改动范围说明

整个项目只有一个脚本文件 `scripts/digest.ts`，AI 调用逻辑集中在两处：

| 位置 | 说明 |
|------|------|
| `OPENAI_DEFAULT_API_BASE` 常量 | API endpoint 地址 |
| `callOpenAICompatible()` 函数 | 请求构造 + 响应解析，约 40 行代码 |

其余所有代码（RSS 抓取、评分 prompt、摘要 prompt、报告生成）均与 AI 提供商无关，无需修改。Prompt 内容本身是通用的，切换模型后可以直接复用。

### 常见替换示例

| 提供商 | API Endpoint | Key 环境变量 |
|--------|-------------|-------------|
| OpenAI | `https://api.openai.com/v1/chat/completions` | `OPENAI_API_KEY` |
| Anthropic | `https://api.anthropic.com/v1/messages` | `ANTHROPIC_API_KEY` |
| DeepSeek | `https://api.deepseek.com/v1/chat/completions` | `DEEPSEEK_API_KEY` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `DASHSCOPE_API_KEY` |
| OpenAI 兼容 API | 自定义 endpoint | 自定义 |

> 💡 如果目标提供商兼容 OpenAI API 格式（如 DeepSeek、Groq、Together AI 等），改动量更小 — 只需换 URL 和 Key，request/response 格式相同。

## 信息源

95 个 RSS 源，包括 92 个精选自 Hacker News 社区最受欢迎的独立技术博客，以及 3 个国内热门科技媒体：

> Simon Willison · Paul Graham · Dan Abramov · Gwern · Krebs on Security · Antirez · John Gruber · Troy Hunt · Mitchell Hashimoto · Steve Blank · Eli Bendersky · Fabien Sanglard ...
>
> 36氪 · 少数派 · InfoQ中文

完整列表内嵌于 `scripts/digest.ts`。
