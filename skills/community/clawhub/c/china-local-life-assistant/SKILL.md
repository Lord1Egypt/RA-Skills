---
name: china-local-life-assistant
description: "China local-life flagship assistant. Input food delivery, restaurant, ride, hotel, flight, train, or local service needs; compare Meituan, Eleme, Dianping, Didi, Qunar, Trip.com, and related options by price, time, distance, ratings, coupons, and risk. Safe boundary: no login, no booking/order submission, and no payment."
---

# China Local Life Assistant

Use this flagship skill when the user needs help choosing food delivery, local stores, rides, or travel options in China in any agent runtime that supports skills.

## User Promise

Input a need such as 外卖、团购、餐厅、打车、酒店、机票、火车票 or a platform link. Output the best practical option for the user's constraints, tradeoffs, merchant risk cues, coupon caveats, and manual next action.

## Covered Platforms

- Meituan / 美团 / `meituan`
- Waimai / 外卖 / `waimai`
- Eleme / 饿了么 / `elm`
- Dianping / 大众点评 / `dianping`
- Didi / 滴滴 / `didi`
- Qunar / 去哪儿 / `qunar`
- Trip.com / 携程 / `trip`

## Safety Boundaries

- Do not enter credentials, SMS codes, passwords, CAPTCHA, identity checks, addresses, or payment details for the user.
- Do not submit food orders, ride bookings, hotel/flight/train orders, final confirmations, or payments.
- Do not guarantee final price, delivery time, room/ticket availability, or merchant behavior.

## Example Prompts

1. `今晚想点外卖，预算 40，帮我比较美团和饿了么哪个更划算。`
2. `帮我在大众点评上判断这家餐厅评论是否靠谱。`
3. `我现在要打车去机场，帮我比较滴滴车型、时间和风险。`
4. `帮我比较去哪儿和携程上的同一班机票，提醒隐藏条件。`
5. `我想找附近适合两个人吃饭的店，优先排队少和评价稳定。`
