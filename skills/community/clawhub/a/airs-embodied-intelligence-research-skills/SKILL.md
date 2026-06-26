---
name: AIRS招投标订单采集与核查
description: >
  AIRS 具身智能产业研究 Skills。面向 embodied intelligence、robotics 和机器人产业研究，将企业主体确认、天眼查招投标/中标公告采集、第三方订单核查、LLM 案例提取、标准入库表生成和案例质量复查组织为一套可复用研究流程。适用于采集公开证据、验证机器人订单、沉淀具身智能案例库和生成产业研究知识资产。
  Keywords: AIRS, 具身智能, embodied intelligence, robotics, robot industry, 天眼查, tianyancha, 招投标, bidding, 中标公告, order verification, case extraction, research skills, knowledge asset.
version: 1.0.2
author: "airs"
license: MIT-0
tags: ["airs", "AIRS", "具身智能", "embodied-intelligence", "robotics", "robot-industry", "tianyancha", "bidding", "招投标", "中标公告", "order-verification", "case-extraction", "data-quality", "research-skills", "knowledge-asset"]
metadata:
  openclaw:
    skillKey: airs-embodied-intelligence-research-skills
    homepage: https://github.com/airs-guest/airs-embodied-intelligence-research-skills
    requires:
      bins:
        - node
        - npm
      config:
        - config/settings.json
        - 具身智能中游企业数据库.md
        - 应用场景分类规则.md
---

# AIRS 具身智能产业研究 Skills

## When to Use

当用户需要围绕具身智能、机器人产业或 embodied intelligence 做公开证据采集、订单核查、案例提取和标准化入库时，使用本 skill。

典型请求：

- "确认这些具身智能企业的天眼查主体"
- "采集宇树、乐聚、智元机器人的中标公告"
- "核查第三方 Excel 里的机器人订单是否有公开招投标证据"
- "把天眼查公告提取成具身智能案例库入库表"
- "复查案例详情、场景分类和案例简介质量"

## Capability Map

本仓库是一个多模块 skill bundle，根入口负责总调度，具体能力位于 `skills/`：

| 能力 | 子 Skill | 命令 |
| --- | --- | --- |
| 企业主体确认 | `skills/company-identity/SKILL.md` | `npm run search` |
| 中标公告采集 | `skills/bidding-crawl/SKILL.md` | `npm run crawl` |
| 第三方订单核查 | `skills/thirdparty-verify/SKILL.md` | `npm run verify` |
| 招投标案例提取 | `skills/case-extract/SKILL.md` | `npm run extract` |
| 标准入库表生成 | `skills/case-ingest/SKILL.md` | `npm run ingest` |
| 案例质量复查 | `skills/case-quality-review/SKILL.md` | `npm run quality:review` |

如果用户只需要某个环节，优先读取对应子 Skill；如果用户要跑完整链路，按企业确认、公告采集、案例提取、人工复核、入库复查的顺序执行。

## Requirements

- Node.js 18+
- npm
- Chrome 浏览器
- 天眼查账号和已登录的浏览器会话
- LLM provider：在本地 `config/settings.json` 中配置 OpenAI-compatible provider，例如 Moonshot

涉及天眼查搜索、采集和核查的命令需要 Chrome 以远程调试模式启动：

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

启动后访问 `https://www.tianyancha.com` 并完成登录。

## Setup

```bash
npm install
cp config/settings.example.json config/settings.json
```

在本地 `config/settings.json` 中填写 API key。真实 API key、天眼查登录状态、抓取结果和本地数据不要提交到仓库。

## Workflow

1. 准备企业名单模板：编辑 `具身智能中游企业数据库.md`。
2. 企业主体确认：运行 `npm run search`，生成 `data/company_list.csv`。
3. 公告证据采集：运行 `npm run crawl`，生成 `data/bidding_records.csv` 与 `data/raw_content/*.md`。
4. 第三方订单核查：如有外部 Excel，运行 `npm run verify -- path/to/orders.xlsx`。
5. 案例提取：运行 `npm run extract`，生成 `data/review_sheet.csv` 和 `data/output/ingestion_output.csv`。
6. 人工复核：在 `review_sheet.csv` 中确认 `待验证` 行，将可入库记录改为 `通过`，再运行 `npm run extract` 刷新入库输入。
7. 标准入库和质量复查：运行 `npm run ingest` 或 `npm run quality:review`。

## Outputs

主要输出位于 `data/`，默认不进入发布包：

- `data/company_list.csv`
- `data/bidding_records.csv`
- `data/raw_content/*.md`
- `data/verify_match_report.csv`
- `data/verify_bidding_records.csv`
- `data/extract_results.csv`
- `data/review_sheet.csv`
- `data/output/ingestion_output.csv`
- `data/output/ingest_final.csv`
- `data/output/ingest_report.md`

## Data And Safety Notes

- 只发布示例配置和模板，不发布真实 Excel、抓取结果、日志、API key 或天眼查会话信息。
- Chrome 远程调试端口只应在可信本机环境中使用；完成采集后关闭该浏览器会话。
- 天眼查验证码或安全验证需要人工完成，不应尝试绕过平台风控。
- 发布到 ClawHub 前检查 `.clawhubignore`、`.gitignore` 和 `git status`。
