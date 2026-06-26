---
name: dianping
description: Help users use Dianping (大众点评) for restaurant discovery, review analysis, store vetting, deal evaluation, and local lifestyle decisions in China. Use when the user wants to find food, compare restaurants, judge whether a store is worth visiting, understand Dianping ratings, avoid review traps, or choose 团购/套餐/咖啡馆/休闲娱乐/本地生活 merchants based on reviews and practical signals.
---

# Dianping

Help users make better decisions on 大众点评 by combining rating interpretation, review reading, store vetting, deal analysis, use-case matching, and browser-based store/deal comparison. Prefer practical judgment over blindly trusting star scores.

## Browser Workflow Upgrade

When the user needs live store-page or deal-page inspection, follow the shared **browser-commerce-base** workflow:
- public store/deal pages → `openclaw`
- logged-in coupon/order pages → `user` only when necessary
- capture score, review count, recent complaints, deal constraints, and location fit
- use screenshots when ranking several candidates

## Quick routing

Read the most relevant reference file when needed:
- **评论分析 / 刷评识别** → `references/reviews.md`
- **团购 / 套餐 / 优惠判断** → `references/deals.md`
- **餐厅 / 咖啡馆 / 甜品店选择** → `references/restaurants.md`
- **按摩 / 美容 / KTV / 密室 / 本地服务** → `references/services.md`

If the user gives several stores or a long batch of reviews, summarize into: **结论 / 理由 / 风险提醒 / 推荐顺位**.

## Core rules

### 1. 先看场景，再看分数
Dianping is not just for “finding a high-score store.” First identify the user’s real need:
- 找餐厅：约会、家庭聚餐、朋友聚会、一个人吃、商务请客
- 找咖啡馆：办公、聊天、拍照、安静坐坐
- 找休闲娱乐：KTV、密室、影院、按摩、美容、美发
- 找本地服务：健身、洗浴、亲子、宠物、培训

A store can be high-rated but still wrong for the specific use case.

### 2. 大众点评评分不能孤立看
Read rating with scale and category in mind:

| Rating | Meaning |
|---|---|
| 4.8–5.0 | Usually excellent, but still check review quality and review count |
| 4.5–4.7 | Often strong and reliable |
| 4.2–4.4 | Mixed; may still be good for value or niche use |
| <4.2 | Requires strong justification before recommending |

Also check:
- **review count**: 评分高但评价少，可信度下降
- **recent reviews**: 过去好不代表现在好
- **category baseline**: 网红甜品、咖啡店、火锅店、按摩店的评分口径不同

### 3. 先看差评，再看好评
For fast vetting, review in this order:
1. recent 1–2 star reviews
2. mid-score reviews
3. photo reviews
4. recent high-score reviews

This gives a more realistic picture than praise-first reading.

### 4. 分清“适合打卡”与“适合复购”
Some stores are photogenic but not practical.

| Signal | 打卡型 | 复购型 |
|---|---|---|
| Photos | Very strong | Moderate |
| Price-performance | Often weak | Usually better |
| Review language | “出片”“拍照好看” | “会再来”“常来” |
| Queue tolerance | Requires patience | More everyday-friendly |

If the user asks for “值得反复去的店,” weight复购 signals more than aesthetics.

### 5. 团购/套餐不要只看便宜
Judge deals by practical fit:
- 是否含真正想点的东西
- 是否限时段/限节假日/限堂食
- 是否需要预约
- 是否对团购用户区别对待
- 单点价格 vs 套餐价格
- 是否存在隐形消费

A good deal is not the cheapest one; it is the best-fit one.

### 6. 输出要解决决策，不是复述评论
Do not dump reviews back to the user. Convert the input into:
- **结论**：值得去 / 谨慎去 / 不建议优先 / 划算 / 一般 / 不建议冲
- **理由**：2–4 条最关键事实
- **风险提醒**：排队、噪音、预约、推销、卫生、隐形收费等
- **推荐顺位**：仅在多店对比时提供

## Decision workflow

### A. Single store judgment
Use when the user asks “这家值不值得去？”

Output pattern:
> 结论：……  
> 理由：……  
> 风险提醒：……

### B. Compare multiple stores
Use when the user gives several options.

Output pattern:
> 推荐顺位：A > B > C  
> A：适合谁 / 优势 / 风险  
> B：适合谁 / 优势 / 风险  
> C：适合谁 / 优势 / 风险

### C. Review analysis
Use when the user gives screenshots/text/review excerpts.

Output pattern:
> 这家店真正稳定的优点是……  
> 真正反复出现的问题是……  
> 对你这个场景，最大的风险是……

### D. Deal/package judgment
Use when the user asks whether a团购/套餐 is worth buying.

Output pattern:
> 结论：划算 / 一般 / 不建议冲  
> 看点：……  
> 风险：……

## Common traps

- 只看总分，不看评价数量
- 被“网红出片”误导
- 忽略近期差评
- 团购只看价格不看限制
- 不区分工作日和周末体验
- 不区分“第一次尝鲜”和“长期复购”
- 把“店很火”误认为“店很稳”

## Example requests

These should trigger this skill:
- 帮我看看这家大众点评上的店值不值得去
- 这几家店怎么选
- 这个团购套餐划算吗
- 大众点评 4.3 分的店还能去吗
- 帮我分析一下评论，有没有刷评感
- 找一家适合约会的餐厅
- 找一家适合一个人安静吃饭的店
- 推荐个适合久坐办公的咖啡馆
- 这家按摩店会不会强推销

## Example outputs

### Example 1
User:
> 这家火锅店 4.6 分，但最近差评都在说排队久，值得去吗？

Output:
> 结论：如果你能接受排队，可以去；如果你更看重效率，不算优先。  
> 理由：4.6 分说明整体口碑不差，但“最近差评集中提排队久”说明高峰期体验有真实摩擦。  
> 风险提醒：周末/晚饭高峰可能很耗时间，建议预约或错峰。

### Example 2
User:
> 这家咖啡馆拍照很好看，适合下午办公吗？

Output:
> 结论：更像打卡型，不一定适合久坐办公。  
> 理由：如果评论主要强调环境和出片，而很少提插座、安静、座位舒适度，通常不适合长时间办公。  
> 风险提醒：下午高峰可能嘈杂，点单价格也可能偏高。

## Final instruction

Judge Dianping merchants by fitness-for-purpose, review quality, friction, and risk — not by star rating alone. Be practical, specific, and experience-oriented.
