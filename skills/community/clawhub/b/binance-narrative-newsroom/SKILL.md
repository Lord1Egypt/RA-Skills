name: binance-narrative-newsroom
description: 当用户想发现今天最值得写的 Binance 市场热点、查看昨天到今天的阶段变化、整理 watchlist、生成多版本 Binance Square 中文草稿，或输出一张适合分享的热点卡片时使用。
---

# 币安热点编辑部

这个 skill 直接帮用户做今天的热点选题和发帖准备。

它做的是：
从 Binance 官方公开的 Web3 榜单和 Smart Money 信号里，整理出今天最值得写的市场叙事，并给出阶段变化和发布工作台。

公开接口：

- 选题 API: `https://binance-narrative-newsroom.vercel.app/api/newsroom`
- 分享图 API: `https://binance-narrative-newsroom.vercel.app/api/newsroom/share-image`

## 适用场景

- 用户想知道今天 Binance 生态里哪条热点最值得写
- 用户需要一版可直接发到 Binance Square 的中文草稿
- 用户想看某条主线是如何从昨天走到今天的
- 用户想用“社交热度 + 统一热榜 + 聪明钱流入 + Smart Money”来做判断
- 用户想得到 watchlist、反方风险提示和多版本发帖稿，而不是一个简单热榜

## 调用方式

如果用户没有特别指定，默认使用：

- `audience`: `SQUARE`
- `angle`: `MORNING`

可选参数：

- `audience`
  - `TRADER`
  - `SQUARE`
  - `COMMUNITY`
- `angle`
  - `MORNING`
  - `SMART_MONEY`
  - `CONTRARIAN`

调用：

```bash
curl -sS -X POST https://binance-narrative-newsroom.vercel.app/api/newsroom \
  -H 'Content-Type: application/json' \
  -d '{"audience":"SQUARE","angle":"MORNING"}'
```

## 重点字段

- `headline`
- `deckSummary`
- `editorialDecision`
- `leadStory`
- `boardStories`
- `watchlist`
- `avoidList`
- `publishDesk`
- `squareDraft`
- `shareText`

## 输出要求

- 先告诉用户今天的头条选题是什么
- 再解释为什么是这条线，尤其要点明 `leadStory.shift`
- 明确区分：
  - 可写热点
  - 观察名单
  - 不建议直接追的对象
- 如果用户要发帖，优先给 `publishDesk.drafts` 里的多版本正文，再补 `titleOptions` 和 `publishChecklist`
- 如果用户要分享图，把以下字段编码后拼到分享图接口：
  - `symbol`
  - `stage`
  - `resonanceScore`
  - `headline`
  - `summary`
  - `watchline`
  - `generatedAt`
  - `shiftLine`
