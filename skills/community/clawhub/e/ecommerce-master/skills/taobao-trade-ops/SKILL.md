---
name: taobao-trade-ops
description: 淘宝交易管理：订单查询/发货/退款 API 面、对账 SOP、授权与限流要点
source:
  type: external
  url: https://open.taobao.com/api.htm?spm=a219a.7386797.0.0&docType=2&docId=1049
  version: "1.0.0"
  updated: 2026-10-29
metadata:
  category: 淘宝运营
  platform: API
  difficulty: 进阶
---

# 淘宝交易管理（Taobao Trade Ops）

> 订单→发货→售后的 API 面速查与对账 SOP。前提：企业店铺 + TOP 应用已获交易类权限
> （资质门槛判断见 `taobao-product-ops` 的双通道决策表）。

## 能力

- 订单查询：`taobao.trades.sold.get`（卖出订单列表）、`taobao.trade.get`（单笔详情）
- 发货闭环：`taobao.logistics.online.send`（在线下单）/ `taobao.logistics.consign.send`（自有物流）
- 售后处理：退款状态查询与响应（`refund` 系列接口）
- 备注与对账：`taobao.trade.memo.add`（订单备注）+ 对账 SOP

## 使用方式

```
/taobao-trade-ops 拉今天的待发货订单并生成发货清单
/taobao-trade-ops 这笔退款该不该同意？帮我查状态和凭证
/taobao-trade-ops 月底对账：订单流 vs 到账流核对
```

## 核心 API 面（速查）

| 环节 | 接口 | 要点 |
|------|------|------|
| 待发货列表 | `trades.sold.get`（`status=SELLER_CONSIGNED_PART`/`WAIT_SELLER_SEND_GOODS`） | 分页拉取，`use_has_next` 翻页 |
| 单笔详情 | `trade.get`（`fields` 按需选字段，防超量） | 含收货地址、买家留言 |
| 发货 | `logistics.online.send` / `consign.send` | 运单号回传后订单状态推进 |
| 退款 | `refund.refuse`（拒绝需凭证）/ 状态轮询 | 卖家响应有时限，超时自动同意 |
| 订单备注 | `trade.memo.add` | 对账打标用 |

## 对账 SOP（每周/每月）

1. `trades.sold.get` 按 `created` 时间窗拉全量订单 → 存本地（hope-server 每笔必录）
2. 对照支付宝/微信到账流水，差异项打 `trade.memo.add` 标记
3. 退款单单独建表：申请时间、凭证、裁决、到账回冲
4. 差异 > 0.5% 停下人工核查，不自动冲账

## 红线与限制

- 交易类 API **需企业资质**（个体工商户可）；个人开发者仅查询类基础权限
- 所有调用带店铺 `session`（OAuth2.0，Token 过期需刷新机制）
- TOP 限流：批量拉单限速 + 重试退避；`fields` 按需声明避免超限
- 买家隐私字段（手机号/地址脱敏）按平台隐私规范使用，不落日志明文
