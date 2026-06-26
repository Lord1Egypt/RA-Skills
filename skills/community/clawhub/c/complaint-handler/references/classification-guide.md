# Complaint Classification Guide

## Two-Pass Classification

### Pass 1: Check for immediate L3 triggers (keyword scan)
Run before any other processing. If any trigger matches → L3 immediately, no further analysis.

**L3 keyword groups:**
```
legal:    律师, 法院, 起诉, 法律途径, 诉讼, 打官司
media:    媒体, 曝光, 记者, 微博, 抖音, 小红书发, 直播
authority: 消协, 12315, 工商局, 市场监管, 食药监
threat:   骗子, 假货, 欺诈, 虚假宣传, 坑人, 黑心
repeat:   (same issue_id seen 3+ times in session history)
```

If L3 triggered: log `{ "class": "escalation_threat", "level": "L3", "keyword": "<matched>" }`
then execute L3 handoff immediately.

---

### Pass 2: Classify complaint type

Score each class based on keyword presence in the message:

| Class | Keywords | Score trigger |
|-------|---------|--------------|
| `quality_issue` | 质量, 坏了, 破损, 开线, 褪色, 起球, 异味, 变形, 脱色, 有问题 | ≥ 1 match |
| `size_fit_issue` | 尺寸, 不合适, 太大, 太小, 偏大, 偏小, 换码, 换个码, 版型 | ≥ 1 match |
| `wrong_item` | 发错, 不对, 和图片不一样, 不是我要的, 颜色不对, 款式不对 | ≥ 1 match |
| `refund_request` | 退款, 退钱, 要退, 不要了, 申请退 | ≥ 1 match |
| `exchange_request` | 换货, 换一个, 换个, 重发, 补发 | ≥ 1 match |
| `service_complaint` | 态度, 服务, 等太久, 没人理, 不专业, 冷漠 | ≥ 1 match |
| `general_dissatisfaction` | 不满意, 失望, 很差, 很烂, 差评 | ≥ 1 match |

**Priority order** (when multiple classes match):
1. `quality_issue` (highest — impacts safety/product liability)
2. `wrong_item`
3. `refund_request`
4. `exchange_request`
5. `size_fit_issue`
6. `service_complaint`
7. `general_dissatisfaction` (lowest)

---

## Permission Level Lookup

| Class | Default Level | Override conditions |
|-------|--------------|-------------------|
| `quality_issue` | L1 | → L2 if amount > threshold |
| `size_fit_issue` | L0 | Stock available; else L1 |
| `wrong_item` | L1 | Always — operational error |
| `refund_request` | L1 (< threshold) / L2 (> threshold) | See `permissions_config.refund_small/large` |
| `exchange_request` | L1 | |
| `service_complaint` | L0 | → L2 if customer specifically requests manager |
| `escalation_threat` | L3 | Immediate, no override |
| `general_dissatisfaction` | L0 | |

---

## Context Enrichment

Before responding, collect these contextual facts (ask if not provided):

| Field | Why needed |
|-------|-----------|
| Purchase date | Determines which policy applies (7-day, 30-day, etc.) |
| Product name/SKU | Confirms which item and policy tier |
| Issue description | Determines class and response |
| Purchase channel | Online vs. in-store may have different policies |
| Desired resolution | Refund vs. exchange vs. repair vs. explanation |

Collect only what's missing. Don't interrogate customers who've already given context.
