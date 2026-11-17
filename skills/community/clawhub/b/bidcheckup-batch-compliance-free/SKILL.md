---
slug: bidcheckup-batch-compliance-free
displayName: 多标书批量合规体检（免费版）
version: 1.0.52
summary: 一次把多家投标文件的报价算术全部核一遍，不需要付款，也不需要注册。 免费、无需注册、无需 API Key。
tags: [招投标, 免费, 逐家报价算术校验, 标书检查, 投标自查]
license: Proprietary
name: bidcheckup-batch-compliance-free
display_name: 多标书批量合规体检（免费版）
display_name_en: BidCheckup Batch Compliance (Free)
description: 一次把多家投标文件的报价算术全部核一遍，不需要付款，也不需要注册。 本免费版执行 逐家报价算术校验。触发词包括 多标书批量合规体检、逐家报价算术校验。
description_zh: 一次把多家投标文件的报价算术全部核一遍，不需要付款，也不需要注册。 本免费版执行 逐家报价算术校验。
description_en: Free batch arithmetic check across up to three bidders in one pass, covering line-item math, totals and written-figure cross-check. No payment, no registration, no API key.
category: office
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 多标书批量合规体检（免费）

> 一句话：一次把多家投标文件的报价算术全部核一遍，不需要付款，也不需要注册。

**完全免费**：不需要付款、不需要注册、不需要配置任何 API Key，直接调用即可。

## 什么时候用

- 一个项目有好几家投标人，想一次性把各家的报价算术都过一遍
- 评标前想先排除「报价算错」这类最容易被质疑的低级问题
- 想知道哪几家的报价明细里有对不上的行

## 这个免费版查什么

| # | 检查项 |
|---|---|
| 1 | 逐家报价算术校验 |

- 逐家报价算术：每家的每一行都核对「合价 = 数量 × 单价」，按投标人分别归集
- 输出逐家 verdict 与问题清单，一眼看出哪几家需要盯

## 这个免费版不包含

以下检查项**不在本版本范围内**，调用时也不会执行：

- 否决条款响应核对
- 模板占位符扫描
- 基本要件扫描
- 跨家串通线索
- 报价离散度分析
- 按风险排序的整改清单

## 怎么调用

### 方式一：命令行脚本（最省事）

```bash
node scripts/run.mjs --sample
node scripts/run.mjs --input my-input.json
node scripts/run.mjs --input my-input.json --json
```

### 方式二：直接引用引擎（接进自己的流程）

脚本本身不做计算，真正的检查在同目录的 `scripts/engine/batch-quote-checkup.js`（纯 Node 标准库，CommonJS），可以直接引用：

```js
const engine = require('./scripts/engine/batch-quote-checkup.js');
const outcome = engine.run(payload);
// outcome.status === 'success'            → outcome.result 就是结果
// outcome.status === 'insufficient_input' → outcome.missing 列出缺什么（此时不出结论）
```

所有检查都在**本机**完成：核对过程不外发材料、不需要任何凭证。

## 入参

给一个 bidders 数组，每家可带结构化报价明细 items（也可以给可解析成表格的报价文本 text）。本版本不做分项加总校验，所以投标总价 price 字段不使用。

```json
{
  "bidders": [
    {
      "name": "河南甲建设有限公司",
      "price": 1000000,
      "items": [
        {
          "name": "钢筋制安",
          "qty": 10,
          "price": 100,
          "amount": 900
        }
      ]
    },
    {
      "name": "河南乙工程有限公司",
      "price": 1050000,
      "items": [
        {
          "name": "钢筋制安",
          "qty": 10,
          "price": 100,
          "amount": 1000
        }
      ]
    }
  ]
}
```

## 返回

返回 `ok: true` 与 `result`：`checks_given` **原样列出本次实际执行了哪些检查项**，
`checks_withheld` 列出本版本不包含的检查项。**不会用默认值编造结论。**

材料不足时（入参为空、只有空白、只有一个字符、解析不出任何明细行）**不出结论**：
会说明缺什么，并以退出码 `3` 结束；正常执行退出码为 `0`。

## 使用限制

- 在本机执行：核对过程不外发材料、没有调用次数上限，也不需要任何凭证。
- 输出的是**AI核对结果**，不是认定、不是评分。

## 反模式

- ❌ 把它的输出当作评标结论 —— 它只做AI核对，认定权在评标委员会。
- ❌ 拿它替代对招标文件的实质响应检查 —— 本版本不含该类检查。
- ❌ 输入残缺时怪结果不对 —— 检查项依赖你提供的字段，缺字段的检查项不会被伪造出来。

## 需要完整档时（可选）

本免费版是**完整可用的核心产出**，本版本**不包含**下面这些项：

- 否决条款响应核对
- 模板占位符扫描
- 基本要件扫描
- 跨家串通线索
- 报价离散度分析
- 按风险排序的整改清单

同名工具的**完整档**是另一个独立商品（条款与条件以它自己的商品页为准）；两档的差别**就是上面这些，没有别的**。

## 边界与免责

只做AI算术核对，不做资格审查、不做技术评审、不构成评标意见。

本技能的所有结论都可由第三方用同一份输入复算出来。
