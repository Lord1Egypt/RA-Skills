---
name: china-commerce-copilot
description: Route shopping and ordering requests to the right China commerce skill, then frame the decision in the most useful way. Use when the user asks where to buy something in China, 哪个平台更合适、淘宝/天猫/京东/拼多多/唯品会/外卖该用哪个、先别执行只帮我判断入口、帮我选最适合的购物平台, or needs a shopping copilot that chooses the right platform-specific skill before deeper analysis.
---

# China Commerce Copilot

China commerce entry router for the shopping skill matrix.

This skill should be triggered before deeper shopping analysis when the user has not yet made clear:
- which platform they should use
- whether they need platform-native guidance or cross-platform comparison
- whether the task is goods shopping or takeout ordering

## Core Job

Do two things, in order:

1. Identify the true shopping intent.
2. Route to the best specialist skill and explain why.

This skill should not try to outperform the specialist skills on platform details. Its value is accurate routing and good framing.

## Routing Map

Route to these skills:

- `alibaba-shopping`
  Use when the user is choosing between Taobao, Tmall, and 1688.

- `taobao-shopping`
  Use when the user wants Taobao-only listing, seller, or variant evaluation.

- `taobao-competitor-analyzer`
  Use when the user wants the same or closest-matching item compared across Taobao, JD, PDD, and Vipshop.

- `jd-shopping`
  Use when trust, self-operated stores, fulfillment speed, and after-sales matter most.

- `pdd-shopping`
  Use when lowest practical price, subsidies, or group-buy mechanics matter most.

- `tianmao`
  Use when flagship stores, authenticity, and brand-official channels matter most.

- `vip`
  Use when branded discount inventory, flash sales, and Vipshop-specific benefits matter most.

- `waimai`
  Use when the task is takeout ordering economics rather than goods shopping.

## Classification Rules

Classify the user request using these questions:

1. Is the user choosing a platform or already inside one platform
2. Is the user comparing the same item across platforms
3. Is the user prioritizing trust, lowest price, authenticity, brand discount, or convenience
4. Is the task goods shopping or takeout ordering
5. Does the user want decision support only or deeper shopping assistance

## Fast Heuristics

Use these strong defaults:

- mentions `淘宝 vs 京东` or `哪个平台更划算`
  -> `taobao-competitor-analyzer`

- mentions `淘宝店铺`, `同款太多`, `这家店能买吗`
  -> `taobao-shopping`

- mentions `淘宝/天猫/1688 哪个更合适`
  -> `alibaba-shopping`

- mentions `京东自营`, `售后`, `发货快`
  -> `jd-shopping`

- mentions `拼多多`, `百亿补贴`, `拼团`, `便宜`
  -> `pdd-shopping`

- mentions `官方旗舰店`, `88VIP`, `正品`
  -> `tianmao`

- mentions `唯品会`, `特卖`, `品牌折扣`, `超级VIP`
  -> `vip`

- mentions `外卖`, `满减`, `配送费`, `起送价`
  -> `waimai`

## Output Contract

Return a short routing answer first:

- `建议入口`
- `为什么`
- `如果用户继续问，下一步该用哪个 skill`

If the route is obvious, route directly and continue with that framing.

If the route is ambiguous, ask one short clarification, for example:
- `你更在意最低价、正品保障，还是配送/售后？`
- `你是想在淘宝站内挑店，还是想跨平台比价？`

## Boundary

- Do not pretend this skill itself is the best specialist for every platform.
- Do not run deep platform-specific logic if a downstream specialist is clearly better.
- Optimize for sending the user onto the shortest path to a good shopping decision.
