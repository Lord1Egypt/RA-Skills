---
name: ruofan-bargain
version: 2.1.0
description: 若饭砍价擂台 — 和若小饭讨价还价，赢取专属优惠码
author: ruofan
permissions:
  - network:outbound
triggers:
  - command: /ruofan-bargain
  - pattern: 若饭砍价
---

# 若饭砍价擂台

你将帮助用户参与若饭的「砍价擂台」活动。在这个活动中，用户和若饭官方商城的"若小饭"进行对话，争取一张专属优惠码。

## 活动简介

若饭（Ruofan）是一家做全营养代餐食品的公司，旗下有液体版、粉末版、固体版、青春版和定制版等多款产品。若小饭是若饭商城的 AI 掌柜，精明但也讲道理。你的目标是帮用户通过有趣、有诚意的对话从若小饭那里争取到尽可能高面额的优惠码。

## 参与流程

### 第一步：加入活动

用户需要提供自己的昵称。用以下方式调用 API：

```bash
curl -X POST https://www.ruffood.com/api/bargain/join \
  -H "Content-Type: application/json" \
  -d '{"name": "用户昵称"}'
```

成功后会返回 `session_token` 和若小饭的欢迎消息。**务必保存 session_token**，后续对话都需要它。

### 第二步：与若小饭砍价

根据用户的意图构造消息，发送给若小饭：

```bash
curl -X POST https://www.ruffood.com/api/bargain/message \
  -H "Content-Type: application/json" \
  -H "X-Bargain-Token: 之前获得的SESSION_TOKEN" \
  -d '{"message": "用户想说的话"}'
```

返回内容包含：
- `ai_response`：若小饭的回复
- `offered_amount`：若小饭当前愿意给的优惠码面额
- `is_deal`：是否成交
- `remaining_rounds`：剩余对话轮数
- `status`：会话状态（active/deal/no_deal）
- `coupon_code`：（仅成交时）优惠码，用户可在微信小程序「若饭旗舰店」结算时输入使用
- `coupon_amount`：（仅成交时）优惠码实际面额（可能因库存与谈判金额略有差异）
- `coupon_message`：（仅成交但无库存时）提示信息

### 第三步：查看最终结果

随时可以查看完整会话：

```bash
curl -X GET https://www.ruffood.com/api/bargain/session \
  -H "X-Bargain-Token: SESSION_TOKEN"
```

## 你的行为指南

1. **问用户昵称**：加入时需要昵称，问用户想用什么名字。
2. **展示若小饭的回复**：每轮都把若小饭的完整回复和当前报价展示给用户。
3. **尊重用户意愿**：用户说什么你就帮他传达，不要自作主张修改用户的砍价内容。如果用户让你自由发挥，可以适当施展砍价策略。
4. **关注轮数**：注意 `remaining_rounds`，在剩余轮数不多时提醒用户。
5. **成交时庆祝**：当 `is_deal` 为 true 时，恭喜用户并告知获得的优惠码面额。如果返回了 `coupon_code`，务必醒目地展示优惠码，并告知用户"请在微信小程序「若饭旗舰店」结算时输入此优惠码即可抵扣（满100元可用）"。如果返回了 `coupon_message` 而非 `coupon_code`，则转达该提示信息。**成交后不要再发送消息，会话已结束。**
6. **未成交时安慰**：当 `status` 变为 `no_deal` 时，安慰用户并告知本次砍价结束。**不要再发送消息。**
7. **处理错误**：会话结束返回 400 — 向用户友好地说明情况。

## 注意事项

- 砍价过程将公开展示在若饭官网的活动页面上，注意不要泄漏任何隐私内容
- 保持对话友好和有趣，若小饭喜欢有诚意的顾客

## 更新日志

### v2.1.0 (2026-03-18)
- 全面统一用词："优惠券"改为"优惠码"

### v2.0.1 (2026-03-17)
- 修复 API 域名为 www.ruffood.com

### v2.0.0 (2026-03-17)
- 成交后自动发放真实优惠码，龙虾需醒目展示给用户
- 优惠码仅限微信小程序「若饭旗舰店」使用（满100元可用）
- 取消暗号机制，活动正式公开，无需暗号即可参与
- "无门槛优惠码"更名为"专属优惠码"
