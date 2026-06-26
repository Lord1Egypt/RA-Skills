---
name: biz-doc-pro
description: "商务文档三件套：方案书+发票+合同一条龙。融合 Proposal + Invoice + Contract 三大技能优点，一站式生成专业商务文档。适合自由职业者、小企业主、创业者快速出方案、发发票、签合同。"
slug: biz-doc-pro
version: "1.0.0"
author: "智美人团队"
tags:
  - business
  - proposal
  - invoice
  - contract
  - document
  - freelance
  - small business
---

# BizDoc Pro - 商务文档大师

融合了 Proposal（方案书）、Invoice（发票）、Contract（合同）三大技能的优点，提供一体化商务文档解决方案。

## 为什么用 BizDoc Pro？

- **三大合一**：一个技能搞定方案书、发票、合同，不用切换
- **数据互通**：方案书的客户信息自动继承到发票和合同
- **专业模板**：内置10+行业模板（IT、设计、咨询、电商等）
- **一键导出**：生成Markdown可转PDF/Word

## 能力

### 1. 方案书生成 (Proposal)
- 客户需求采集 → 方案架构 → 报价表 → 时间线
- 从 `contract` 继承多轮协商能力
- 从 `proposal` 继承专业排版

### 2. 发票生成 (Invoice)
- 自动编号、税种计算、支付追踪
- 从 `invoice` 继承专业模板
- 继承 `contract` 的版本控制

### 3. 合同起草 (Contract)
- 条款生成、风险分析、版本管理
- 从 `contract` 继承全部合同能力
- 继承 `proposal` 的需求采集流程

## 存储结构

```
~/biz-docs/
├── clients/              # 客户信息（共享）
│   └── {client-name}/
│       ├── profile.md
│       └── history.md
├── proposals/            # 方案书
│   └── {project-name}/
│       ├── current.md
│       └── versions/
├── invoices/             # 发票
│   └── {client-name}/
│       ├── current.md
│       └── history.md
└── contracts/            # 合同
    └── {contract-name}/
        ├── current.md
        └── versions/
```

## 使用方式

```
biz-doc-pro> 新方案书
  → 输入客户名称、项目范围、预算
  → 自动生成方案书+报价

biz-doc-pro> 开发票 [客户名]
  → 自动填入客户信息
  → 计算税额，生成发票

biz-doc-pro> 起草合同 [客户名] [项目名]
  → 继承方案书内容
  → 生成专业合同条款
```

## 已有技能融合点

| 源技能 | 融合点 |
|--------|--------|
| proposal | 需求采集流程、方案排版 |
| contract | 条款生成、版本控制、风险分析 |
| invoice | 发票模板、税种计算、支付追踪 |
