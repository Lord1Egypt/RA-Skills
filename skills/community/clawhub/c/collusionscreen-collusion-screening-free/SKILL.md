---
slug: collusionscreen-collusion-screening-free
displayName: 串通投标线索筛查（免费版）
version: 1.0.52
summary: 把多家投标文件放在一起，找出客观可复算的雷同线索，不需要付款，也不需要注册。 免费、无需注册、无需 API Key。
tags: [招投标, 免费, 联系方式一致, 标书检查, 投标自查]
license: Proprietary
name: collusionscreen-collusion-screening-free
display_name: 串通投标线索筛查（免费版）
display_name_en: CollusionScreen (Free)
description: 把多家投标文件放在一起，找出客观可复算的雷同线索，不需要付款，也不需要注册。 本免费版执行 联系方式一致、项目成员交叉。触发词包括 串通投标线索筛查、联系方式一致、项目成员交叉。
description_zh: 把多家投标文件放在一起，找出客观可复算的雷同线索，不需要付款，也不需要注册。 本免费版执行 联系方式一致、项目成员交叉。
description_en: Free cross-bidder screening for objective bid-rigging clues, such as identical contact details and overlapping project staff.
category: office
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 串通投标线索筛查（免费）

> 一句话：把多家投标文件放在一起，找出**客观可复算**的雷同线索，不需要付款，也不需要注册。

**完全免费**：不需要付款、不需要注册、不需要配置任何 API Key，直接调用即可。

## 什么时候用

- 怀疑几家投标人的文件出自同一只手，但说不清依据在哪
- 想核对不同投标人的联系电话、邮箱、账号是不是同一个
- 想核对项目经理、技术负责人这些关键人名有没有跨家重复
- 招标代理在开标前做一轮客观线索预检

## 这个免费版查什么

| # | 检查项 |
|---|---|
| 1 | 联系方式一致 |
| 2 | 项目成员交叉 |

- 联系方式一致：电话、邮箱、统一社会信用代码、银行账号跨家重复即列入
- 项目成员交叉：项目经理、技术负责人等关键人名跨家重复即列入
- 输出前自动脱敏（如 138****00），线索可被第三方用同一份输入复算出来

## 这个免费版不包含

以下检查项**不在本版本范围内**，调用时也不会执行：

- 文本异常一致
- 报价规律性差异
- 文件相互混装
- 同一处错漏
- 保证金同源
- 格式指纹一致

## 怎么调用

### 方式一：命令行脚本（最省事）

```bash
node scripts/run.mjs --sample
node scripts/run.mjs --input my-input.json
node scripts/run.mjs --input my-input.json --json
```

### 方式二：直接引用引擎（接进自己的流程）

脚本本身不做计算，真正的检查在同目录的 `scripts/engine/collusion-screening.js`（纯 Node 标准库，CommonJS），可以直接引用：

```js
const engine = require('./scripts/engine/collusion-screening.js');
const outcome = engine.run(payload);
// outcome.status === 'success'            → outcome.result 就是结果
// outcome.status === 'insufficient_input' → outcome.missing 列出缺什么（此时不出结论）
```

所有检查都在**本机**完成：核对过程不外发材料、不需要任何凭证。

## 入参

给一个 bidders 数组，每家一份投标文件文本。

```json
{
  "bidders": [
    {
      "name": "河南甲建设有限公司",
      "text": "项目经理：张三 联系电话：13800138000 我方承诺按招标文件要求组织施工"
    },
    {
      "name": "河南乙工程有限公司",
      "text": "项目经理：张三 联系电话：13800138000 我方完全响应招标文件要求"
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

- 文本异常一致
- 报价规律性差异
- 文件相互混装
- 同一处错漏
- 保证金同源
- 格式指纹一致

同名工具的**完整档**是另一个独立商品（条款与条件以它自己的商品页为准）；两档的差别**就是上面这些，没有别的**。

## 边界与免责

只输出客观线索，**是否构成串通投标须由评标委员会或监管部门依法认定**，本工具不做定性。

本技能的所有结论都可由第三方用同一份输入复算出来。
