---
slug: depreciation-check-free
displayName: 固定资产折旧核对（免费版）
version: 1.0.51
summary: 固定资产台账逐项核对，每条结论都带原文行号，不需要付款，也不需要注册。
tags: [固定资产折旧核对,固定资产台账,核对,对账,免费]
license: Proprietary
name: depreciation-check-free
display_name: 固定资产折旧核对（免费版）
display_name_en: Fixed Asset Depreciation Check (Free)
description: 固定资产台账逐项核对（逐行算术、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 固定资产台账核对、固定资产台账对不上。
description_zh: 固定资产台账逐项核对（逐行算术、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 固定资产台账核对、固定资产台账对不上。
description_en: A free deterministic check for 固定资产台账. Every finding cites the source line. No payment, no registration, no API key, no network.
category: business-ops
author: WorkBuddy 开放平台开发者
allowed-tools: Read, Bash
---

# 固定资产折旧核对（免费）

> **完全本地运行**：引擎已经打包在本技能里（`engine/` 目录）。
> 核对过程不需要联网、不需要 API Key、**没有调用次数上限**。

## 什么时候用

**谁会在什么时候用**：财务、出纳、仓管等岗位在**每月结账/发薪/对账/盘点**这类固定节点上，必须把这张表核一遍才能往下走。

**这张表会逐项核对什么**：逐项月折旧额复核（(原值 × (1 − 残值率)) ÷ 使用年限 ÷ 12）；逐项累计折旧复核（月折旧额 × 已提月数）；逐项净值复核（原值 − 累计折旧）。

每条结论都带**原文行号与出处**，可被第三方用同一口径复算；
材料不足时**不给结论**，会明确列出还缺什么，不会输出「未发现问题」。

## 这个免费版查什么

（检查项由引擎的 `CHECKS_*` 导出，跑 `--sample` 会打印实际执行了哪些。）

## 怎么用

```bash
node scripts/run.mjs --sample                 # 先看样例
node scripts/run.mjs --input 你的材料.json     # 跑自己的材料
```

## 需要完整档时（可选）

本免费版是**完整可用的核心产出**，本版本**不包含**下面这些项：

- 超提检测（已提月数 > 使用年限 × 12）
- 累计折旧超过「原值 − 残值」上限检测
- 停提异常（已提月数 > 0 但本月折旧为 0）
- 残值率区间校验（默认 0%~10%）

同名工具的**完整档**是另一个独立商品（条款与条件以它自己的商品页为准）；两档的差别**就是上面这些，没有别的**。

## 边界（请务必知道）

本工具**不做**引擎 `CHECKS_OUT_OF_SCOPE` 里列的那些判断；
材料不足时**不给结论**，也不会输出「未发现问题」。
