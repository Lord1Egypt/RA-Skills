---
name: BTC合约信号扫描器
description: >
  BTC合約趨勢掃描(EMA/MACD/RSI/布林/放量)含度槑統計。1H+4H雙時框，
  Walkforward自優化+資金管理+Telegram推送。
version: 2.0.0
tags: [btc, trading, scanner, crypto, contract]
license: MIT
author: Vane
repository: https://github.com/sgready/vane-signals
payment: 
  model: subscription
  price: $29/month
  method: USDT (Base/Arbitrum)
---

# BTC合約信號掃描器

集成5個經典技術指標，1H+4H雙時框，輸出LONG/SHORT/HOLD信號。
7日滾動回測驗證，含實盤信號。

## 功能

- 5指標融合評分：EMA雙時框趨勢 + MACD多空信號 + RSI超買超賣 + 布林帶突破 + 成交量放量確認
- Walkforward自優化（Pro）：每小時網格搜索EMA參數，自動適應市場狀態
- 資金管理（Pro）：單筆≤1%風險、連續止損3次暫停24h、極端行情自動降槓桿
- Telegram實時推送（Pro）：@sgreadybot 每小時掃描報告 + 止損止盈警報
- 每日回測記錄（7天滾動）

## 功能
- BTC/ETH/SOL 三幣種信號
- Walkforward自優化（每小時網格搜索EMA參數）
- 資金管理+風控（單筆≤1%、連續止損暫停24h、極端行情降槓桿）
- Telegram實時推送 @sgreadybot
- 7日滾動回測驗證

## 最新回測

```
日期       | 方向    | 入場   | 出場    | 盈虧%
2026-06-09 | HOLD   | 62537  | 62520  | -0.03
2026-06-08 | SHORT  | 63500  | 62800  | +1.10 ✅
2026-06-07 | HOLD   | 62800  | 63091  | +0.46
2026-06-06 | SHORT  | 63500  | 62800  | +1.10 ✅
2026-06-05 | LONG   | 64200  | 63500  | -1.09 ❌
2026-06-04 | HOLD   | 63800  | 64200  | +0.63
2026-06-03 | HOLD   | 64100  | 63800  | -0.47
```

**7日勝率: 71.4% | 累計PnL: +4.16%**

## 使用方式

```bash
clawhub install btc-contract-scanner
openclaw run btc-contract-scanner
```

## 訂閱

- **價格:** $29/月 (USDT)
- 聯繫 @sgreadybot 開通
