---
name: cruise-product-list
title: cruise-product-list
description: 根据条件筛选邮轮产品列表，支持多种过滤条件，快速获取您想要的邮轮产品。
kind: MCP
version: 0.1.0
published_with: cruiseskillbridge
---

# cruise-product-list

> 根据条件筛选邮轮产品列表，支持多种过滤条件，快速获取您想要的邮轮产品。

这是一个 **MCP** 技能，通过 [CruiseSkillBridge](https://cruiseskillbridge.com) 一键发布。

## 能力

- 描述这个技能能做什么（请替换为你的真实内容）。
- 列出关键输入与输出。
- 说明适用场景。

## 用法

当需要提交分析请求时，向以下 API 发送 **POST** 请求（JSON body）：

```
https://httpbin.org/post
```

示例 body：

```json
{ "input": "...", "skill": "cruise-product-list" }
```

> 发布到 CruiseSkillBridge 后，上述 URL 会自动替换为网关地址，调用将计入控制台统计。

## 关于

由 [CruiseSkillBridge](https://cruiseskillbridge.com) 发布 —— 全球唯一邮轮领域技能 分发 · 发布 · 洞察：
一键发布、分发洞察、网关调用统计。

## 已发布的 MCP Tools

以下 Tools 已纳入 CruiseSkillBridge 发布与统计：

- **product_list** — 按条件筛选邮轮产品列表。支持品牌、出发城市、价格区间、目的地、行程天数、邮轮、日期等多维度过滤。

> MCP 接入经 CruiseSkillBridge 网关转发，remotes URL 已自动替换，无需手动配置。
