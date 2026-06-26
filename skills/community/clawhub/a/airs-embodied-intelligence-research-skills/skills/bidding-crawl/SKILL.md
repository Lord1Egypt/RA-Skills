---
name: airs-bidding-crawl
description: >
  采集具身智能机器人企业天眼查中标公告的 AIRS 研究 Skill。用于读取 data/company_list.csv，批量抓取企业招投标和中标公告，保存公告列表、详情链接和原始 Markdown，生成 data/bidding_records.csv 与 data/raw_content/*.md。用户需要采集季度公开证据、补抓 raw_content、断点续跑 crawl 或做企业增量采集时使用。
  Keywords: AIRS, 具身智能, embodied intelligence, bidding, tender, 招投标, 中标公告, 天眼查, tianyancha, robot company, public evidence, data collection.
tags: ["airs", "AIRS", "具身智能", "embodied-intelligence", "robotics", "bidding", "tender", "tianyancha", "中标公告", "招投标", "evidence-collection", "data-crawl"]
---

# 天眼查中标公告采集

## 目标

从已确认主体口径的企业列表中，批量采集天眼查中标公告，并保留后续案例提取所需的原文证据。

## 输入

- `data/company_list.csv`
- `config/settings.json`
- Chrome 远程调试端口 `9222`
- 已登录天眼查的浏览器会话

## 输出

- `data/bidding_records.csv`
- `data/raw_content/*.md`
- `data/crawl_progress.json`

## 执行流程

1. 确认 `data/company_list.csv` 已由企业全称确认技能生成。
2. 确认 Chrome 远程调试和天眼查登录状态。
3. 全量采集运行：

```bash
npm run crawl
```

4. 增量采集运行：

```bash
npm run crawl:incremental
```

5. 只补详情原文运行：

```bash
npm run crawl:rawcontent
```

6. 采集结束后，抽查 `bidding_records.csv` 与 `data/raw_content/` 是否一一对应。

## 业务规则

- 采集年份、金额阈值以 `config/settings.json` 为准。
- Crawl 去重键为 `(标题标准化, 日期)`。
- `raw_content` 是后续案例提取的原文依据，缺失时必须补抓。
- 遇到验证码时暂停等待人工处理，不要跳过大量企业。

## 质量检查

- `data/crawl_progress.json` 应显示企业处理进度清晰可续跑。
- 随机打开 5 条 `data/raw_content/*.md`，确认不是登录页、验证码页或空页面。
- 关注企业明显不相关、发布时间越界、重复公告过多等异常。

## 失败处理

- Chrome 连接失败：检查远程调试端口。
- 详情页抓取失败：优先重跑 `npm run crawl:rawcontent`。
- 页面结构变化：优先检查 `src/modules/biddingDownload.js`。
