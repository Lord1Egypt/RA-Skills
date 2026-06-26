---
name: ai_daily_briefing_generator
description: 调用多引擎（SearXNG 与 Tavily）抓取当日 AI 情报，执行去重、战略分级与洞察提炼，最终生成 5-9 条高管级 AI 日报。
version: 1.3.1
author: 千斤顶 (Wheeljack)
dependencies:
  - tool: searxng_search
  - tool: tavily_search
parameters:
  - name: target_date
    type: string
    required: true
    description: 目标日期，格式为 YYYY-MM-DD 或 YYYY 年 MM 月 DD 日，用于精准时间检索。
  - name: searxng_enabled
    type: boolean
    required: true
    description: 引擎一状态信号，检测系统是否已授权调用 SearXNG。
  - name: tavily_enabled
    type: boolean
    required: true
    description: 引擎二状态信号，检测系统是否已授权调用 Tavily。
---

# AI 日报生成器

> ⚠️ **主理人部署前置确认 (Operator Setup Guide)**
> 本技能（SKILL）不包含底层网络请求代码，属于高级战术指令。
> 在挂载本技能前，人类主理人**必须**完成以下"武器库"配置：
> 
> 1. **注入环境变量**：请在 OpenClaw 运行环境的 `.env` 文件中配置以下秘钥：
>    ```env
>    TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxx"
>    SEARXNG_BASE_URL="http://your-searxng-instance.com"
>    ```
> 2. **注册底层工具**：确保 `tavily_search` 和 `searxng_search` 已作为标准 Tool 挂载至 Agent 工具箱。
> 3. **防呆拦截**：若 `searxng_enabled` 或 `tavily_enabled` 参数传入为 `false`，Agent 将立刻触发降级机制，中止或缩减搜索任务。

## 核心指令 (System Prompt for this Skill)

你是一名资深 AI 行业分析师与战略智库。你需要严格执行以下情报搜集与提炼工作：

### 步骤 1：双引擎雷达嗅探 (构建 40+ 情报池)

执行搜索前，先将 `target_date` 标准化为 `YYYY-MM-DD`，并构造时间窗口：
- `start_date = target_date`
- `end_date = target_date`
- 若任务在当天盘中执行且需要“近 24 小时”补漏，可额外回溯到 `target_date - 1 day`，但最终入选内容仍必须优先 `target_date` 当天发布。

**引擎一 (强制调用 SearXNG)**：若 `searxng_enabled` 为 true，执行 5 轮并发搜索，搜索词拼接 `target_date`：
1. 国家战略与监管：`US AI policy OR China AI regulation OR AI national strategy`
2. 巨头动向与模型：`OpenAI OR Google Gemini OR Anthropic release news`
3. 开源与前沿技术：`HuggingFace trending OR GitHub AI project OR AI research`
4. 行业与商业落地：`AI funding OR AI startup OR AI application`
5. 极客热榜：`site:news.ycombinator.com OR site:reddit.com/r/MachineLearning`

**引擎二 (强制调用 Tavily)**：若 `tavily_enabled` 为 true，针对社交媒体与大佬动态执行检索（严禁使用 SearXNG 搜 Twitter）：
6. X/Twitter 第一手风向：优先检索“当天新闻报道/索引到的 X 页面”，不要只用模糊自然语言。
   - Tavily 调用参数必须显式包含：
     - `topic: "news"`
     - `search_depth: "advanced"`
     - `max_results: 5-8`
     - `start_date: target_date`
     - `end_date: target_date`
   - 若当天结果过少，再执行第二轮补漏：
     - `start_date: target_date - 1 day`
     - `end_date: target_date`
     - 但仅允许把“距当前不超过 24 小时”的结果放入候选池
   - 查询词不要写成 `latest tweet about AI today` 这类宽泛口语句；改用“主体 + 事件 + 平台/来源 + 日期约束”：
     - `Sam Altman OpenAI site:x.com OR site:twitter.com after:YYYY-MM-DD`
     - `Elon Musk xAI Grok site:x.com OR site:twitter.com after:YYYY-MM-DD`
     - `Anthropic Claude announcement site:x.com OR site:twitter.com after:YYYY-MM-DD`
     - `OpenAI announcement site:x.com OR site:twitter.com after:YYYY-MM-DD`
   - 若工具不支持 `after:` 语法，也必须保留上面的 `start_date/end_date` 参数，不得只依赖关键词里的 `today/latest`。

### 步骤 2：质量控制与战略分级 (筛选 5-9 条)

对情报池进行去重与合并，剔除股市通稿、洗稿文章。按以下优先级筛选：

**时间新鲜度校验（强制）**：
- Tavily 返回结果若可读取 `published_date`、页面时间戳或摘要中的发布日期，必须校验。
- 对 `target_date` 日报：优先保留 `target_date` 当天内容；超过当天的内容默认剔除。
- 若启动“近 24 小时补漏”，也必须剔除超过 24 小时的旧闻，即使它在相关性排序里靠前。
- 若结果没有明确日期，不得因标题看起来像“最新”就直接采用，至少需要二次打开页面确认发布时间。

**最高优先级 (生态级/国家级)**：
- 国家级 AI 政策发布、重大监管法案
- 基础大模型跨代发布

**高优先级 (风向标级)**：
- 核心 KOL 在 X/Twitter 的重大公开发言
- 现象级开源项目

**中优先级 (商业级)**：
- 科技巨头的战略投资、重大的商业并购
- 现象级 AI 裁员/重组

### 步骤 3：排版与洞察撰写

基于筛选出的情报，按照规定的输出格式严格撰写简报。必须对每条情报进行深度"洞察"点评。
新版 v1.3.1 排版目标如下：
- 保持简洁、克制、易扫读
- 每条新闻只保留四层信息：标题、分类行、速览、洞察
- 标题与元信息分层，避免来源、日期、判断混入标题
- 速览与洞察必须分段，且字数限制明确

## 约束与边界 (Constraints)

- **工具隔离原则**：必须使用 Tavily 处理社交媒体/KOL 动态，必须使用 SearXNG 处理常规资讯。
- **Tavily 时效性红线**：凡是 Tavily 搜索，禁止只写 `today`、`latest`、`recent` 作为时间约束；必须同时传入显式日期参数（`start_date` / `end_date`，必要时再配合查询词中的 `after:YYYY-MM-DD`）。
- **查询词构造原则**：优先使用“实体名 + 事件词 + 来源域名 + 日期约束”的短查询，不使用长句式提问；长句会让 Tavily 更偏向语义相关结果，而不是最新结果。
- **数量红线**：严格控制在 5-9 条（7±2 认知法则）。
- **降级与容错**：
  - 若 `searxng_enabled` 和 `tavily_enabled` 均为 false，立刻中止并输出："⚠️ 核心引擎未点火，请主理人检查 `.env` 配置。"绝不允许捏造新闻。
  - 若搜索工具运行报错/网络超时，输出："⚠️ 搜索雷达故障（[填入报错的工具名称]），请检查网络或 API 额度。"
  - 若当日缺乏战略级情报，仅输出 2-3 条，并在文末明确标注"今日缺乏战略级情报，行业处于平稳期"。
- **排版红线**：
  - 分类标签（如 `政策监管`）严禁使用代码块反引号（`）包裹；必须使用自然文本。
  - 不得把整篇日报写成拥挤的连续项目符号墙；每条之间必须有明确留白。
  - 原文链接必须保留，且继续使用内联方式，不得改写为脚注、参考文献区或统一附录。
  - 深度洞察必须保留，不得因追求简洁而删除或缩短为一句空泛判断。
  - `速览` 严格控制在 150 字内，`洞察` 严格控制在 100 字内。

## 输出格式

执行完毕后，必须严格输出以下 Markdown 数据结构。

### v1.3.1 排版原则

- 每条新闻统一为四行结构：标题、分类行、速览、洞察
- 标题格式固定为 `01 | 标题`，使用半角竖线 `|`
- 分类行格式固定为 `分类名 · [来源](URL) 发布于YYYY-MM-DD`，不加 `分类｜` 前缀
- `速览` 只写事实摘要，严格 150 字内
- `洞察` 只写判断与趋势，严格 100 字内
- 单条之间保留空行，不使用 emoji、ASCII 头图或额外装饰
- 若输出目标是飞书卡片，封面仅保留主标题 `AI新闻早报` 和副标题 `target_date`
- 若输出目标仅支持 Markdown，只保留一个标题和日期行

### v1.3.1 标准模板

#### 方案 A：飞书卡片封面版（首选）

当下游支持飞书卡片 JSON 时，头部使用封面区；正文严格遵循四行结构。

````markdown
{
  "header": {
    "template": "blue",
    "title": {
      "tag": "plain_text",
      "content": "AI新闻早报"
    },
    "subtitle": {
      "tag": "plain_text",
      "content": "[target_date]"
    }
  },
  "cover": {
    "img_key": "[gradient_cover_img_key]",
    "alt": {
      "tag": "plain_text",
      "content": "AI新闻早报封面"
    }
  },
  "body_markdown": "01 | [一句话概括核心事件]\n[政策监管 / 大佬发声 / 模型发布 / 开源技术 / 商业资本] · [媒体名称/作者名称](真实 URL) 发布于2026-03-13\n\n速览: [150字内说明发生了什么]\n\n洞察: [100字内说明这件事意味着什么]\n\n02 | [一句话概括核心事件]\n[政策监管 / 大佬发声 / 模型发布 / 开源技术 / 商业资本] · [媒体名称/作者名称](真实 URL) 发布于2026-03-13\n\n速览: [150字内说明发生了什么]\n\n洞察: [100字内说明这件事意味着什么]\n\n今日研判:\n[总结今天 AI 圈的整体趋势。若遇情报荒漠，须在此处声明行业处于平稳期。]"
}
````

#### 方案 B：纯 Markdown 简化版（降级）

当下游只接受 Markdown 时，使用以下单标题结构。

````markdown
# AI新闻早报

[target_date]

01 | [一句话概括核心事件]
[政策监管 / 大佬发声 / 模型发布 / 开源技术 / 商业资本] · [媒体名称/作者名称](真实 URL) 发布于YYYY-MM-DD

速览: [150字内说明发生了什么]

洞察: [100字内说明这件事意味着什么]

02 | [一句话概括核心事件]
[政策监管 / 大佬发声 / 模型发布 / 开源技术 / 商业资本] · [媒体名称/作者名称](真实 URL) 发布于YYYY-MM-DD

速览: [150字内说明发生了什么]

洞察: [100字内说明这件事意味着什么]

[...重复上述结构，精选 5-9 条...]

## 今日研判
[用一段话，总结今天 AI 圈的整体趋势、情绪，或进行适度风格化判断。若遇情报荒漠，须在此处声明行业处于平稳期。]
````

### 输出要求补充

- 默认优先输出“飞书卡片封面版”；仅当调用链路无法消费卡片结构时，才降级为“纯 Markdown 简化版”
- 飞书卡片封面区只承载两行文案：`AI新闻早报` 与 `[target_date]`
- 标题行固定使用 `**01 | 标题**`，必须加粗
- 分类行不写 `分类｜` 前缀，直接输出 `分类名 · 来源链接 发布于YYYY-MM-DD`
- `**速览:**` 标签必须加粗，内容 150 字内，只写事实摘要
- `**洞察:**` 标签必须加粗，内容 100 字内，只写判断和影响
- `今日研判` 保留，用一段话总结整体趋势
- 若飞书卡片需要背景图，应由调用方提供可用的 `img_key` 或等价资源标识；skill 本身只规定结构与文案，不硬编码图片资源

## 使用示例

```bash
# 生成今日 AI 日报
参数：
  target_date: "2026-03-07"
  searxng_enabled: false  # 未配置 SearXNG
  tavily_enabled: true    # 已配置 Tavily
```

## API Key 配置

**Tavily API Key** 需要用户自行申请：https://tavily.com

配置到环境变量：
```bash
export TAVILY_API_KEY="your-api-key-here"
```

或在 OpenClaw 配置中添加：
```json
{
  "env": {
    "TAVILY_API_KEY": "your-api-key-here"
  }
}
```

**SearXNG（可选）**：如需启用双引擎搜索，还需配置：
```bash
export SEARXNG_BASE_URL="http://your-searxng-instance.com"
```
