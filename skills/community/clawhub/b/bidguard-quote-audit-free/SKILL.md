---
slug: bidguard-quote-audit-free
displayName: 投标报价AI审查（免费版）
version: 1.0.54
summary: 把一份投标报价单里能被算出来证明是错的问题找出来，不需要付款，也不需要注册。 免费、无需注册、无需 API Key。
tags: [招投标, 免费, 分项算术校验, 标书检查, 投标自查]
license: Proprietary
name: bidguard-quote-audit-free
display_name: 投标报价AI审查（免费版）
display_name_en: BidGuard Quote Audit (Free)
description: 把一份投标报价单里能被算出来证明是错的问题找出来，不需要付款，也不需要注册。 本免费版执行 分项算术校验、缺漏项提示。触发词包括 投标报价AI审查、分项算术校验、缺漏项提示。
description_zh: 把一份投标报价单里能被算出来证明是错的问题找出来，不需要付款，也不需要注册。 本免费版执行 分项算术校验、缺漏项提示。
description_en: Free mechanical audit of a single bid quotation across line-item arithmetic, totals, the tender upper price cap and the written-figure cross-check.
category: business-ops
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 投标报价AI审查（免费）

> 一句话：把一份投标报价单里**能被算出来证明是错的**问题找出来，不需要付款，也不需要注册。

**完全免费**：不需要付款、不需要注册、不需要配置任何 API Key，直接调用即可。

## 什么时候用

- 报价单里某几行的「合价」跟「数量 × 单价」对不上
- 有几行只填了数量没填单价，或者只填了单价没填合价
- Excel 里拉完公式想再核一遍，但不想手工逐行看
- 投标前想先跑一遍，看看有没有低级算术错误

## 这个免费版查什么

| # | 检查项 |
|---|---|
| 1 | 分项算术校验 |
| 2 | 缺漏项提示 |

- 分项算术：每行核对「合价 = 数量 × 单价」，偏差一并给出差额
- 缺漏项：数量、单价、合价任一为空的行会被单独指出（这类行在评标时最容易被挑）

## 这个免费版不包含

以下检查项**不在本版本范围内**，调用时也不会执行：

- 分项加总校验
- 最高投标限价校验
- 大小写金额互校
- 投标保证金比例校验
- 不平衡报价预警

## 怎么调用

### 方式一：命令行脚本（最省事）

```bash
node scripts/run.mjs --sample
node scripts/run.mjs --input my-input.json
node scripts/run.mjs --input my-input.json --json
```

### 方式二：直接引用引擎（接进自己的流程）

脚本本身不做计算，真正的检查在同目录的 `scripts/engine/quote-audit.js`（纯 Node 标准库，CommonJS），可以直接引用：

```js
const engine = require('./scripts/engine/quote-audit.js');
const outcome = engine.run(payload);
// outcome.status === 'success'            → outcome.result 就是结果
// outcome.status === 'insufficient_input' → outcome.missing 列出缺什么（此时不出结论）
```

所有检查都在**本机**完成：核对过程不外发材料、不需要任何凭证。

## 入参

两种入参二选一：把 Excel 报价表直接粘贴成文本，或给结构化 JSON。

```json
{
  "text": "序号\t项目名称\t数量\t单价\t合价\n1\t土方开挖\t100\t25\t2500\n2\t混凝土浇筑\t50\t400\t19000\n3\t钢筋制安\t\t3800\t76000"
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

- 分项加总校验
- 最高投标限价校验
- 大小写金额互校
- 投标保证金比例校验
- 不平衡报价预警

同名工具的**完整档**是另一个独立商品（条款与条件以它自己的商品页为准）；两档的差别**就是上面这些，没有别的**。

## 边界与免责

只做AI算术核对，不做技术标评审、不做资格判定、不构成评标意见。

本技能的所有结论都可由第三方用同一份输入复算出来。
