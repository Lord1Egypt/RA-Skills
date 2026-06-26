---
name: brand-sentinel
description: >
  品牌舆情哨兵：搜索公开平台的品牌相关信息，自动去重和时效过滤，输出结构化结果供 LLM 做风险分级和预警。
  触发场景：监控某品牌/产品的公开舆情、搜索负面信息并按时间筛选、定时巡查品牌口碑、竞品舆情对比。
  关键词：品牌监控、舆情搜索、负面信息、口碑巡查、舆情预警、品牌声誉、sentinel、舆情哨兵。
  不做的事：不做风险分级（交给 Agent/LLM）、不做预警推送（交给 cron）、不做特定行业适配。
---

# brand-sentinel — 品牌舆情哨兵

搜索公开平台的品牌相关信息 → 去重 → 时效过滤 → 输出结构化结果。

## 核心脚本

`scripts/sentinel.py` — 纯 Python（无第三方依赖），调用 AutoGLM Web Search API。

## 依赖

- Python 3.10+
- 本地 AutoGLM Token 服务运行中（`http://127.0.0.1:18432/get_token`）
- `certifi` 包（SSL 证书，通常已预装）

## 用法

### 命令行

```bash
# 基本用法
python3 scripts/sentinel.py --brand "特斯拉" --keywords "刹车失灵,自燃" --hours 48

# JSON 输出（供 LLM 消费）
python3 scripts/sentinel.py --brand "瑞幸咖啡" --keywords "食品安全,蟑螂" --hours 24 --output json

# 配置文件模式
python3 scripts/sentinel.py --config references/config-example.json
```

### 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--brand` | 是* | 品牌名，如 "特斯拉" |
| `--keywords` | 是* | 逗号分隔的关键词，如 "刹车失灵,自燃" |
| `--hours` | 否 | 时效窗口（小时），默认 48 |
| `--output` | 否 | `text`（默认）或 `json` |
| `--config` | 是* | JSON 配置文件路径（替代上方参数） |

\* `--brand`+`--keywords` 与 `--config` 二选一。

### 配置文件格式

见 `references/config-example.json`：

```json
{
  "brand": "品牌名",
  "keywords": ["关键词1", "关键词2"],
  "hours": 48,
  "output": "json"
}
```

## 输出结构

### JSON 模式

```json
{
  "brand": "特斯拉",
  "run_time": "2026-04-14 19:00:00",
  "time_window_hours": 48,
  "keywords": ["刹车失灵", "自燃"],
  "stats": {
    "raw_count": 85,
    "kept_count": 62,
    "expired_count": 8,
    "no_date_count": 15
  },
  "items": [
    {
      "title": "页面标题",
      "url": "页面链接",
      "snippet": "摘要内容",
      "date_status": "recent|expired|unknown",
      "parsed_date": "2026-04-14|null"
    }
  ]
}
```

### 字段说明

- `date_status`:
  - `recent` — 解析到日期且在时效窗口内 ✅
  - `expired` — 解析到日期但超出时效窗口（已被过滤掉）
  - `unknown` — 未解析到日期（搜索词含"最新"限定，大概率近期，默认保留）
- `parsed_date` — 从标题/摘要提取的日期，解析失败为 `null`

## 工作流程

1. **构建搜索词** — 对每个关键词自动生成 3 种变体：原始词、`+ 最新`、`+ 当前年月`
2. **批量搜索** — 调用 autoglm-websearch，每个词间隔 0.3s
3. **URL 去重** — 同一 URL 只保留首次出现
4. **日期解析** — 从标题+摘要中提取日期（支持"2026年4月14日"、"3天前"、"昨天"等中文格式）
5. **时效过滤** — 超出时间窗口的结果丢弃，无日期的默认保留
6. **输出** — text 或 json 格式

## 典型 Agent 工作流

```
用户: "帮我看看特斯拉最近有什么负面新闻"

1. Agent 调用 sentinel.py:
   python3 scripts/sentinel.py --brand "特斯拉" --keywords "刹车失灵,自燃,自动驾驶事故,降价维权" --hours 48 --output json

2. Agent 读取 JSON 输出，用 LLM 判断:
   - 哪些是真正的负面/危机
   - 风险分级（普通/关注/严重/危机）
   - 是否需要预警

3. Agent 生成人类可读的摘要推送给用户
```

## 注意事项

- 搜索 API 有速率限制，关键词数量建议 ≤10 组（每组会生成 3 个变体，共 30 次搜索）
- 日期解析基于正则匹配，覆盖率约 60-70%，未解析到的默认保留
- 搜索词加"最新"限定可提升近期结果命中率，但不能保证 100% 时效性
- 如需跨次运行去重，Agent 可自行维护 URL 集合
