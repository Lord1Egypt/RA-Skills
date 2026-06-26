---
name: airs-thirdparty-order-verify
description: >
  核查第三方具身智能机器人订单 Excel 的 AIRS 研究 Skill。用于导入外部订单表，按项目名称、中标单位、采购单位、金额和年份在天眼查搜索匹配，输出 verify_match_report.csv、verify_bidding_records.csv 和通过记录原文。用户需要验证第三方订单数据、补充可进入案例提取的公告证据、定位未匹配或低分匹配记录时使用。
  Keywords: AIRS, 具身智能, embodied intelligence, third-party order verification, order verify, Excel, 订单核查, 招投标匹配, 证据匹配, 天眼查, tianyancha, fuzzy match.
tags: ["airs", "AIRS", "具身智能", "embodied-intelligence", "order-verification", "third-party-data", "Excel", "fuzzy-match", "evidence-matching", "订单核查", "tianyancha"]
---

# 第三方订单核查

## 目标

把第三方 Excel 中的订单线索，与天眼查公开招投标公告做证据匹配，筛出可进入后续 Extract 的通过记录。

## 输入

- 默认：`2025年全国具身智能机器人企业订单_数据表.xlsx`
- 或用户指定的第三方 Excel 文件
- Chrome 远程调试端口 `9222`
- 已登录天眼查的浏览器会话

## 输出

- `data/verify_match_report.csv`
- `data/verify_bidding_records.csv`
- `data/verify_progress.json`
- 通过记录对应的 `data/raw_content/*.md`

## 执行流程

默认文件：

```bash
npm run verify
```

指定文件：

```bash
npm run verify -- path/to/other.xlsx
```

核查结束后：

1. 查看 `data/verify_match_report.csv` 的通过率、匹配得分和未通过原因。
2. 抽查通过记录的标题、采购单位、中标单位、金额和发布日期。
3. 将确认通过的 `data/verify_bidding_records.csv` 追加到 `data/bidding_records.csv`。
4. 后续继续运行案例提取和标准入库技能。

## 匹配规则

- 强匹配因素：项目标题、采购单位、中标单位、金额、发布日期。
- 对目标年份订单，天眼查发布日期应符合目标年份。
- 低分匹配不应直接入库，应进入人工确认。
- 项目名过短时，优先组合中标单位、采购单位、金额和年份搜索。

## 质量检查

- 重点看低分但标题相近的记录。
- 排查发布日期非目标年份、金额单位异常、中标单位字段噪声等问题。
- 通过记录必须有可追溯链接和原文文件。

## 失败处理

- 搜索无结果：尝试缩短项目名或改用主体组合搜索。
- 详情页解析异常：查看原文 Markdown，必要时人工确认后再追加。
- 断点续跑：保留 `data/verify_progress.json`，直接重跑命令。
