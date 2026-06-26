---
name: amazon-review-reveyes
version: "1.0.0"
author: reveyes
description: >
  使用 Reveyes API 批量抓取亚马逊商品评论，支持 20 个站点。
  输出评论列表、星级分布统计和差评摘要。
  Use when: 用户提到抓评论、查差评、分析竞品口碑、给出 ASIN 编号需要评论数据。
  NOT for: 分析已经抓好的本地评论文件，或查询亚马逊商品价格/销量。
tags:
  - amazon
  - ecommerce
  - review
  - scraping
  - cross-border
requires:
  env:
    - REVEYES_API_KEY
---

## When to Run

- 用户发送 ASIN 编号并要求抓取评论（如「帮我抓 B08N5WRWNW 的评论」）
- 用户说「帮我看看这个竞品的差评」「分析一下这款产品的用户反馈」
- 用户要对比同一商品在多个亚马逊站点的口碑
- 用户要导出评论数据做分析

## Parameters

从用户消息中提取以下信息：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `asin` | 亚马逊 ASIN，10 位字母数字（必须） | — |
| `marketplace` | 站点代码，见下方列表 | `US` |
| `pages` | 抓取页数（1-10），1 页约 10 条评论 | `2` |
| `filter_star` | 星级筛选：`all_stars` `positive` `critical` `five_star`…`one_star` | `all_stars` |

**支持的站点代码：**
`US` `CA` `MX` `UK` `DE` `FR` `IT` `ES` `NL` `SE` `PL` `BE` `IE` `JP` `IN` `SG` `AE` `SA` `AU` `BR`

## Workflow

1. **提取参数**：从用户消息中识别 ASIN（10 位）、站点代码、页数、星级筛选
   - 若用户只给 ASIN，其余使用默认值
   - 若用户说「差评」自动设置 `filter_star=critical`
   - 若用户说「好评」自动设置 `filter_star=positive`

2. **执行抓取**：调用 `scripts/fetch.py`，传入参数
   ```
   python scripts/fetch.py <ASIN> <marketplace> <pages> <filter_star>
   ```

3. **等待完成**：脚本内部自动轮询（最多 5 分钟），完成后输出 JSON 结果

4. **格式化输出**：
   - 汇总：总评论数、平均评分、各星级占比
   - Top 5 差评（如请求的是 `critical` 或 `all_stars`）：标题 + 正文前 150 字
   - 如评论数 > 20，额外输出高频关键词（从差评标题提取）

5. **错误处理**：
   - `AuthenticationError` → 提示用户检查 `REVEYES_API_KEY`
   - `InsufficientCreditsError` → 提示前往 https://www.reveyes.cn 充值
   - `BadParamsError` → 提示检查 ASIN 或站点代码是否正确
   - `TimeoutError` → 告知任务仍在运行，提供 task_id 供后续查询

## Output Format

```
📦 ASIN: B08N5WRWNW  |  站点: US  |  共 87 条评论

⭐ 评分分布：
  ★★★★★  42 条 (48%)  ████████████
  ★★★★☆  18 条 (21%)  █████
  ★★★☆☆   8 条  (9%)  ██
  ★★☆☆☆   5 条  (6%)  █
  ★☆☆☆☆  14 条 (16%)  ████

📝 典型差评（最近 5 条）：
1. ★★ "Stopped working after 2 weeks"
   Bought this expecting quality but it broke down...

2. ★★ "Not as described"
   The color is completely different from the photos...

[查看完整结果或导出 CSV，请告诉我]
```
