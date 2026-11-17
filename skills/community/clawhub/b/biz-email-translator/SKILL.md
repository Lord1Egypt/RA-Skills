---
name: biz-email-translator
description: "This skill should be used when the user wants an idiomatic foreign-language version of Chinese business correspondence. Trigger phrases include '商务邮件翻译', '帮我翻译成英文邮件', '这封邮件地道的英文怎么说', '报价邮件翻译', 'translate this business email', 'business email in English'. It outputs native-sounding translations with subject line options, register variants, and notes on key phrasing choices."
agent_created: true
---

# 商务邮件地道翻译

## Overview

把中文商务邮件翻译成**符合目标语言商务习惯**的地道译文，而不是字对字的直译。除了正文，还要产出主题行备选、语气版本差异、以及关键表达的选用理由，方便用户在不同关系和场景下选择。

## When to use

- 用户贴中文邮件要求翻译成外语。
- 用户说「这封邮件英文怎么说才地道」「帮我回一封外文邮件」「商务邮件翻译」。

## Workflow

1. **识别邮件类型**：询盘 / 报价 / 议价 / 催款 / 道歉 / 进度跟进 / 感谢 / 婉拒 / 投诉处理 / 会议邀约。不同类型有不同的语气范式。
2. **确认目标语言与正式度**：英语（美式 / 英式）、日语、德语等；正式度从 Very formal 到 Casual。
3. **确认关系与背景**：对方是客户 / 供应商 / 内部 / 潜在客户，过往沟通基础，是否需要保留原格式（条款、表格）。
4. **翻译并本地化**：
   - 称呼与结尾敬语按目标语言惯例
   - 中式客套（如「打扰了」「承蒙厚爱」）转译为目标语言的对等礼貌表达，不要逐字翻
   - 长句拆分，符合目标语言邮件阅读习惯
5. **处理数字与格式**：日期格式、货币符号与单位、小数点/千分位、时区、度量衡按目标市场转换并提示。
6. **给 2-3 个语气版本**。
7. **列出关键表达说明**。

## 语气对照

| 场景 | 英文倾向 |
|------|----------|
| 首次接触潜在客户 | 正式、克制，用 I would appreciate / would it be possible |
| 老客户日常沟通 | 中性偏友好，用 Hope you're well / Just checking in |
| 催款 | 礼貌但明确边界，避免指责：「Following up on invoice … due on …」 |
| 拒绝 / 负面答复 | 先缓冲再给结论，给替代方案：「Unfortunately we're unable to … However …」 |
| 道歉并补救 | 明确承认 + 补偿动作，不推诿：「My apologies for … We have …」 |

## 输出模板

```
## 邮件背景
- 类型：…  目标语言：…  正式度：…  对象关系：…

## 主题行备选
1. …（简洁）
2. …（含关键信息）
3. …（偏正式）

## 正文译文（推荐版）
Dear …,
…
Best regards,
XX

## 语气变体
- 更正式：…
- 更委婉：…

## 关键表达说明
| 中文原句 | 译文处理 | 为什么这样译 |
|----------|----------|--------------|

## 需注意的转换
- 日期 / 货币 / 单位：…（已转换，请确认）
- 待确认信息：…
```

## 关键规则

- **去中式直译**：「请知悉」不要译成 Please know，「期待您的回复」用 I look forward to hearing from you，而不是 I wait for your reply。
- **敬语成对**：Dear 与 Best regards / Sincerely / Kind regards 要匹配正式度；日语注意敬语体系的上下关系。
- **主题行必须有用**：要有具体信息（订单号、会议时间、诉求），不要只写 Hello 或 Question。
- **数字转换要提示**：金额币种（¥ / $ / €）、单位（万 vs thousand / million）、日期格式（Sep 24 vs 24 Sep）转换后提醒用户核对。
- **保留专有名词**：人名、公司名、产品型号、订单号保持原样或按官方英文名，不自创。
- **不擅自加承诺**：原文没有的交期、折扣、保证不要为了礼貌自作主张添加；不确定处列为「待确认」。
- **负面消息先缓冲**：拒绝、延期、涨价类邮件要给结构化理由，不要把负面信息藏到段落中间。

## 自检清单

- [ ] 主题行有具体信息且给了备选
- [ ] 称呼、正文、结尾敬语正式度一致
- [ ] 中式客套已做对等转译，非直译
- [ ] 数字/货币/日期已转换并标记提醒
- [ ] 提供了至少一种语气变体
- [ ] 未擅自添加原文没有的承诺
- [ ] 专有名词保持一致
