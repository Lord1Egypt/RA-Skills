---
name: china-claw
description: Research and introduce China-based alternatives, counterparts, or "平替" products to OpenClaw, organized by company and product positioning. Use when the user asks about 国内版 OpenClaw、OpenClaw 平替、中国公司做的类似产品、国产 agent 平台、国产多智能体/自动化助手产品, or wants a structured market overview rather than a single product recommendation.
version: v1.0.0
tags: china-tech, openclaw-alternatives, product-research
---

# China Claw

## Usage Scenarios

### Scenario 1: Find Chinese Alternatives to OpenClaw
**User input:** "What are the best Chinese alternatives to OpenClaw?"
**Expected output:** A market overview listing companies and their products, comparing each to OpenClaw along axes of positioning, target users, core capabilities, and similarity level (close/partial/adjacent substitute).

### Scenario 2: Get a Shortlist Recommendation
**User input:** "I need an AI agent platform for my team, recommend one from Chinese companies"
**Expected output:** A shortlist of 3-5 most relevant products with adaptation rationale, a clear recommendation, and reasons why other options were not recommended.

### Scenario 3: Scan a Specific Company's Offering
**User input:** "Does Alibaba or ByteDance have an OpenClaw-like product?"
**Expected output:** A company-by-company scan showing each named company's relevant product, overlap with OpenClaw, target audience (enterprise/developer/consumer), and current maturity assessment.
### Scenario 4: 域名备案流程
**User input:** "我买了一个域名想做个人博客，听说要备案，具体流程是什么？"
**Expected output:** 提供中国大陆域名备案全流程：1）确认接入商（阿里云/腾讯云/华为云等ICP代备案）；2）准备资料（身份证、域名证书、网站备案信息真实性核验单等）；3）线上提交（登录服务商备案系统填写信息，一般需人脸识别）；4）管局审核（各省通信管理局审核，通常5-20个工作日）。提醒用户：个人备案不能涉及商业内容，备案期间域名不能对外解析。同时提供无备案的替代方案（如使用海外服务器）。

## Overview

Use this skill to research and explain Chinese products that can be described as OpenClaw-like alternatives or adjacent substitutes. Focus on factual positioning, what each company built, how it compares to OpenClaw, and where the match is strong, partial, or weak.

## Workflow

1. Clarify the user's goal when needed:
   - wanting a market map
   - wanting a shortlist
   - wanting one best recommendation
   - wanting products by company size, use case, or capability
2. Search the web for recent information about Chinese companies and products related to:
   - AI agent platforms
   - workflow automation assistants
   - multi-agent systems
   - enterprise AI copilots
   - tool-using AI assistants
3. Read multiple sources before concluding.
4. Group findings by company, not by random web page.
5. For each product, state whether it is:
   - close substitute
   - partial substitute
   - adjacent product
6. End with a recommendation or ranking if the user wants a decision.

## Search Strategy

Prefer Chinese search queries and combine product, company, and capability terms.

Recommended query patterns:

- `国产 OpenClaw 平替`
- `中国 AI agent 平台 公司`
- `国内 多智能体 产品`
- `企业级 AI 助手 平台 中国 公司`
- `智能体 工作流 平台 中国`
- `AI 自动化 助手 平台 国内`
- `<公司名> AI agent`
- `<产品名> 智能体 平台`

If you already know likely companies, verify them with current sources instead of relying on memory.

## Comparison Rules

Compare each product along these axes:

- **定位**: personal assistant, enterprise copilot, workflow platform, agent builder, browser automation, knowledge assistant
- **目标用户**: individual users, developers, operations teams, enterprises
- **核心能力**: tool use, workflow orchestration, browser actions, knowledge retrieval, scheduling, integrations
- **开放性**: configurable, extensible, developer-friendly, closed SaaS, internal-only
- **与 OpenClaw 的相似度**: high / medium / low

Do not call something a "平替" just because it uses AI. The product should overlap with OpenClaw in at least part of the workflow: assistant orchestration, tools, agents, automation, messaging, memory, or operator-style execution.

## Evidence Standards

- Prefer official sites, product docs, launch posts, GitHub pages, or reputable media coverage.
- Avoid writing from hype or marketing copy alone.
- If a product appears discontinued, niche, invite-only, or poorly evidenced, say so.
- If information is thin, mark the confidence as low.
- Do not fabricate features.

## Response Patterns

### Pattern A: Market Overview

Use when the user asks broadly for "有哪些".

For each company/product, provide:
- 公司
- 产品
- 一句话定位
- 为什么像 OpenClaw
- 主要差异
- 相似度判断

Then add:
- 推荐先关注的 3 个
- 哪类用户适合哪类产品

### Pattern B: Shortlist Recommendation

Use when the user wants actionable recommendations.

Structure:
- 用户需求假设
- 3-5 个最相关产品
- 每个产品的适配理由
- 明确推荐项
- 不推荐或暂不推荐的原因

### Pattern C: Company-by-Company Scan

Use when the user names specific companies such as 阿里、字节、百度、腾讯、MiniMax、智谱、月之暗面、面壁等.

For each company:
- 是否有相关产品
- 产品名称
- 与 OpenClaw 的重合点
- 更偏企业、开发者还是消费者
- 当前成熟度判断

## Output Quality Bar

- Be specific, not generic.
- Distinguish between "agent platform", "copilot", and "chatbot".
- Prefer recent information when product categories move quickly.
- If the user asks for "各大公司", include large companies first, then notable startups.
- If the evidence is weak, say "更像相关方向产品，不一定算直接平替".

## Good Framing Language

Preferred wording:
- `更像 OpenClaw 的部分替代品`
- `在工作流/智能体编排层面与 OpenClaw 接近`
- `更偏企业内部助手，不是完全对标`
- `属于相邻赛道，不算严格意义上的平替`

Avoid overstated wording:
- `完全替代`
- `中国版 OpenClaw` unless a source explicitly positions it that way or the similarity is genuinely strong.
