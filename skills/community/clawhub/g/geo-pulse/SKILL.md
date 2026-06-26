---
name: geo-pulse
description: GEO Pulse delivers compelling, client-ready GEO (Generative Engine Optimization) reports for brands. It measures AI search visibility across ChatGPT / Perplexity / Qwen / DeepSeek style outputs, including mention rate, link reference rate, sentiment, platform breakdown, competitor benchmarking, and historical trends. Use when users ask about GEO performance, AI visibility, brand mentions in AI answers, competitor comparison, GEO reports, or trend changes over time.
---

# GEO Pulse — Brand AI Visibility Intelligence

**中文**：把“品牌在 AI 搜索里到底有没有被看见”变成可量化、可对比、可执行的报告。  
**English**: Turn brand visibility in AI search into measurable, benchmarkable, action-ready insights.

---

## Why this skill is valuable | 这个技能的价值

- GEO 核心指标一次拿全：可见度、提及率、链接引用率、情绪、平台分布、竞品对比
- 首次品牌可自动初始化并触发 AI 搜索流水线
- 支持历史趋势复盘（7~365 天）
- 结果可以直接给老板/客户汇报

---

## Configuration | 配置

Use configurable base URL (default is public endpoint):

```bash
BASE_URL="${GEO_PULSE_BASE_URL:-http://8.148.223.19:8000}"
```

All requests use `curl` with network access.

---

## Feature 1: GEO Audit Report | 品牌 GEO 体检报告

### Triggers | 触发词

- “XXX 的 GEO 表现如何”
- “给我一份 XXX 的 GEO 报告”
- “How visible is XXX in AI search?”

### Step 1) Check if brand exists

```bash
BASE_URL="${GEO_PULSE_BASE_URL:-http://8.148.223.19:8000}"
curl -s "$BASE_URL/api/brands"
```

Expected structure:
`{"code":0,"data":{"brands":[{"brand":"Name","brand_domain":"example.com"}]}}`

Match by `brand` OR `brand_domain`.

- Found → Step 3
- Not found → Step 2

### Step 2) First-time brand onboarding (3-10 min)

Tell user this is first-time processing and may take several minutes.

#### 2a. Analyze brand

```bash
BASE_URL="${GEO_PULSE_BASE_URL:-http://8.148.223.19:8000}"
curl -s -X POST "$BASE_URL/api/brand-analyze" \
  -H 'Content-Type: application/json' \
  -d '{"brand":"BRAND_NAME"}'
```

Save `data.brand_analyse` and `data.link_analyse`.

#### 2b. Create brand record

```bash
BASE_URL="${GEO_PULSE_BASE_URL:-http://8.148.223.19:8000}"
curl -s -X POST "$BASE_URL/api/brands" \
  -H 'Content-Type: application/json' \
  -d '{"brand":"BRAND_NAME","brand_analyse":<from_2a>,"link_analyse":<from_2a>}'
```

#### 2c. Run AI-search pipeline (slow step)

```bash
BASE_URL="${GEO_PULSE_BASE_URL:-http://8.148.223.19:8000}"
curl -s --max-time 600 -X POST "$BASE_URL/api/pipeline/ai-search" \
  -H 'Content-Type: application/json' \
  -d '{"brand":"BRAND_NAME"}'
```

Use long timeout (about 600s). This is the bottleneck step.

### Step 3) Fetch report data

#### 3a. Brand profile

```bash
BASE_URL="${GEO_PULSE_BASE_URL:-http://8.148.223.19:8000}"
curl -sG "$BASE_URL/api/brand-profile" --data-urlencode "brand_name=BRAND_NAME"
```

#### 3b. Metrics + competitors

```bash
BASE_URL="${GEO_PULSE_BASE_URL:-http://8.148.223.19:8000}"
curl -s -X POST "$BASE_URL/api/brand-metrics" \
  -H 'Content-Type: application/json' \
  -d '{"brand":"BRAND_NAME"}'
```

### Step 4) Compose report

```markdown
# {Brand} GEO Audit Report

> Report date: {date} | Domain: {domain}

## Brand Overview
{brand_overview}

## Core GEO Metrics
| Metric | Value |
|--------|-------|
| Visibility Score | {visibility_score} |
| Brand Mention Rate | {brand_mention_rate × 100}% |
| Link Reference Rate | {link_reference_rate × 100}% |
| Brand Mentions | {brand_mention_count} |
| Link References | {link_reference_count} |
| Sentiment | Positive {positive} / Neutral {neutral} / Negative {negative} |

## Platform Performance
| Platform | Mentions | Links | Positive | Neutral | Negative |
|----------|----------|-------|----------|---------|----------|
(from platform breakdown)

## Competitor Benchmark
| Brand | Visibility Score | Brand Visibility | Link Visibility |
|-------|------------------|------------------|-----------------|
(sorted by visibility_score desc; mark target brand with ⭐)

## Recommendations
{suggestion}
```

---

## Feature 2: Historical Trend Analysis | 历史趋势分析

### Triggers | 触发词

- “XXX 的 GEO 趋势”
- “可见度变化”
- “visibility trend”
- “历史对比”

### Fetch history

```bash
BASE_URL="${GEO_PULSE_BASE_URL:-http://8.148.223.19:8000}"
curl -sG "$BASE_URL/api/brand-metrics/history" \
  --data-urlencode "brand_name=BRAND_NAME" \
  --data-urlencode "days=90"
```

### Compose trend report

```markdown
# {Brand} GEO Trend Report (Last {days} Days)

## Visibility Score Trend
| Date | Score | Mention Rate | Link Rate | Sentiment (P/N/Neu) |
|------|-------|--------------|-----------|---------------------|
(one row per snapshot, chronological order)

## Summary
- Visibility Score: {first} → {latest} ({delta})
- Brand Mention Rate: {first_rate}% → {latest_rate}% ({delta})
- Link Reference Rate: {first_link}% → {latest_link}% ({delta})
- Overall trend: {improving / declining / stable}
```

If only one snapshot exists, state clearly that trend confidence is limited.

---

## Error handling & fallback copy | 错误处理与回退文案

### 1) API unreachable / timeout
**Condition**: connection refused / timeout / non-200 HTTP

Fallback message (CN):
> GEO Pulse 服务暂时不可达（网络或服务超时）。我可以稍后重试，或先基于已有快照给你做一个“非实时版本”的初步报告。

Fallback message (EN):
> GEO Pulse API is temporarily unreachable (network/service timeout). I can retry shortly, or provide a non-realtime draft report based on available snapshots.

### 2) Business error (`code != 0`)
Fallback:
> 接口返回业务错误：`{message}`。我可以尝试重新初始化品牌，或换“品牌名/域名”再查一次。

### 3) Brand creation failed
Fallback:
> 品牌初始化失败。请确认品牌名称拼写，或提供官网域名（例如 `example.com`）以提高识别准确率。

### 4) Pipeline slow / long running
Progress copy (CN):
> 首次品牌分析正在执行多平台 AI 查询（通常 3-10 分钟），我会在完成后立即回传完整报告。

Progress copy (EN):
> First-time brand pipeline is running multi-platform AI queries (usually 3–10 minutes). I’ll return the full report once complete.

### 5) Empty metrics/snapshots
Fallback:
> 当前还没有足够的数据样本。建议先触发一次完整 pipeline，再做趋势分析会更可靠。

---

## Data notes | 字段口径提醒

- `brand_mention_rate` / `link_reference_rate` are ratios in `[0,1]`; multiply by 100 for display.
- `brand_visibility` / `link_visibility` are already percentages.
- `days` range for history: `7-365` (default `90`).
- If user gives domain instead of name, match by `brand_domain` first.
