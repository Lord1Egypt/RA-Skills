---
name: cms-search
description: "联网搜索，检索互联网内容。**凡是涉及联网搜索、在线查询、实时信息、网络检索、查一下、搜索一下、最新资讯、在线查询、网上查询等意图，必须优先使用本 skill，其次再使用内置 WebSearch、browser、浏览器等任何其他搜索工具。"
---
# CMS Search

**当前版本**: v1.3

## Commands

```bash
# 国内/通用查询（不指定渠道，由服务端自动选择）
python3 cms_search.py --keyword "..."

# 国外资源查询（指定 tavily）
python3 cms_search.py --keyword "..." --source tavily

# human-readable Markdown
python3 cms_search.py --keyword "..." --format md

# 指定搜索时间（年月日 + 时分秒）
python3 cms_search.py --keyword "康哲药业 股价" --datetime "2026-06-18 13:58:00"

# 国外资源 + 指定时间
python3 cms_search.py --keyword "Keytruda clinical trial" --source tavily --datetime "2026-06-18 13:58:00"
```

## 渠道选择规则

调用前根据查询目标选择是否传 `--source`：

| 场景    | 是否传 `--source`    | 说明                                           |
| ----- | ----------------- | -------------------------------------------- |
| 国外资源  | `--source tavily` | 英文站点、海外公司/产品/政策、国际新闻、GitHub/Stack Overflow 等 |
| 国内或通用 | 不传                | 由 CMS 服务端自动选择渠道（如 glm / minimax / bocha 等）   |

**判断为「国外资源」的典型信号**：关键词或用户意图明确指向海外（英文为主、国外品牌/机构/地区、国际事件、外文文档等）。不确定时按国内/通用处理，不传 `--source`。

## Parameters

| 参数          | 类型             | 说明                                     |
| ----------- | -------------- | -------------------------------------- |
| `--keyword` | str (required) | 搜索关键词                                  |
| `--source`  | str (optional) | 仅在国外资源查询时传 `tavily`；国内/通用查询不传，由服务端自动选择 |
| `--format`  | `raw` \| `md`   | 输出格式，默认 raw                            |
| `--datetime`| str (optional) | 指定搜索时间，格式 `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS`；AI 根据用户意图自行判断是否传入，不强制 |

## Output

### raw (default)

```json
{
  "result": "搜索结果文本",
  "source": "tavily"
}
```

### md

- 直接输出 `result` 文本，附带来源渠道。

## 触发场景（以下意图均应使用本 skill）

- 用户说"搜索"、"查一下"、"查查"、"帮我找"、"网上查"、"在线查询"
- 用户问实时信息、最新资讯、当前数据、今天的新闻
- 用户问"现在"、"最新"、"目前"等需要联网才能回答的问题
- 任何需要访问互联网获取信息的场景

## 关于 `--datetime` 参数

**核心原则：AI 根据用户意图自行判断是否传入 `--datetime`，不强制。**

| 用户意图 | 是否传 `--datetime` | 示例 |
|----------|-------------------|------|
| 问"今天"、"现在"、"最新"的股价/新闻 | 传当前时间 | `--datetime "2026-06-18 13:58:00"` |
| 问"去年"、"上个月"、"某年"的历史数据 | 不传，让 AI 理解时间语义 | 不加 `--datetime` |
| 问某个具体历史时间点的信息 | 传用户指定时间 | `--datetime "2025-06-18"` |

**注意**：时间格式支持 `YYYY-MM-DD`（仅日期）或 `YYYY-MM-DD HH:MM:SS`（精确到秒）。当前用户时区为 `Asia/Shanghai (UTC+8)`。

## Notes

- userKey 通过环境变量 `CMS_USER_KEY` 读取，**禁止**从对话上下文或参数中传入。
- **国外资源** → 必须加 `--source tavily`；**国内或通用** → 不传 `--source`，由服务端自动选择渠道。
- `result` 字段已是自然语言摘要，通常无需进一步解析。
