---
name: airs-company-identity
description: >
  确认具身智能机器人企业主体口径的 AIRS 研究 Skill。用于从企业数据库 Markdown 中解析企业简称，连接天眼查搜索并确认工商全称、简称、别名和主体匹配状态，生成 data/company_list.csv。用户需要新增企业、校准企业名称、统一企业简称、准备后续招投标采集或案例入库主体映射时使用。
  Keywords: AIRS, 具身智能, embodied intelligence, robot company, company identity, 企业全称, 企业简称, 工商主体, 天眼查, tianyancha, entity resolution, company mapping.
tags: ["airs", "AIRS", "具身智能", "embodied-intelligence", "robotics", "company-identity", "entity-resolution", "company-mapping", "企业主体", "企业全称", "tianyancha"]
---

# 企业全称确认

## 目标

将 `具身智能中游企业数据库.md` 中的企业简称和候选名称，确认成后续所有技能共用的企业主体口径。`data/company_list.csv` 是后续公告采集、字段提取、主体简称映射的权威来源。

## 输入

- `具身智能中游企业数据库.md`
- `config/settings.json`
- Chrome 远程调试端口 `9222`
- 已登录天眼查的浏览器会话

## 输出

- `data/company_list.csv`

## 执行流程

1. 确认 Chrome 已用远程调试模式启动，并已登录天眼查。
2. 确认 `config/settings.json` 中的浏览器端口与实际端口一致。
3. 运行：

```bash
npm run search
```

4. 检查 `data/company_list.csv`，重点关注企业简称、搜索确认全称、匹配状态和失败原因。
5. 对未确认企业，优先补充别名或人工确认工商全称，再重跑本技能。

## 业务规则

- 企业简称以 `具身智能中游企业数据库.md` 为准。
- 工商全称以天眼查搜索结果为准。
- 同一企业存在多个法人主体时，优先选择与机器人整机、具身智能业务最相关的主体。
- 不确定时标记待人工确认，不要编造工商全称。
- 后续案例详情和案例简介中的企业名称，应尽量统一回填到这里确认过的简称。

## 质量检查

- `company_list.csv` 应覆盖输入名单中的国内目标企业。
- 未找到企业应有清晰原因，而不是静默缺失。
- 随机抽查高价值企业，确认工商全称与简称对应关系无误。

## 失败处理

- 遇到验证码：等待用户在 Chrome 中处理后继续。
- Chrome 连接失败：检查远程调试端口和 `config/settings.json`。
- 搜索结果混乱：先人工补充别名或缩小候选主体范围，再重跑。
