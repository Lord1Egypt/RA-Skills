# 🎯 bid-collection

<<<<<<< HEAD
**招投标商机采集 Skill for Claude Code**

7×24自动监控全网招投标公开信息，基于公司业务赛道智能筛选高价值商机线索，实现招投标项目早发现、早跟进、早布局。

## 安装

```bash
# 通过 npm 安装
npm install -g bid-collection
```

然后在 Claude Code 中使用 `/bid-collection` 命令。

## 使用方式

| 命令 | 功能 |
|------|------|
| `/bid-collection scan <关键词>` | 实时扫描招投标商机 |
| `/bid-collection monitor` | 启动定时监控 |
| `/bid-collection report` | 生成汇总报告 |
| `/bid-collection list-sources` | 查看监控渠道 |
| `/bid-collection add-source <url>` | 添加监控源 |

## 采集范围

- 政府公共资源交易平台（中国政府采购网、各省交易中心）
- 国企采购平台（中国移动、中国联通、中国电信等）
- 行业招投标网站（AI/大模型、数字化、IT服务等）
- 第三方招投标信息聚合平台
- 自定义监控关键词与行业场景

## 核心价值

- 🌐 **全域覆盖**：政府平台、国企采购、行业网站一站聚合
- ⏰ **实时同步**：招标预告→正式招标→变更→中标，全周期跟踪
- 🧠 **智能匹配**：基于业务赛道自动筛选高适配商机
- 📊 **标准展示**：项目名称、采购方、预算、时间、需求、联系方式一键掌握
=======
**Tender & Procurement Lead Collection Skill for Claude Code**

24/7 automated monitoring of public tender and procurement notices across government platforms, SOE procurement systems, industry-specific sites, and third-party aggregators. Intelligently filters high-value leads matching your business tracks for **early discovery, early follow-up, and early positioning**.

[![npm version](https://img.shields.io/npm/v/bid-collection.svg)](https://www.npmjs.com/package/bid-collection)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-Cryptocxf%2Fbid--collection-blue)](https://github.com/Cryptocxf/bid-collection)

## Installation

```bash
# Install via npm
npm install -g bid-collection
```

Then use `/bid-collection` in Claude Code.

## Usage

| Command | Function |
|---------|----------|
| `/bid-collection scan <keywords>` | Real-time scan for tender/procurement leads |
| `/bid-collection monitor` | Start scheduled background monitoring |
| `/bid-collection report` | Generate summary report |
| `/bid-collection list-sources` | View monitored channels |
| `/bid-collection add-source <url>` | Add custom monitoring source |

## Collection Scope

- **Government Platforms**: China Government Procurement (ccgp.gov.cn), provincial/city trading centers, China Tendering Public Service Platform
- **SOE Procurement**: China Mobile, China Unicom, China Telecom, State Grid, CNPC, China Railway, and more
- **Industry-specific Sites**: AI/LLM, digital transformation, IT services, computing power, smart applications
- **Third-party Aggregators**: Qianlima, Bidcenter, Jianyu360, and others
- **Custom Keywords**: Fully configurable monitoring keywords and industry scenarios

## Core Value

- 🌐 **Full Coverage**: Government, SOE, industry platforms in one place
- ⏰ **Real-time Sync**: Pre-tender → Open tender → Amendment → Award, full lifecycle tracking
- 🧠 **Smart Matching**: Auto-match to 10 business tracks with priority scoring
- 📊 **Standardized Display**: Project name, buyer, budget, deadline, requirements, contacts at a glance

## Features

### 10 Business Tracks
AI Technical Services, Large Language Models, System Development, Computing Power & Model Services, Digital Transformation, Information Security, Cloud Services, Smart Applications, AI Vision/Content, and dedicated SuYan (Suzhou Research) procurement coverage.

### Priority Scoring Algorithm
```
Score = Track Weight × Budget Factor × Timeliness Factor × Buyer Factor
```

### Auto-filtering
Irrelevant categories (office supplies, construction, property management, vehicles, etc.) are automatically excluded.

## CLI Flags

| Flag | Description |
|------|-------------|
| `--days=N` | Search window (default: 3 days) |
| `--budget-min=N` | Minimum budget in CNY |
| `--budget-max=N` | Maximum budget in CNY |
| `--track=core` | Core tracks only |
| `--priority=urgent` | Urgent priority only |
| `--output=detail` | Detailed output with summaries |

## Links

- **GitHub**: [https://github.com/Cryptocxf/bid-collection](https://github.com/Cryptocxf/bid-collection)
- **npm**: [https://www.npmjs.com/package/bid-collection](https://www.npmjs.com/package/bid-collection)
- **Issues**: [https://github.com/Cryptocxf/bid-collection/issues](https://github.com/Cryptocxf/bid-collection/issues)
>>>>>>> 5210fda (Initial release: bid-collection v1.0.0 — Tender & Procurement Lead Collection Skill for Claude Code)

## License

MIT