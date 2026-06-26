---
name: aky-public-opinion
description: >
  Professional-grade Chinese social media sentiment analysis report writer for government and enterprise use.
  Generates structured public opinion analysis reports covering risk assessment, communication data analysis,
  and actionable countermeasures. Supports 5 daily report types (Rapid Assessment / Special Report / Deep Research /
  Retrospective / Monthly) and 5 special event types (International Pressure / Ethnic & Ideological /
  Industrial-Economic Security / Governance Innovation / Diplomatic Sensitivity).
  Use when the user asks: "write a sentiment analysis report", "analyze this incident's public opinion risk",
  "do a sentiment assessment", "review this public sentiment event", or "monthly sentiment summary".
---

# Chinese Public Opinion & Sentiment Analysis Report Writer

## Overview

This skill generates professional-grade public opinion (sentiment) analysis reports for Chinese social media and news events. Reports are designed for government/institutional internal decision-making contexts. Style: formal, rigorous, evidence-based, combining data analysis, risk assessment, and actionable policy recommendations.

## Report Categories

### A. Daily Reports (5 types, 9 subtypes)

| Type | Purpose | Typical Length |
|------|---------|---------------|
| **Investigation & Analysis Report (调研分析报告)** | Multi-dimensional investigation: factual discovery + legal framework + socio-political-economic-cultural impact + risk assessment | 2,000-5,000 chars |
| **Rapid Assessment (快报)** | Quick assessment of breaking incidents | 800-1,500 chars |
| **Special Report (专报)** | Systematic deep dive on a specific incident | 2,000-4,000 chars |
| **Deep Research Report (研报)** | Policy-oriented research & industry analysis | 3,000-6,000 chars |
| **Retrospective Report (复盘)** | Post-mortem of major incidents | 2,000-4,000 chars |
| **Monthly Report (月报)** | Monthly summary + risk forecast | 2,500-4,000 chars |

### B. Special Event Reports (5 types)

| Type | Purpose | Typical Length |
|------|---------|---------------|
| **International/Pressure** | Foreign pressure, trade friction, geopolitics | 3,000-6,000 chars |
| **Ethnic/Religious/Ideological** | Ethnic policy, anti-China narratives, ideology | 2,500-5,000 chars |
| **Industrial-Economic Security** | Supply chain security, trade barriers, sanctions | 3,000-6,000 chars |
| **Governance Innovation/Social Phenomena** | Social governance innovation, emerging trends | 2,500-5,000 chars |
| **Diplomatic Sensitivity (JP/US etc.)** | Bilateral relations-triggered sentiment | 2,000-4,000 chars |

## Pre-flight Checklist

1. Verify user provides sufficient event details (time, location, actors, sequence, communication data)
2. If info is insufficient, proactively ask: event basics, current communication landscape, available data
3. For **Investigation & Analysis** type, additionally verify: phenomenon timeline, key actors/players, operational/business model, legal/regulatory framework, domestic/local impact channels, existing warnings or prior incidents, social/political/economic/cultural impact dimensions
3. Confirm report type with user. If unclear, infer:
   - Emerging tech/finance/cross-border phenomenon needing investigation → Investigation & Analysis
   - Single breaking incident → Rapid Assessment
   - Developed incident needing multi-dimensional analysis → Special Report
   - Macro policy / intl relations / industry security → Deep Research
   - Incident mostly resolved, needs lessons learned → Retrospective
   - Periodic summary → Monthly
   - Foreign pressure / intl conflict → Special Event

## Workflow

### Step 1: Information Collection

1. Organize user-provided core facts (timeline, involved parties, key nodes)
2. If URLs provided, use `web_fetch` to gather more details and latest communication data
3. If background is needed, use `web_search` to find related reports and similar cases

### Step 2: Determine Report Type

Match event characteristics to the appropriate template. Key decision criteria:
- **Event intensity**: High heat + ongoing → Special Report; moderate but needs warning → Rapid Assessment
- **Analysis depth**: Needs industry/policy deep dive → Research Report; needs lessons learned → Retrospective
- **Time dimension**: Single point in time → Rapid Assessment; multi-day period → Monthly
- **Event nature**: International relations / foreign forces → Special Event Report
- **Emerging phenomenon/investigation**: New technology, cross-border finance, religious-linked activity, regulatory grey zone → Investigation & Analysis Report

### Step 3: Write per Template

Strictly follow the selected type's structure. Core requirements:

1. **Precise title**: Summarizes event essence. No exclamation marks or question marks
2. **Data citation**: Use specific numbers. Attribute sources and time points
3. **Risk elaboration**: Each risk point follows the chain: "trigger condition → risk behavior → risk consequence"
4. **Practical recommendations**: Each recommendation must be actionable, assignable to a responsible body, with expected outcomes
5. **Formal language**: Official document style. No colloquial or emotional expressions

### Step 4: Delivery

Output as Markdown. The report uses Chinese throughout since it targets Chinese government/enterprise audiences.

## Key Writing Principles

- All analysis based on facts. No speculation or exaggeration
- Risk assessment must be concrete and operational
- Use official document stock phrases where appropriate (see references)
- Rigorous wording when covering negative information. No pre-judged positions
- Attribute external information sources
- Communication data must be precise to the number
- Timeline marked to the day (hour:minute when necessary)
- For location references, use xx to replace specific city names (maintain consistency)

## Enumeration Standards

Two enumeration systems are available. Match to report type:

### System A: First/Second/Third (for sentiment reports)
Used in: Rapid Assessment, Special Report, Monthly Report, Retrospective
> "First, ... Second, ... Third, ..."

### System B: 一是/二是/三是 (for investigation reports)
Used in: Investigation & Analysis Report
> "一是基本情况...二是运营模式...三是风险分析..."

**Nested enumeration rules:**
- Top-level section markers: 一、二、三、四、五
- Sub-level using: 一是/二是/三是  (with full-width Chinese numbering)
- Third level: (一)(二)(三) or bullet points
- Maximum 3 levels of nesting

## Investigation Report Writing Standards (调研分析报告专有)

| Principle | Description |
|-----------|-------------|
| **Opening formula** | Begin with "工作发现" / "调研发现" / "网络巡查发现" — establishes investigative posture |
| **Fact-first structure** | Facts before analysis: 基本情况→运营模式→境内传播→社会政治经济文化影响→风险评估→对策建议 |
| **Legal citations** | Full regulatory title + issuing body + date. E.g.: "2026年2月，中国人民银行等八部门联合发布《关于进一步防范和处置虚拟货币等相关风险的通知》" |
| **Bilingual naming** | First mention of foreign terms: original + Chinese translation + abbreviation if any |
| **一是/二是/三是 pattern** | Use throughout for structured enumeration of findings |
| **Data precision** | Specific numbers, dates, platform names, currency values |
| **Social/Political/Economic/Cultural impact** | Each dimension separately analyzed: affected groups, governance implications, market consequences, cultural value shifts |

## Legal Citation Format

When citing Chinese laws, regulations, or policy documents:
```
[Issuance date], [Issuing body] [Document Title]
Example: 2026年2月，中国人民银行等八部门联合发布《关于进一步防范和处置虚拟货币等相关风险的通知》
```
Key legal sources commonly cited in investigations:
- 中国人民银行 + multi-ministry notices
- 《中华人民共和国刑法》第X条
- 《中华人民共和国网络安全法》
- 《中华人民共和国数据安全法》
- 《中华人民共和国个人信息保护法》
- State Council opinions and regulations
- Local government risk warnings (cite when applicable)

## Core Risk Analysis Logic (Three-Layer Progression)

Each risk point follows this structure:

1. **Risk trigger / context** — "Currently...", "As... approaches...", "With X node approaching..."
2. **Risk behavior and actors** — "Some netizens may...", "Certain self-media accounts...", "Foreign forces..."
3. **Risk consequences and impact** — "Leading to...", "Triggering...", "Exacerbating...", "Causing damage to..."

**Complete example:**
> Guard against incitement leading to group polarization. As several sensitive anniversaries approach (trigger), certain netizens may exploit "patriotic" framing to spread inflammatory rhetoric on platforms (behavior), escalating social antagonism and undermining stability (consequence).

## Recommendation Writing Standards

Each recommendation: **Responsible body + Specific action + Expected outcome**
- Macro before micro
- Online and offline measures in parallel
- Both "treat symptoms" and "treat root causes"
- Quantity: Rapid Assessment 3-5 / Special Report & Retrospective 5-8 / Research Report 4-6 / Monthly 8-10

## Reference Files

`references/templates.md` — Full template structures, formatting specs, and composition guidelines for all 10 report types
