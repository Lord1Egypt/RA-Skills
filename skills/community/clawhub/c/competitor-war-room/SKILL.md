---
name: Competitor War Room
description: Real-time competitive intelligence dashboard. Monitors competitor moves, pricing changes, feature launches, hiring signals, and market positioning across 20+ sectors.
author: ClawHub
version: 1.0.0
tags: ["business", "competitive-intelligence", "strategy", "market-research", "startup", "enterprise"]
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: ccce6a035782beb383eb6aaf17a72a9b_competitor_war_room_001
    ReservedCode1: Dv5ePA7ZkJInZI0tdkqEjWjIhMrkQq52HD09yRVO5mM=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: ccce6a035782beb383eb6aaf17a72a9b_competitor_war_room_001
    ReservedCode2: Dv5ePA7ZkJInZI0tdkqEjWjIhMrkQq52HD09yRVO5mM=
---



# 竞品战情室 (Competitor War Room)

## 概述

全网首创的实时竞品情报监控系统，覆盖产品动态、定价变化、招聘动向、融资新闻、社交媒体声量五大维度，内置 SWOT 矩阵与波特五力模型，输出可执行的竞争反制策略与高管预警简报。

## 适用场景

1. SaaS 产品竞品功能与定价实时监控
2. 竞品融资/并购/裁员等重大事件预警
3. 多维 SWOT 对比矩阵自动生成
4. 竞品社交媒体声量与情绪趋势追踪
5. 管理层竞品周报/月报自动编写
6. 新进入者威胁评估与市场壁垒分析

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| company | string | 是 | 具体值由技能数据底座智能匹配 |
| sector | string | 是 | 具体值由技能数据底座智能匹配 |
| competitors | string | 是 | 具体值由技能数据底座智能匹配 |
| region | string | 是 | 具体值由技能数据底座智能匹配 |

## 评分体系

| 分数 | 等级 | 建议 |
|------|------|------|
| 90-100 | ⭐⭐⭐⭐⭐ 极佳 | 强烈推荐执行 |
| 75-89 | ⭐⭐⭐⭐ 良好 | 具备较高置信度 |
| 60-74 | ⭐⭐⭐ 一般 | 可参考，需交叉验证 |
| 40-59 | ⭐⭐ 较差 | 信号较弱，谨慎采用 |
| 0-39 | ⭐ 不可用 | 数据不足或噪音过大 |

## 支付协议（AI收）

本技能采用支付宝 AI 收 HTTP 402 协议，按次计费。

| 项目 | 值 |
|------|-----|
| 单价 | ¥0.50 / 次 |
| 支付协议 | `alipay_` 短链协议 |
| 网关地址 | `http://8.145.54.67:3000` |
| 技能路径 | `/skill/competitor-war-room` |
| 支付确认路径 | `/pay-confirm` |

### 支付流程

```
1. 客户端发起分析请求  POST /skill/competitor-war-room
2. 服务端返回 402 Payment Required
   Header: Payment-Needed: <Base64支付信息>
   Body: { step: "payment_required", short_link: "alipay_XXX", pay_url: "..." }
3. 用户完成支付宝支付
4. 客户端携带支付凭证回传  x-payment-credential
5. 服务端验证通过 → 执行分析 → 返回结果
```

### HTTP 请求头规范

| 头名称 | 说明 |
|--------|------|
| `Payment-Needed` | 服务端返回：Base64 编码的支付引导信息 |
| `x-payment-credential` | 客户端回传：支付完成后的 alipay_ 凭证字符串 |

## 数据底座

所有数据存储于 `references/competitor-war-room.json`，包含完整的分析模型参数、行业数据库、策略模板与案例库。

## 使用示例

### 请求

```bash
curl -X POST http://8.145.54.67:3000/skill/competitor-war-room \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

### 响应（支付后）

```json
{
  "status": "completed",
  "skill": "competitor-war-room",
  "data": { ... },
  "payment": { "status": "paid", "amount": "0.50" }
}
```

## 许可

MIT License
*（内容由AI生成，仅供参考）*


## 监控维度

### 1. 产品动态
实时追踪竞品功能发布、UI/UX 改版、API 变更、定价页面更新、文档修改。核心产品页面变更即触发告警。

### 2. 定价策略
监控竞品价格计划调整、每席位/每用量变动、免费层修改、企业定制价格、促销活动。支持单价比对与 TCO 计算器。

### 3. 招聘信号
追踪竞品各部门编制变化、关键高管入职/离职、研发 vs 销售比例变化、远程办公政策调整、实习生/校招规模。

### 4. 融资与并购
监控竞品融资轮次（金额/领投方/估值）、收购目标与理由、IPO/SPAC 信号、二级市场股票交易、裁员与降轮。

### 5. 社交媒体声量
追踪竞品 X/Twitter 关注增长、LinkedIn 员工数、Glassdoor 评分趋势、G2/Capterra 评论速度、Reddit 提及情感。

## 行业覆盖

| 行业 | 市场规模(2026E) | 增速 | 竞争焦点 |
|------|---------------|------|---------|
| AI SaaS | $91.6B | 32% | 企业合同/API定价/模型性能/安全合规 |
| 金融科技 | $310B | 22% | 跨境支付/BNPL监管/嵌入式金融/CBDC |
| 电商 | $6.8T | 14% | 社交电商/当日达/AI推荐/可持续包装 |
| 网络安全 | $320B | 18% | 零信任/AI检测/云安全/供应链安全 |
| 云计算 | $620B | 25% | GPU供给/多云编排/边缘计算/绿色云 |

## 竞争分析框架

| 框架 | 适用场景 | 核心维度 |
|------|---------|---------|
| SWOT 矩阵 | 单竞品深度分析 | 优势/劣势/机会/威胁 |
| 波特五力 | 行业吸引力评估 | 供应商力/买方力/竞争强度/新进入者/替代品 |
| 蓝海战略 | 差异化定位 | 消除/减少/提升/创造 |
| BCG 矩阵 | 产品组合管理 | 明星/金牛/问题/瘦狗 |

## 公开情报源

| 来源 | 数据类型 | 更新频率 | 可靠性 |
|------|---------|---------|--------|
| Crunchbase | 融资/并购/高管变动 | 每日 | 高 |
| LinkedIn | 编制增长/部门扩张/招聘 | 每周 | 高 |
| Glassdoor | 员工情绪/薪资/面试体验 | 每月 | 中 |
| G2/Capterra | 客户满意度/功能对比 | 每月 | 中高 |
| SimilarWeb | 网站流量/推荐来源/地域 | 每月 | 中高 |
| BuiltWith | 技术栈/工具/平台迁移 | 每月 | 高 |
| SEC Edgar | 财务文件/S-1/年报 | 每季/年 | 极高 |
| USPTO/WIPO | 专利申请/技术方向/IP战略 | 每月 | 高 |

## 数据底座

`competitor-war-room.json` 包含：六大行业玩家库、五大监控维度与告警规则、四大反制策略（产品/价格/人才/营销）、四大竞争分析框架、三大历史竞争案例（OpenAI vs Google、TikTok Shop vs Amazon、Cloudflare vs AWS）、竞品人格原型、八级事件严重度矩阵、战斗卡模板、十项 OSINT 情报源、健康度指标。



## 反制策略库

| 攻击类型 | 推荐动作 | 响应时限 |
|---------|---------|---------|
| 竞品推出直接竞争产品 | CEO通知，反制方案24h内 | < 4小时 |
| 竞品融资 $500M+ | 董事会通报，竞争定位重审 | < 24小时 |
| 竞品挖角高管 | 法务审查（竞业），知识转移评估 | < 12小时 |
| 竞品降价 30%+ | 定价委员会评审，客户留存联络 | < 48小时 |
| 竞品负面舆情 | 识别挖人/定位机会 | < 1周 |
| 竞品申请核心专利 | 知识产权律师审查，先有技术检索 | < 1周 |

## 竞品人格原型

| 原型 | 特征 | 反制策略 | 典型示例 |
|------|------|---------|---------|
| 攻击型颠覆者 | 快速迭代/低价/负面营销/挖人 | 忽略噪音，专注企业信任与SLA | OpenAI（2022-2025） |
| 迟缓在位者 | 保护现有收入/合规重流程/收购优先 | 在其无法快速转型的领域创新 | Oracle/SAP/IBM |
| 生态建设者 | 平台打法/开发者优先/开源/市场模型 | 打造更好开发者体验和集成 | Stripe/Shopify/AWS |
| 潜伏捕食者 | 静默R&D/专利积累/关键挖人/充分准备后发布 | 挖他们的人，监控专利文件 | Apple/Amazon发布前 |

## 七大事件严重度矩阵

| 触发条件 | 严重度 | 响应时间 | 行动 |
|---------|--------|---------|------|
| 竞品推出直接竞争核心产品功能 | CRITICAL | <4h | 作战室召集/CEO通知/24h内反制方案 |
| 竞品融资$500M+/$10B+估值 | HIGH | <24h | 董事会更新/竞争定位重审 |
| 竞品从你公司挖走C-suite | HIGH | <12h | 法务审查/知识转移评估 |
| 竞品降价30%+ | MEDIUM | <48h | 定价委员会审查/客户留存联络 |
| 竞品Glassdoor/Trustpilot负面趋势 | INFO | <1周 | 识别挖人/定位机会 |
| 竞品在核心领域申请专利 | MEDIUM | <1周 | IP律师审查/先有技术检索 |
| 行业分析师下调竞品评级 | INFO | <48h | 销售赋能：与潜在客户分享 |

## 历史案例

### OpenAI vs Google (2022-2026)
ChatGPT发布 → Google内部红色警报 → 加速Gemini开发 → Bard发布翻车（股价-8%）→ Gemini Ultra vs GPT-4 Turbo价格战 → Agentic AI成为新战场。核心教训：快速跟随策略在有分发优势时有效。

### TikTok Shop vs Amazon (2023-2026)
TikTok Shop美国上线 → Amazon Inspire失败 → TikTok Shop月度GMV突破$1B → Amazon Haul反击。核心教训：社交电商威胁需社交原生方案，而非附加功能。

### Cloudflare vs AWS (2021-2026)
R2存储（无出口费）→ S3局部降价 → Workers AI边缘推理 → AWS Lambda@Edge升级。核心教训：攻击在位者的商业模式弱点，而非功能对等。

## 公开情报源

| 来源 | 数据类型 | 更新频率 | 可靠性 | 费用 |
|------|---------|---------|--------|------|
| Crunchbase | 融资/并购/高管变动 | 每日 | 高 | 免费层可用 |
| LinkedIn | 编制增长/部门扩张/招聘 | 每周 | 高 | Sales Navigator $99/月 |
| Glassdoor | 员工情绪/薪资/面试体验 | 每月 | 中 | 免费（有限） |
| G2/Capterra | 客户满意度/功能对比 | 每月 | 中高 | 免费层可用 |
| SimilarWeb | 网站流量/推荐来源/地域 | 每月 | 中高 | $199/月起 |
| BuiltWith | 技术栈/工具/平台迁移 | 每月 | 高 | $295/月起 |
| SEC Edgar/Companies House | 财务文件/S-1/年报 | 每季/年 | 极高 | 免费 |
| USPTO/WIPO/EPO | 专利申请/技术方向/IP战略 | 每月 | 高 | 免费 |
