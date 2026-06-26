---
name: ccfddl-conference-watch
description: >
  Fetch and filter academic conference deadlines from CCFDDL (https://ccfddl.com).
  Use this skill whenever the user mentions CCF conferences, paper submission deadlines,
  CFP (Call for Papers), academic venue selection, conference rankings (CCF-A, CCF-B, CORE),
  or asks questions like "有哪些可以投稿的会议", "最近有什么DDL", "upcoming deadlines",
  "哪些会议还能投", "帮我查一下CCF会议", "conference deadline reminder",
  "图形学/AI/多媒体方向的会议". Also trigger when the user asks about CCFDDL, ccfddl.com,
  or wants a daily/weekly deadline briefing. Even if the user just says "DDL" or "投稿"
  in an academic context, this skill is likely relevant.
---

# CCFDDL Conference Watch

Query real conference deadline data from CCFDDL and present it clearly.

## Data fetching strategy

Try sources in this order — stop as soon as one succeeds:

1. **Primary: RSS feed via `web_fetch`**
   Fetch `https://ccfddl.com/conference/deadlines_zh.xml` using the `web_fetch` tool.
   This returns XML with all conferences (including historical ones — you must filter).

2. **Fallback: web_search + web_fetch**
   If the RSS feed fails, search for `site:ccfddl.com {会议名或方向} deadline` and
   fetch relevant result pages.

3. **Last resort**
   Tell the user: "CCFDDL 数据暂时无法获取，建议直接访问 https://ccfddl.com 查看。"
   Never fabricate conference data.

## XML structure and parsing

The feed contains hundreds of `<item>` entries spanning many years. Each item looks like:

```xml
<item>
  <title>AAAI 2022 截稿日期</title>
  <link>https://aaai.org/Conferences/AAAI-22/</link>
  <description>AAAI Conference on Artificial Intelligence 会议时间: February 22 - March 1, 2022 会议地点: Vancouver, British Columbia, Canada 截止时间 (UTC-12): 2021-08-30 23:59:59 分类: 人工智能 (AI) CCF A, CORE A*, THCPL A 会议官网: https://aaai.org/Conferences/AAAI-22/ DBLP索引: https://dblp.org/db/conf/aaai</description>
  <pubDate>Mon, 30 Aug 2021 23:59:59 -1200</pubDate>
  <guid isPermaLink="false">AAAI-2022-abstract-2021-08-30 23:59:59@ccfddl.com</guid>
  <category>AI</category>
</item>
```

### Field extraction from each `<item>`

| 目标字段 | 提取方式 |
|---------|---------|
| 简称 + 年份 | `<title>` — 如 "AAAI 2022 截稿日期"，提取 "AAAI 2022" |
| 截稿类型 | `<title>` 末尾：含 "摘要截稿" → 摘要DDL；含 "截稿日期" → 全文DDL。也可从 `<guid>` 判断：含 `abstract` → 摘要，含 `deadline` → 全文 |
| 全称 | `<description>` 开头到 "会议时间:" 之前的文本 |
| 会议时间 | `<description>` 中 "会议时间:" 与 "会议地点:" 之间的文本 |
| 会议地点 | `<description>` 中 "会议地点:" 与 "截止时间" 之间的文本 |
| 截止时间 | `<description>` 中 "截止时间 (UTC-12):" 后的日期时间字符串 |
| 分类 | `<category>` 标签值，如 "AI"；中文名在 "分类:" 后（如 "人工智能 (AI)"） |
| CCF 等级 | `<description>` 中 "CCF" 后紧跟的字母：A / B / C / N |
| 官网 | `<link>` 标签，或 "会议官网:" 后的 URL |

### 关键：description 是平铺字符串

所有字段用中文标签分隔，没有换行符。按关键词顺序切分：
`会议时间:` → `会议地点:` → `截止时间` → `分类:` → `CCF` → `会议官网:` → `DBLP索引:`

## Filtering（极其重要）

Feed 包含大量历史条目（从 2020 年起）。必须严格过滤：

1. **只保留截止时间在今天之后的条目** — 用 "截止时间 (UTC-12)" 与当前日期比较
2. **去重合并** — 同一会议同一年可能有 "摘要截稿" 和 "截稿日期" 两条，合并为一行展示
3. **同一会议多个年份** — 只保留截止时间未过的最新一届

## Default filter（用户未指定时的默认值）

- **CCF 等级**: A 和 B
- **分类**: CG (计算机图形学与多媒体), AI (人工智能), MX (交叉/综合/新兴)
- 用户明确指定时覆盖对应默认值（如 "只看A类"、"网络方向"）

## Output format

按截稿日期从近到远排序，用表格展示：

```
| 简称 | 全称 | CCF | 截稿日期 (UTC-12) | 会议地点 | 官网 |
|------|------|-----|-------------------|---------|------|
| AAAI 2026 | AAAI Conference on AI | A | 摘要: 08-15 / 全文: 08-22 | Seattle, USA | [链接] |
```

- 同一会议有摘要和全文两个 DDL 时，合并到一行的截稿日期列
- 排序依据：最早的截稿日期
- 表格后附一行汇总："共 X 个会议，最近截稿: {会议名} ({日期})"
- 无匹配结果时："当前没有符合条件且截稿日期未过的会议。可以放宽条件再试。"

## Example interaction

**User**: "最近有什么 AI 方向的 CCF-A 会议可以投？"

1. `web_fetch` 获取 `https://ccfddl.com/conference/deadlines_zh.xml`
2. 解析所有 `<item>`，过滤：`<category>` = AI，CCF = A，截止时间 > 今天
3. 合并同一会议的摘要/全文条目
4. 按截止日期排序，输出表格

**User**: "CVPR 什么时候截稿？"

1. 同样 fetch RSS
2. 在所有 `<item>` 中搜索 title 含 "CVPR" 的条目（不限分类和等级）
3. 只保留截止时间未过的
4. 输出该会议的完整信息

## Important rules

- 所有数据必须来自 CCFDDL feed，严禁编造任何会议信息
- 保留原始时区标注（通常为 UTC-12 / AoE）
- 查询特定会议时（如 "CVPR"），跳过分类和等级的默认过滤，直接按名称搜索
- 用户要求"定期提醒"时，说明 Claude 无法发送定时消息，但可以随时再问
- feed 数据量很大，如果被截断，优先关注 pubDate 较新的条目