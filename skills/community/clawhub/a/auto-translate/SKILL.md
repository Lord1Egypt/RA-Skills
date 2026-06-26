---
name: auto-translate
description: 自动三语翻译技能。在回答用户问题时，自动在中文回答后附上英文翻译和日文翻译。触发场景包括：用户要求翻译、要求回复附带英日文、回答后附翻译、或任何中英日三语输出场景。
---

# auto-translate — 中英日三语翻译技能

## 核心逻辑

每次回答用户问题时，严格按以下顺序输出：

1. **中文回答**（完整、自然、言必有据）
2. **英文翻译**：跟上中文回答的英文翻译
3. **日文翻译**：跟上中文回答的日文翻译

## 输出格式

```
[中文回答正文]

英文翻译：[English translation]
日文翻訳：[日本語翻訳]
```

## 示例

**输入：** 什么叫ETF？

**输出：**
> ETF（Exchange Traded Fund）即交易所交易基金，是一种在证券交易所上市交易的、可以像股票一样买卖的开放式基金。它兼具封闭式基金和开放式基金的特点，投资者既可以在二级市场按市场价格买卖，也可以在发行商处进行申购和赎回。
>
> 英文翻译：ETF (Exchange Traded Fund) is an exchange-traded fund listed and traded on stock exchanges, similar to stocks. It combines the characteristics of both closed-end and open-end funds, allowing investors to buy and sell at market prices on the secondary market, as well as subscribe and redeem from the issuer.
>
> 日文翻訳：ETF（Exchange Traded Fund）は証券取引所に上場・取引されているファンドで、株式のように売買できるオープン型ファンドです。決算型ファンドと開放型ファンドの両方の特徴を兼ね備え、投資家は二级市場で時価売買できる他に、発行会社での申购・償還も可能です。

## 翻译要求

- **准确性**：忠实传达原意，不遗漏关键信息
- **自然通顺**：目标语言表达自然流畅，符合地道习惯
- **术语一致**：专业术语使用标准译法（如 ETF、P/E 等）
- **不添加额外解释**：翻译内容仅包含回答本身，不另加注释或评论
- **标签明确**：英文标签用"英文翻译："，日文标签用"日文翻訳："

## 何时使用本技能

- 用户明确要求翻译、多语言输出时
- 用户要求回答后附英日文翻译时
- 用户要求每个回答都翻译时

## 注意事项

- 如果回答中包含数据、代码、公式等，保持原样不翻译
- 人名、地名、专有名词可保留原文或附上惯用译法
- 翻译标籖语言跟随目标语言（中文回答 → 英文翻译 / 日文翻訳）
