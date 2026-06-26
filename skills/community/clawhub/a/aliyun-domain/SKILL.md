---
  name: aliyun-domain
  description: Manage domain assets through Alibaba Cloud OpenAPI, supporting domain query, renewal, transfer, registration, and information modification. Requires user double confirmation for financial operations. Also provides Alibaba Cloud domestic domain promotion policy consultation, including registration activity prices, bulk registration discounts, transfer-in discounts, renewal discounts, and promotional codes. Added domain, website building, and filing industry consulting capabilities, based on RAG retrieval of local knowledge base (knowledge/aliyun-domain-help) to provide accurate answers. Added domain monitoring subscription functionality to monitor domain expiration time, WHOIS information changes, and SSL certificate status. Built-in creative domain naming capability, providing intelligent naming suggestions for projects/brands and checking availability.
  triggers:
    - "domain monitoring"
    - "WHOIS"
    - "domain expiration"
    - "SSL certificate"
    - "domain query"
    - "domain renewal"
    - "domain registration"
    - "domain transfer"
    - "domain ownership transfer"
    - "domain filing"
    - "domain website building"
    - "domain trading"
    - "domain investment"
    - "hotspot domain"
    - "domain price"
    - "promotional code"
    - "creative naming"
    - "domain naming"
    - "brand naming"
    - "project naming"
    - "brainstorm domain"
    - "domain suggestion"
---
# Alibaba Cloud Domain Management Skill

Manage domain assets through Alibaba Cloud OpenAPI, supporting domain query, renewal, transfer, registration, and information modification.

## 🆕 Industry Consulting Capability (RAG Retrieval)

### Feature Description

When users ask questions related to domain registration, trading, website building, filing, etc., **must use RAG capability to retrieve local knowledge base** `knowledge/aliyun-domain-help` Alibaba Cloud help documents, and answer users based on document content.

### Trigger Rules

**When user questions involve any of the following topics, RAG retrieval must be triggered:**

| Topic Category | Trigger Words/Scenarios | Search Keywords Example |
|:---|:---|:---|
| 🆕 **Domain Registration** | How to register domain, registration process, what is needed for registration, registration conditions | `domain registration` `registration process` `real-name verification` |
| 💰 **Domain Trading** | Domain buying/selling, fixed price, domain push, domain buyback, trading process | `domain trading` `buy domain` `fixed price` `push` |
| 🏗️ **Website Building** | How to build website, website setup, building process, domain binding | `website building` `website setup` `domain binding` `resolution` |
| 📋 **Filing** | ICP filing, filing process, filing materials, filing conditions, website filing | `filing` `ICP` `website filing` `filing materials` |
| 🔒 **Domain Security** | Domain lock, transfer lock, update lock, security protection | `lock` `security lock` `prohibit transfer` |
| 📝 **Domain Management** | Domain ownership transfer, information modification, DNS modification, domain transfer | `ownership transfer` `information modification` `DNS` `transfer` |
| 💸 **Renewal & Redemption** | Domain renewal, expired redemption, renewal price, redemption process | `renewal` `redemption` `expired domain` |
| ❓ **FAQ** | Domain issues, registration failure, audit rejected, error messages | `FAQ` `common issues` `failure` `error` |

### RAG Retrieval Process

1. **Identify User Intent**: Extract keywords and topics from user questions
2. **Call RAG Retrieval**: Use `domain_knowledge_rag.py` to retrieve local knowledge base
3. **Integrate Document Content**: Organize answers based on retrieved help document fragments
4. **Mark Sources**: Must mark the cited document names and categories in the answer
5. **Provide Links**: If original links are available, provide them to users

### Answer Standards

1. **Retrieve Before Answering**: Must call RAG to retrieve knowledge base first, cannot answer from memory
2. **Mark Document Sources**: Clearly state the cited document names in the answer, such as "According to the Domain Registration Quick Start document..."
3. **Maintain Original Accuracy**: Key steps, conditions, requirements, etc. must be consistent with the original
4. **Segment Citations**: Multiple document contents should be marked in segments to avoid confusion
5. **Timeliness Note**: Remind users of document update time, recommend referring to the latest version on Alibaba Cloud official website
6. **Beyond Knowledge Base Scope**: If no relevant documents are retrieved, inform truthfully and provide official website links

### Example Dialogue

**Domain Registration Consultation:**
```
User: I want to register a domain, what is the process?
AI: 📚 According to Alibaba Cloud help document "Domain Registration Quick Start", the domain registration process is as follows:

1. **Query Domain Availability**
   - Visit Alibaba Cloud domain query page
   - Enter desired domain name
   - Check if domain is available for registration

2. **Real-name Verification**
   - Individual users: Upload front and back of ID card
   - Enterprise users: Upload business license
   - Wait for review (usually 1-2 business days)

3. **Submit Registration Order**
   - Select registration period (1-10 years)
   - Fill in domain holder information
   - Complete payment

4. **Domain Management**
   - Set DNS server
   - Configure domain resolution
   - Enable security protection (transfer lock, etc.)

📄 Complete document: knowledge/aliyun-domain-help/02-快速入门/域名注册快速入门.md
🔗 Original link: https://help.aliyun.com/zh/dws/getting-started/domain-name-quick-start
```

**Website Building Consultation:**
```
User: How to build a website after registering a domain?
AI: 📚 According to Alibaba Cloud help document "From Domain Registration to Website Building", the complete website building process is as follows:

**Stage 1: Domain Preparation**
1. Register domain and complete real-name verification
2. Set domain resolution (DNS)

**Stage 2: Server Preparation**
1. Purchase cloud server (ECS) or virtual hosting
2. Configure server environment (web server, database, etc.)

**Stage 3: Website Filing**
1. Prepare filing materials (ID card/business license, domain certificate, etc.)
2. Submit application through Alibaba Cloud filing system
3. Wait for administration bureau review (usually 7-20 business days)

**Stage 4: Website Deployment**
1. Upload website code to server
2. Configure domain resolution pointing to server IP
3. Test website access

📄 Cited documents:
- knowledge/aliyun-domain-help/02-快速入门/从域名注册到网站搭建.md
- knowledge/aliyun-domain-help/05-备案与合规/ICP 备案流程.md
```

**Filing Consultation:**
```
User: What materials are needed for personal website filing?
AI: 📚 According to Alibaba Cloud help document "ICP Filing Process", personal website filing materials include:

**Required Materials:**
1. ✅ Personal ID card front and back scans
2. ✅ Domain certificate (can be downloaded from Alibaba Cloud domain console)
3. ✅ Personal contact information (phone number, email)
4. ✅ Website responsible person photo (half-body photo)

**Other Possible Materials:**
- Personal commitment letter (required in some regions)
- Pre-approval documents (special industries)

**Filing Conditions:**
- Domain has completed real-name verification for more than 3 days
- Domain holder is the same person as filing responsible person
- Individual must be at least 18 years old

📄 Complete document: knowledge/aliyun-domain-help/05-备案与合规/ICP 备案流程.md
⚠️ Note: Requirements may vary slightly by administration bureau, please refer to the local administration bureau review for specifics.
```

**Domain Trading Consultation:**
```
User: What does fixed price domain mean?
AI: 📚 According to Alibaba Cloud help documents "Fixed Price (Premium)" and "Fixed Price (Select)":

**Fixed Price Domain** refers to a trading method where the seller sets a fixed price, and the buyer immediately obtains domain ownership after payment.

**Fixed Price (Premium) vs Fixed Price (Select):**

| Type | Description | Price Range | Review |
|:---|:---|:---|:---|
| Premium | Published by regular sellers, price self-determined | Tens to hundreds of thousands of yuan | Automatic review |
| Select | Platform selected premium domains | Usually over 10,000 yuan | Manual review |

**Trading Process:**
1. Buyer places order and pays
2. System automatically transfers domain
3. Transaction complete (usually 1-2 hours)

**Notes:**
- Confirm domain has no disputes or violation records
- Check domain history (whether penalized by search engines)
- Understand transfer process and fees

📄 Cited documents:
- knowledge/aliyun-domain-help/04-域名交易/一口价（优选）.md
- knowledge/aliyun-domain-help/04-域名交易/一口价（严选）.md
```

## ⚠️ Security Rules (Important)

### 🔐 Double Confirmation Principle for Financial Operations

**All API calls involving orders and financial operations must be explicitly double confirmed by the user before execution!**

#### Operations Requiring Double Confirmation

The following operations **must** display detailed information to the user and obtain explicit confirmation (such as "confirm", "yes", "ok", etc.) before calling the API:


| Operation Type | Risk Level | Confirmation Content |
| ------------------------ | -------- | -------------------------------------- |
| 🆕 Domain Registration | 🔴 High | Domain name, registration period, total cost, registrant information |
| 💰 Domain Renewal | 🔴 High | Domain name, renewal period, total cost, expiration time |
| 🔄 Domain Redemption | 🔴 High | Domain name, redemption price, current status |
| 📝 Domain Transfer (In/Out) | 🟡 Medium | Domain name, transfer fee, target registrar |
| 🔒 Domain Lock/Unlock | 🟡 Medium | Domain name, operation type, impact description |
| ✏️ Contact Information Modification | 🟡 Medium | Domain name, modified fields, old/new value comparison |
| 🌐 DNS Server Modification | 🟡 Medium | Domain name, old/new DNS list |

#### Confirmation Process

1. **Display Operation Details**: Clearly list operation content, scope of impact, fee details
2. **Wait for User Confirmation**: Must obtain explicit affirmative reply from user
3. **Execute Operation**: Call API after confirmation
4. **Feedback Result**: Provide immediate feedback after operation completes

#### Example Dialogue

❌ **Wrong Approach** (Execute without confirmation):

```
User: Help me register shenyue.xyz
AI: ✅ Registered shenyue.xyz (Order number: xxx)
```

✅ **Correct Approach** (Confirm before executing):

```
User: Help me register shenyue.xyz
AI: 🛒 Domain Registration Confirmation

Domain: shenyue.xyz
Period: 1 year
Cost: ¥7
Registrant: [Template ID: xxx]
Real-name Status: ✅ Verified

Confirm registration? Reply "confirm" to continue.

User: confirm
AI: ✅ Registration successful! Order number: xxx
```

#### Operations Not Requiring Confirmation

The following query operations **do not** require confirmation and can be executed directly:

- ✅ Domain list query
- ✅ Domain detail query
- ✅ Domain availability check
- ✅ Task status query
- ✅ Contact information query
- ✅ Statistics retrieval
- ✅ Expiring domain query
- ✅ Domain price/promotion policy query

---

## 📚 Safe Operation Guide

For detailed safe operation guide and code examples, please refer to:

- 📄 [SAFE_OPERATION_GUIDE.md](SAFE_OPERATION_GUIDE.md) - Complete safe operation guide
- 🧪 [scripts/safe_operation_example.py](scripts/safe_operation_example.py) - Safe operation example code

---

## 📖 Local Knowledge Base

### Knowledge Base Files

| File Path | Content Description |
| --------------------------------------- | ------------------------------------------------------------------------------------ |
| `knowledge/domain_pricing_discounts.md` | Alibaba Cloud domestic domain promotion policies (registration activity prices, bulk registration discounts, transfer-in discounts, renewal discounts, promotional codes) |
| `knowledge/aliyun-domain-help/` | Alibaba Cloud domain service help document library (complete guide for domain registration, trading, management, website building, filing, etc.) |

> Need to update `knowledge/domain_pricing_discounts.md` promotion policy content at the beginning of each month.
> Regularly update help documents in `knowledge/aliyun-domain-help/` to ensure content timeliness.

### Help Document Library Structure

```
knowledge/aliyun-domain-help/
├── 01-产品概述/           # Domain service introduction, basic concepts, price description
├── 02-快速入门/           # Domain registration, trading, website building quick guides
├── 03-操作指南/           # Detailed operation tutorials (registration, verification, transfer, security, etc.)
├── 04-域名交易/           # Trading types, purchase process, anti-fraud guide
├── 05-备案与合规/         # ICP filing process, compliance requirements
└── 06-常见问题/           # Various FAQs and problem solutions
```

### RAG Retrieval Script

Use `scripts/domain_knowledge_rag.py` for knowledge base retrieval:

```bash
# Command line usage
python3 scripts/domain_knowledge_rag.py "domain registration process"
python3 scripts/domain_knowledge_rag.py "what materials are needed for filing"
python3 scripts/domain_knowledge_rag.py "how to build website"

# Python code usage
from domain_knowledge_rag import answer_with_rag

answer = answer_with_rag("What conditions are needed for domain ownership transfer?")
print(answer)
```

### Trigger Rules

**When user questions involve any of the following topics, must read `knowledge/domain_pricing_discounts.md` before answering:**

- Domain registration price / registration fee / how much for registration
- Domain renewal price / renewal fee / how much for renewal
- Domain transfer-in price / transfer-in fee
- Bulk registration discount / bulk renewal discount
- Promotion activity / discount / sale / promotion
- Promotional code / renewal code
- Premium word / premium domain discount
- Multi-year registration package / register for multiple years at once
- Which suffix is cheaper / cheapest domain
- Fee confirmation before user performs registration/renewal/transfer-in operation

### Creative Naming Trigger Rules 🆕 NEW

**When user needs creative domain naming, directly perform creative analysis and domain recommendation:**

| Trigger Scenario | Example Question | Processing Method |
|:---|:---|:---|
| **New Project Naming** | "I want to make a project management tool, help me name a domain" | Analyze project → Generate creative domains → Check availability |
| **Brand Naming** | "Give my design studio a brand domain" | Understand brand positioning → Recommend brand domain |
| **Creative Divergence** | "Help me brainstorm some domain ideas" | Multi-angle divergence → Provide various style options |
| **Product Naming** | "What domain should my AI writing assistant use" | Analyze product features → Match target audience |
| **Specific Keyword** | "Recommend domains based on the word 'pixel'" | Keyword variations → Combination generation |
| **Suffix Preference** | "Want a short domain with .io suffix" | Specify suffix → Filter short domains |

#### Creative Naming Workflow

**Step 1: Understand Project/Brand**

Analyze information provided by user:
- Project type: SaaS / Tool / Platform / Content site / E-commerce, etc.
- Target audience: Developers / Enterprises / Consumers / Specific industries
- Core functionality: What problem does it mainly solve
- Brand tone: Professional / Friendly / Tech-savvy / Creative

**Step 2: Generate Creative Domains**

Generate 10-15 candidate domains according to the following strategies:

| Strategy | Description | Example |
|:---|:---|:---|
| **Descriptive Naming** | Directly describe product functionality | codeclip.com (code snippet tool) |
| **Metaphorical Naming** | Use related metaphors | lighthouse.io (navigation/guidance) |
| **Compound Words** | Two words combined | devflow.dev (developer workflow) |
| **Creative Spelling** | Omit letters or creative spelling | pixl.ai (pixel variant) |
| **Short Domain** | 4-6 letter short words | snap.io / flux.dev |
| **Suffix Fusion** | Domain combined with suffix | get.dev / start.io |

**Step 3: Check Availability**

Use Alibaba Cloud API to check domain registrability:
- Priority check .com / .cn (mainstream suffixes)
- Check .io / .dev / .ai (tech suffixes)
- Check .app / .co / .xyz (alternative choices)

**Step 4: Output Recommendation Plan**

Formatted output, including:
- Available domain list (marked with ✓)
- Recommendation reason for each domain
- Alibaba Cloud price and promotion information
- One-click purchase link

#### Domain Naming Best Practices

**Characteristics of Good Domains:**

| Characteristic | Description | Example |
|:---|:---|:---|
| ✓ **Short** | Ideally within 15 characters | flux.dev (4 characters) |
| ✓ **Memorable** | Easy to recall and spell | snippetbox.com |
| ✓ **Pronounceable** | Can be communicated verbally | codeflow.io |
| ✓ **Descriptive** | Suggests product functionality | devtools.io |
| ✓ **Brandable** | Unique and recognizable | vercel.com |
| ✗ **No Hyphens** | Avoid confusion | ❌ code-box.com |

**TLD Selection Guide:**

| Suffix | Applicable Scenarios | Price Reference |
|:---|:---|:---|
| **.com** | General, commercial, global business | ¥85/year |
| **.cn** | China market, domestic business | ¥38/year |
| **.io** | Tech startups, developer tools | ¥198/year |
| **.dev** | Developer products, tech projects | ¥88/year |
| **.ai** | AI/ML products | ¥680/year |
| **.app** | Mobile apps, Web apps | ¥88/year |
| **.co** | .com alternative, startups | ¥168/year |
| **.xyz** | Creative projects, low-cost choice | ¥7/year |
| **.tech** | Tech companies, tech products | ¥38/year |

#### Example Dialogue

```
User: I want to make a project management tool for remote teams, help me name a domain

AI: 🎯 Analyzing your project...

**Project Analysis:**
- Type: Collaboration tool / SaaS
- Audience: Remote teams, project managers
- Core functionality: Task management, team collaboration, progress tracking
- Brand tone: Professional, efficient, modern

🎯 Creative Domain Recommendations

## Available Domains (.com)
1. ✓ teamflow.com - Team workflow, intuitive and memorable
   Reason: Directly conveys "team collaboration process" concept

2. ✓ collabboard.com - Collaboration board
   Reason: Combines collaboration + board, clear functionality

## Available Domains (Tech Suffixes)
3. ✓ teamsync.io - Team sync
   Reason: .io popular with tech startups, sync suggests real-time collaboration

4. ✓ remotely.dev - Remote work
   Reason: .dev suffix fits developer audience, remotely directly addresses the topic

5. ✓ collab.app - Collaboration app
   Reason: .app suffix feels modern, collab is concise and powerful

## Already Registered (.com)
- team.com (registered)
- collaborate.com (registered, premium domain)

## Recommendation Ranking

🏆 Top Choice: teamsync.io
- Short and powerful (8 characters)
- Strong tech feel, suitable for SaaS positioning
- .io suffix has high recognition among target audience

🥈 Alternative: teamflow.com
- .com suffix has strong universality
- Easy for word-of-mouth spread
- Great branding potential

💰 Alibaba Cloud Prices:
- teamsync.io: ¥198/year
- teamflow.com: ¥85/year (can be reduced to ¥82 with promotional code)

🔗 One-click Purchase:
- [teamsync.io](https://wanwang.aliyun.com/buy/commonbuy?domain=teamsync&suffix=io&duration=12)
- [teamflow.com](https://wanwang.aliyun.com/buy/commonbuy?domain=teamflow&suffix=com&duration=12)

💡 Tip: Recommend registering both .com and .io suffixes to protect the brand
```

### Hotspot Investment Analysis Trigger Rules ⭐ NEW

**When user questions involve the following keywords, trigger hotspot domain investment analysis feature:**

| Trigger Word | Example Question | Recommended Operation |
|:---|:---|:---|
| `hotspot` | "What are the recent domain investment hotspots?" | Recommend claw/ai/agent and other hotspot keywords |
| `investment` | "Are claw-related domains worth investing in?" | Analyze claw keyword domain investment opportunities |
| `recommend` | "Recommend some domains worth registering" | Recommend registrable domains based on hotspots |
| `bulk` | "Want to bulk register some domains for investment" | Recommend .xyz and other low-price suffix combinations |
| `lucky numbers` | "What lucky number domains are available for registration" | Analyze 168/518/678 and other number combinations |
| `AI domain` | "What AI-related domains are available for registration" | Analyze ai/agent/bot and other keywords |

**Analysis Process**:

1. **Identify Hotspot Keywords**: Extract keywords from user questions (such as claw, ai, agent)
2. **Generate Candidate Domains**: Generate 50+ candidate domain combinations based on keywords
3. **Batch Check Registrability**: Call API to check registration status of each domain
4. **Generate Investment Recommendations**: Sort by heat, price, potential, output TOP 10 recommendations
5. **Provide Registration Suggestions**: Include promotional codes and total cost estimates
6. **Generate Purchase Links**: Generate Alibaba Cloud one-click purchase links for each recommended domain (universal feature)

### Purchase Link Feature ⭐ NEW (Universal)

**All recommended registrable domains in all scenarios will automatically generate purchase links:**

| Scenario | Description | Example |
|:---|:---|:---|
| Hotspot investment analysis | Registrable domains recommended for hotspot keywords | `python3 domain_hotspot_analyzer.py claw` |
| Daily domain check | Check if a domain is registrable | `check_domain("example.cn")` |
| Bulk domain screening | Batch check registrability of multiple domains | Loop through domain list check |
| Keyword recommendation | Recommend domains based on user-provided keywords | "Recommend some AI-related domains" |
| Lucky number combinations | Lucky number domain recommendations | "What 168-ending domains are available for registration" |

**Link Specification**:

- **Link Format**: `https://wanwang.aliyun.com/buy/commonbuy?domain={domain}&suffix={suffix}&duration=12`
- **Auto Extract**: Automatically extract suffix from complete domain (e.g., tryagent.cn → domain: tryagent, suffix: cn)
- **One-click Purchase**: Click link to go directly to Alibaba Cloud purchase page, domain and period (1 year) pre-filled
- **Output Format**:
  - Markdown clickable link: `[tryagent.cn](https://wanwang.aliyun.com/buy/commonbuy?domain=tryagent&suffix=cn&duration=12)`
  - Quick link list: Provide complete links for all recommended domains at the end of the report

**Example Output**:

```
✅ Registrable Domain Recommendations:

1. [claw168.cn](https://wanwang.aliyun.com/buy/commonbuy?domain=claw168&suffix=cn&duration=12) - ¥38 🔢 Lucky Number
2. [claw518.cn](https://wanwang.aliyun.com/buy/commonbuy?domain=claw518&suffix=cn&duration=12) - ¥38 🔢 Lucky Number
3. [tryagent.cn](https://wanwang.aliyun.com/buy/commonbuy?domain=tryagent&suffix=cn&duration=12) - ¥38 🤖 AI Agent

🔗 Quick Purchase Links:
  1. https://wanwang.aliyun.com/buy/commonbuy?domain=claw168&suffix=cn&duration=12
  2. https://wanwang.aliyun.com/buy/commonbuy?domain=claw518&suffix=cn&duration=12
  3. https://wanwang.aliyun.com/buy/commonbuy?domain=tryagent&suffix=cn&duration=12
```

### Answer Standards

1. **Read Before Answering**: Must fully read knowledge base file before answering user. Do not answer price questions from memory.
2. **Mark Timeliness**: When answering, state the validity period of promotion policies (e.g., "March activity price, ends March 31"), remind users to note activity time.
3. **Include Links**: If knowledge base contains official website activity links, provide them when answering.
4. **Fee Confirmation Collaboration**: When user wants to perform registration/renewal/transfer-in operation, actively cite promotion prices from knowledge base in double confirmation step to help users understand the best plan. For example: If user renews .com, remind them they can use promotional code to get a lower price.
5. **Beyond Knowledge Base Scope**: If the suffix or scenario user asks about is not in the knowledge base, truthfully state that current knowledge base does not cover it, suggest user check the latest price on Alibaba Cloud official website.
6. **Price For Reference Only**: Actual order price is subject to Alibaba Cloud API return or official website page display, must include this note when answering.

### Example Dialogue

**Price Query:**

```
User: How much does it cost to register a .xyz domain?
AI: 📋 .xyz Domain Registration Price

Original Price: 14 yuan
March Activity Price: 7 yuan (activity ends March 31)

Note: Actual price is subject to order time. Need help registering a .xyz domain?
```

**Promotional Code Query:**

```
User: Are there any discounts for .com renewal?
AI: 💰 .com Renewal Discount Plan

1. Promotional Code: Use code 「com批量注册更享优惠」, renewal price drops from 95 yuan to 90 yuan
2. Bulk Renewal Discount (single order):
   - ≥20: 84 yuan each
   - ≥50: 83 yuan each
   - ≥100: 82 yuan each

Suggestion: If only renewing a few domains, using the promotional code will get the best price.
```

**Operation Collaboration:**

```
User: Help me renew example.com
AI: 🛒 Domain Renewal Confirmation

Domain: example.com
Period: 1 year
Cost: ¥95
💡 Tip: Use promotional code 「com批量注册更享优惠」 to reduce to ¥90

Confirm renewal? Reply "confirm" to continue.
```

**Creative Naming Collaboration:**

```
User: I want to make a project management tool for remote teams, help me name a domain

AI: 🎯 Calling creative domain naming tool for you...

[Call domain-name-brainstormer skill to generate creative suggestions]

🎯 Based on your remote team project management tool, recommend the following domains:

## Available Domain Recommendations (.com)
1. ✓ snippetbox.com - Clear, memorable
   Reason: Directly describes product functionality
   💰 Alibaba Cloud Price: ¥85/year
   🔗 [Buy Now](https://wanwang.aliyun.com/buy/commonbuy?domain=snippetbox&suffix=com&duration=12)

2. ✓ codeclip.com - Short and powerful
   Reason: Suggests quick code sharing
   💰 Alibaba Cloud Price: ¥85/year
   🔗 [Buy Now](https://wanwang.aliyun.com/buy/commonbuy?domain=codeclip&suffix=com&duration=12)

## Available Domain Recommendations (Tech Suffixes)
3. ✓ snippet.dev - Developer first choice
   Reason: .dev extension adds credibility
   💰 Alibaba Cloud Price: ¥88/year
   🔗 [Buy Now](https://wanwang.aliyun.com/buy/commonbuy?domain=snippet&suffix=dev&duration=12)

4. ✓ codebox.io - Strong tech feel
   Reason: .io popular with tech startups
   💰 Alibaba Cloud Price: ¥198/year
   🔗 [Buy Now](https://wanwang.aliyun.com/buy/commonbuy?domain=codebox&suffix=io&duration=12)

🏆 Recommendation: snippet.dev - Perfect fit for developer audience
💡 Tip: Use promotional code to save costs
```

---

## 📋 Feature Overview

### 🆕 Industry Consulting Capability (RAG Retrieval)

- ✅ **Domain Registration Consultation**: Registration process, real-name verification, registration conditions, required materials
- ✅ **Domain Trading Consultation**: Domain buying/selling, fixed price, push, buyback, trading process
- ✅ **Website Building Consultation**: Complete website building process, domain binding, resolution configuration
- ✅ **Filing Consultation**: ICP filing process, filing materials, filing conditions, various administration bureau requirements
- ✅ **Domain Management Consultation**: Ownership transfer, information modification, DNS settings, security protection
- ✅ **Renewal & Redemption Consultation**: Renewal process, redemption price, expiration handling
- ✅ **FAQ Answers**: Registration failure, audit rejection, various error handling

**RAG Retrieval Features**:
- 📚 Based on Alibaba Cloud official help documents
- 🔍 Intelligent semantic retrieval, precise matching
- 📄 Mark document sources and categories
- 🔗 Provide original links
- ⏰ Mark document update time

### Domain Management

### Domain Investment Analysis ⭐ NEW

- ✅ **Hotspot Keyword Analysis**: Recommend domain investment opportunities based on market hotspots
- ✅ **Bulk Domain Screening**: Automatically generate candidate domains and check registrability
- ✅ **Investment Value Assessment**: Provide heat level, investment reason, price estimate
- ✅ **Lucky Number Combinations**: Support 168/518/678/886 and other lucky number combinations
- ✅ **Domain Asset Assessment Dashboard** 📊: One-click generate asset overview/expiration distribution/value statistics/asset recommendations
- ✅ **Purchase Link Generation**: All registrable domains automatically generate one-click purchase links

### Creative Domain Naming 🆕 NEW

- ✅ **Project Understanding Analysis**: Analyze project type, target audience, core functionality, brand tone
- ✅ **Creative Naming Strategy**: Descriptive/metaphorical/compound words/creative spelling/short domain/suffix fusion
- ✅ **Multi-suffix Recommendation**: .com/.cn/.io/.dev/.ai/.app/.co/.xyz/.tech, etc.
- ✅ **Availability Check**: Call Alibaba Cloud API to check domain registrability in real-time
- ✅ **Brand Insight Explanation**: Explain recommendation reason and applicable scenarios for each domain
- ✅ **Alibaba Cloud Price Integration**: Automatically attach Alibaba Cloud purchase links and promotion information
- ✅ **TLD Selection Guide**: Recommend best suffix based on project type

### Domain Monitoring Subscription 🆕 NEW

- ✅ **Domain Expiration Monitoring**: Real-time monitoring of domain expiration time, advance warning
- ✅ **WHOIS Information Tracking**: Record registrar, DNS and other key information changes
- ✅ **SSL Certificate Monitoring**: Check certificate validity and expiration time
- ✅ **Status Change Alert**: Timely reminder of important changes
- ✅ **Monitoring History Query**: View domain monitoring records and alert history

**Supported Hotspot Keywords**:

| Keyword | Hotspot Topic | Heat | Description |
|:---|:---|:---:|:---|
| `claw` | Claw Hotspot (OpenClaw) | ⭐⭐⭐⭐⭐ | 2026 GitHub's hottest open source AI project, 180k stars |
| `ai` | Artificial Intelligence | ⭐⭐⭐⭐⭐ | AI.com sold for $70 million, agent craze |
| `agent` | AI Agent | ⭐⭐⭐⭐⭐ | AI Agent is the hottest investment direction in 2026 |
| `bot` | Robot/Automation | ⭐⭐⭐⭐ | Automation robot concept |
| `qwen` | Qwen | ⭐⭐⭐⭐ | Alibaba's Tongyi large model series |
| `168/518/678/886` | Lucky Numbers | ⭐⭐⭐ | Lucky number combinations preferred by Chinese people |

### Domain Promotion Policy Consultation

- ✅ Query domain registration activity prices (various suffix activity prices, premium word discounts)
- ✅ Query bulk registration discounts (.com/.cn/.net/.xin bulk price tiers)
- ✅ Query domain transfer-in discounts (Wednesday transfer-in day activity prices)
- ✅ Query renewal discounts (bulk renewal discounts + promotional codes)
- ✅ Recommend optimal registration/renewal/transfer-in plans

## 🔐 Configuration Instructions

### 1. Get Alibaba Cloud AccessKey

1. Login to [Alibaba Cloud Console](https://ram.console.aliyun.com/)
2. Enter RAM Access Control
3. Create user or use existing user
4. Create AccessKey (AK/SK)
5. Authorize user with `AliyunDomainFullAccess` permission

### 2. Configure Environment Variables (Recommended)

**Set AccessKey through environment variables, no need to create configuration file:**

```bash
export ALIYUN_ACCESS_KEY_ID="your-access-key-id"
export ALIYUN_ACCESS_KEY_SECRET="your-access-key-secret"
```

**Permanent Configuration** (add to `~/.bashrc` or `~/.zshrc`):

```bash
echo 'export ALIYUN_ACCESS_KEY_ID="your-access-key-id"' >> ~/.zshrc
echo 'export ALIYUN_ACCESS_KEY_SECRET="your-access-key-secret"' >> ~/.zshrc
source ~/.zshrc
```

**Parameter Description**:


| Environment Variable | Description | Example |
| ------------------------- | ------------------- | ----------- |
| `ALIYUN_ACCESS_KEY_ID` | Alibaba Cloud AccessKey ID | `LTAI5t...` |
| `ALIYUN_ACCESS_KEY_SECRET`| Alibaba Cloud AccessKey Secret | `abcdef...` |

### 3. Security Recommendations

- ✅ **Recommend using environment variables, avoid hardcoding to files**
- ✅ Recommend using RAM sub-account AK, not main account
- ✅ Regularly rotate AccessKey
- ⚠️ Do not commit AccessKey to Git or share with others

## 🚀 Usage

### Command Line Usage

```bash
# Configure environment variables (first use or each new terminal session)
export ALIYUN_ACCESS_KEY_ID="your-access-key-id"
export ALIYUN_ACCESS_KEY_SECRET="your-access-key-secret"

# Query domain list
python3 scripts/aliyun_domain.py list

# Query domain details
python3 scripts/aliyun_domain.py detail --domain example.com

# Query expiring domains
python3 scripts/aliyun_domain.py expiring --days 30

# Domain renewal
python3 scripts/aliyun_domain.py renew --domain example.com --years 1

# Query domain tasks
python3 scripts/aliyun_domain.py tasks --status Running

# 🔥 Hotspot domain investment analysis (NEW)
python3 scripts/domain_hotspot_analyzer.py claw
python3 scripts/domain_hotspot_analyzer.py ai
python3 scripts/domain_hotspot_analyzer.py agent

# List all supported hotspot keywords
python3 scripts/domain_hotspot_analyzer.py --list

# 🆕 Domain monitoring subscription (NEW)
python3 scripts/domain_monitor.py add example.com           # Add domain monitoring
python3 scripts/domain_monitor.py status example.com        # View domain status
python3 scripts/domain_monitor.py list                      # List all monitoring
python3 scripts/domain_monitor.py check                     # Check all domains
python3 scripts/domain_monitor.py remove example.com        # Remove domain monitoring
python3 scripts/domain_monitor.py history example.com       # View monitoring history
```

### Industry Consulting RAG Retrieval Script

`scripts/domain_knowledge_rag.py` provides RAG-based industry consulting retrieval functionality, covering domain registration, trading, website building, filing and other topics:

```python
from domain_knowledge_rag import answer_with_rag, DomainKnowledgeRAG

# Method 1: Get answer directly
answer = answer_with_rag("What is the process for domain registration?")
print(answer)

# Method 2: Use retriever to get more detailed information
rag = DomainKnowledgeRAG()

# Search relevant documents
sections = rag.get_relevant_sections("filing materials", max_sections=3)
for section in sections:
    print(f"Title: {section['title']}")
    print(f"Category: {section['category']}")
    print(f"Excerpt: {section['excerpt'][:200]}...")
    print()

# Get complete document content
content = rag.get_document_content(sections[0]['file_path'])
print(content)
```

**Supported Query Types**:

| Query Type | Example | Description |
|:---|:---|:---|
| Domain Registration | "How to register domain" | Registration process, conditions, materials |
| Real-name Verification | "What is needed for real-name verification" | Individual/enterprise verification requirements |
| Domain Trading | "What is fixed price domain" | Trading types, process, notes |
| Website Building | "How to build website after registering domain" | Complete website building process, server selection |
| Filing | "Personal filing materials" | ICP filing process, materials, conditions |
| Domain Management | "How to transfer domain ownership" | Ownership transfer, information modification, DNS settings |
| Security Protection | "How to lock domain" | Transfer lock, update lock, security lock |
| Renewal & Redemption | "What to do if domain expires" | Renewal, redemption, prices |
| FAQ | "What to do if registration fails" | Various error handling, FAQ |

### Promotion Information Retrieval Script

`scripts/domain_promotion_search.py` provides RAG-based domain promotion information retrieval functionality:

### Python Code Usage

```python
import os
from aliyun_domain import AliyunDomainClient

# Read AccessKey from environment variables
access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID')
access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET')

# Initialize client
client = AliyunDomainClient(
    access_key_id=access_key_id,
    access_key_secret=access_key_secret
)

# Query domain list
domains = client.list_domains(page_size=100)
for domain in domains:
    print(f"{domain['DomainName']} - {domain['ExpirationDate']}")

# Query domain details
detail = client.query_domain_detail("example.com")
print(detail)

# Query expiring domains
expiring = client.query_expiring_domains(days=30)
print(f"Expiring: {len(expiring)} domains")

# Domain renewal (⚠️ Requires double confirmation)
# Step 1: Display confirmation information
print("🛒 Domain Renewal Confirmation")
print("Domain: example.com")
print("Period: 1 year")
print("Cost: ¥85")
confirm = input("Confirm renewal? (yes/no): ")

# Step 2: Execute after user confirmation
if confirm.lower() == 'yes':
    result = client.renew_domain("example.com", years=1)
    print(f"Renewal successful! Order number: {result.get('OrderId')}")
```

## 📚 API Reference

### Domain Management API


| Method | Function | API Action |
| ----------------------------- | ---------------- | ---------------------------------------- |
| `list_domains()` | Query domain list | DescribeDomains |
| `query_domain_detail()` | Query domain details | QueryDomainDetail |
| `query_domain_list()` | Paginated domain query | QueryDomainList |
| `query_expiring_domains()` | Query expiring domains | QueryDomainList |
| `save_single_domain_update()` | Domain information modification | SaveSingleTaskForUpdatingContactInfo |
| `transfer_domain_in()` | Domain transfer in | TransferDomainIn |
| `transfer_domain_out()` | Domain transfer out | TransferDomainOut |
| `renew_domain()` | Domain renewal | SaveSingleTaskForRenewingDomain |
| `register_domain()` | Domain registration | SaveSingleTaskForCreatingOrderActivate |
| `lock_domain()` | Domain lock | SaveSingleTaskForTransferProhibitionLock |
| `unlock_domain()` | Domain unlock | SaveSingleTaskForTransferProhibitionLock |

### Task Management API


| Method | Function | API Action |
| --------------------- | ------------ | ------------------- |
| `query_task_list()` | Query task list | QueryTaskList |
| `query_task_detail()` | Query task details | QueryTaskDetailList |

## 📁 File Structure

```
aliyun_domain/
├── SKILL.md                        # Skill documentation
├── README.md                       # Project description
├── SAFE_OPERATION_GUIDE.md         # Safe operation guide
├── config/
│   ├── credentials.json            # Credential configuration
│   └── credentials.json.example    # Configuration template
├── knowledge/                      # Local knowledge base 📚
│   ├── domain_pricing_discounts.md # Promotion policy knowledge base
│   └── aliyun-domain-help/         # Alibaba Cloud help document library (RAG retrieval) ⭐ NEW
│       ├── 01-产品概述/
│       ├── 02-快速入门/
│       ├── 03-操作指南/
│       ├── 04-域名交易/
│       ├── 05-备案与合规/
│       ├── 06-常见问题/
│       └── README.md
├── learnings/                      # Lessons learned library ⭐
│   ├── README.md                   # Index file
│   ├── API_QUICK_REFERENCE.md      # API quick reference
│   ├── API_FIELD_CASE_ISSUE.md     # API field case issue
│   ├── DOMAIN_LOCK_OPERATION.md    # Domain lock operation guide
│   └── REGISTRANT_PROFILE_QUERY.md # Real-name template query issue
└── scripts/
    ├── aliyun_domain.py            # Domain API client (1345 lines)
    ├── domain_hotspot_analyzer.py  # 🔥 Hotspot domain investment analysis (NEW)
    ├── domain_knowledge_rag.py     # 📚 Industry consulting RAG retrieval (NEW)
    ├── domain_promotion_search.py  # 💰 Promotion information retrieval
    ├── domain_monitor.py           # 🆕 Domain monitoring subscription (NEW)
    ├── safe_operation_example.py   # Safe operation example
    └── ...                         # Other scripts
```

## 🔧 Dependency Installation

```bash
# Install Alibaba Cloud SDK core and domain SDK
pip3 install aliyun-python-sdk-core aliyun-python-sdk-domain
```

## 📝 Example Output

### Domain List

```
🦐 Alibaba Cloud Domain List
============================================================
Domain                          Expiration Date          Status
------------------------------------------------------------
example.com                   2027-01-15        Normal
example.cn                    2026-06-20        Normal
example.net                   2026-04-01        Expiring Soon
------------------------------------------------------------
Total 3 domains
```

### Domain Details

```
🦐 Domain Details: example.com
============================================================
Domain Name: example.com
Registrar: Alibaba Cloud Computing Ltd.
Registration Date: 2020-01-15
Expiration Date: 2027-01-15
Domain Status: ok
DNS Servers: dns1.hichina.com, dns2.hichina.com
Registrant: [Name]
```

### Expiring Domains

```
🦐 Expiring Domains (within 30 days)
============================================================
⚠️  example.net                   2026-04-01        17 days remaining
⚠️  test.cn                       2026-03-25        11 days remaining
------------------------------------------------------------
Total 2 domains need renewal soon
```

## ⚠️ Notes

1. **API Call Limits**: Alibaba Cloud API has QPS limits, please avoid high-frequency calls
2. **Permission Requirements**: Need `AliyunDomainFullAccess` or custom permission policy
3. **Region Selection**: Domain API mainly uses `cn-hangzhou` region
4. **Fee Description**: Some API calls may incur fees (such as domain renewal, registration)
5. **Redemption Period**: After domain expires, it enters redemption period, renewal price will be higher (¥200-500)

## 🆘 Troubleshooting

### Issue: Invalid AccessKey

```
Error: InvalidAccessKeyId.NotFound
```

**Solution**: Check if AK/SK in credentials.json is correct, confirm RAM user is authorized.

### Issue: Insufficient Permissions

```
Error: Forbidden.Ram
```

**Solution**: Add `AliyunDomainFullAccess` permission policy for RAM user.

### Issue: API Call Failed

```
Error: SDK.Server.Unreachable
```

**Solution**: Check network connection, confirm can access api.aliyuncs.com.

### Issue: Error When Modifying DNS `MissingAliyunDns`

```
Error: HTTP Status: 400 Error:MissingAliyunDns
```

**Solution**: Ensure `set_AliyunDns(False)` parameter is set when calling.

```python
request.set_DomainNames(domain_name)
request.set_DomainNameServers(dns_servers)
request.set_AliyunDns(False)  # ✅ Required parameter
```

### Issue: Error When Modifying DNS `set_DomainList` Does Not Exist

```
AttributeError: 'SaveBatchTaskForModifyingDomainDnsRequest' object has no attribute 'set_DomainList'
```

**Solution**: Use correct parameter name.

```python
# ❌ Wrong
request.set_DomainList([...])

# ✅ Correct
request.set_DomainNames(domain_name)        # String
request.set_DomainNameServers(dns_servers)  # List
```

### Issue: `query_task_list()` Returns Empty List

**Symptom**: Even with tasks, wrapper method returns `[]`.

**Solution**: Use raw API call.

```python
from aliyunsdkdomain.request.v20180129.QueryTaskListRequest import QueryTaskListRequest

request = QueryTaskListRequest()
request.set_PageNum(1)
request.set_PageSize(100)

response = client.client.do_action_with_exception(request)
data = json.loads(response)
tasks = data['Data']['TaskInfo']  # ✅ Correct retrieval
```

### Issue: `query_registrant_profiles()` Returns Empty List

**Symptom**: Even with templates, wrapper method returns `[]`.

**Reason**:
1. API return path is `RegistrantProfiles.RegistrantProfile`, not `Data.RegistrantProfile`
2. `RegistrantProfile` may be object or array, need type judgment

**Solution**: Use raw API call.

```python
from aliyunsdkdomain.request.v20180129.QueryRegistrantProfilesRequest import QueryRegistrantProfilesRequest
import json

request = QueryRegistrantProfilesRequest()
request.set_PageNum(1)
request.set_PageSize(20)

response = client.client.do_action_with_exception(request)
result = json.loads(response)

# ✅ Correct parsing
profiles = result.get('RegistrantProfiles', {}).get('RegistrantProfile', [])

# ⚠️ Key: If single object, convert to array
if isinstance(profiles, dict):
    profiles = [profiles]

# Iterate results
for profile in profiles:
    template_id = profile.get('RegistrantProfileId')
    status = profile.get('RealNameStatus')  # ✅ Not AuditStatus
    print(f'{template_id}: {status}')
```

**Detailed Documentation**: [learnings/REGISTRANT_PROFILE_QUERY.md](learnings/REGISTRANT_PROFILE_QUERY.md)

---

## 📝 Quick Reference Table for Common Issues

For more detailed problem analysis and solutions, please refer to [📚 Lessons Learned Library](#-lessons-learned-library).

| ❌ Issue | ✅ Solution |
|:---|:---|
| `check_domain()` return field uses uppercase `Available` | Use lowercase `available` |
| `set_DomainList()` parameter does not exist | Use `set_DomainNames()` |
| `set_DnsName()` parameter does not exist | Use `set_DomainNameServers()` |
| Modify DNS error `MissingAliyunDns` | Set `set_AliyunDns(False)` |
| `query_task_list()` returns empty list | Use raw API call |
| Bulk query domains all show "registered" | Check API field case, test with random domain to verify |
| Domain lock error `InvalidStatus` | Status parameter use string `'true'` or `'false'` |
| Query task error `MissingPageNum` | Add `set_PageNum(1)` and `set_PageSize(10)` |
| `query_registrant_profiles()` returns empty list | Use raw API, path `RegistrantProfiles.RegistrantProfile` |
| Template status field `AuditStatus` does not exist | Use `RealNameStatus` |

---

## 🔒 Domain Lock Operation (Updated 2026-03-14)

### Transfer Lock & Update Lock API Parameters

**⚠️ Key: Status parameter must use string, not boolean!**

```python
# ✅ Correct
request.set_Status('true')   # Enable lock
request.set_Status('false')  # Disable lock

# ❌ Wrong
request.set_Status(True)           # Boolean will error
request.set_Status('OPEN')         # String OPEN will error
request.set_Status('Enable')       # String Enable will error
```

### Complete Code Example

```python
# Enable transfer lock
from aliyunsdkdomain.request.v20180129.SaveSingleTaskForTransferProhibitionLockRequest import SaveSingleTaskForTransferProhibitionLockRequest

request = SaveSingleTaskForTransferProhibitionLockRequest()
request.set_DomainName('example.xyz')
request.set_Status('true')  # ⚠️ Must be string "true"

response = client.client.do_action_with_exception(request)
result = json.loads(response)
task_no = result.get('TaskNo', '')

# Enable update lock
from aliyunsdkdomain.request.v20180129.SaveSingleTaskForUpdateProhibitionLockRequest import SaveSingleTaskForUpdateProhibitionLockRequest

request = SaveSingleTaskForUpdateProhibitionLockRequest()
request.set_DomainName('example.xyz')
request.set_Status('true')  # ⚠️ Must be string "true"
```

### Query Lock Status

```python
detail = client.query_domain_detail('example.xyz')

transfer_lock = detail.get('TransferProhibitionLock')  # OPEN / CLOSE
update_lock = detail.get('UpdateProhibitionLock')      # OPEN / CLOSE

print(f'Transfer Lock: {"🔒 Enabled" if transfer_lock == "OPEN" else "🔓 Disabled"}')
print(f'Update Lock: {"🔒 Enabled" if update_lock == "OPEN" else "🔓 Disabled"}')
```

**Detailed Documentation**: [learnings/DOMAIN_LOCK_OPERATION.md](learnings/DOMAIN_LOCK_OPERATION.md)

---



---

## 📚 Lessons Learned Library

For detailed API call experience, troubleshooting, and problem solutions, please refer to documents in the `learnings/` folder:

| Document | Content Description |
|:---|:---|
| [learnings/API_QUICK_REFERENCE.md](learnings/API_QUICK_REFERENCE.md) | API quick reference manual |
| [learnings/API_FIELD_CASE_ISSUE.md](learnings/API_FIELD_CASE_ISSUE.md) | API field case issue record |
| [learnings/DOMAIN_LOCK_OPERATION.md](learnings/DOMAIN_LOCK_OPERATION.md) | Domain lock operation guide |
| [learnings/REGISTRANT_PROFILE_QUERY.md](learnings/REGISTRANT_PROFILE_QUERY.md) | Real-name template query issue record |

**Quick Reference for Common Issues**:


| ❌ Error | ✅ Correct |
| -------------------------- | ----------------------------------------------- |
| `set_DomainList()` | `set_DomainNames()` + `set_DomainNameServers()` |
| `set_DnsName()` | `set_DomainNameServers()` |
| Missing `set_AliyunDns()` | Must set `set_AliyunDns(False)` |
| `query_task_list()` returns empty | Use raw API call |



## 📞 Support

- Alibaba Cloud Documentation: https://help.aliyun.com/product/35836.html
- API Reference: https://next.api.aliyun.com/api/Domain/2018-01-29
- 🔐 Safe Operation Guide: [SAFE_OPERATION_GUIDE.md](SAFE_OPERATION_GUIDE.md)

---

**Skill Version**: v2.0.0
**Last Updated**: 2026-03-19

**Security Rules**: ⚠️ All API calls involving orders and financial operations must be explicitly double confirmed by the user before execution!

**Changelog**:
- v2.0.0 (2026-03-19): 🎯 Built-in creative domain naming capability, complete workflow (project analysis → creative strategy → availability check → purchase link)
- v1.3.0 (2026-03-17): 📡 Domain monitoring subscription, supports expiration monitoring, WHOIS tracking, SSL certificate monitoring
- v1.2.0 (2026-03-16): 📚 RAG industry consulting, provides precise answers for domain/website building/filing based on local knowledge base
- v1.1.0 (2026-03-15): 📊 Domain asset assessment dashboard + hotspot domain investment analysis
- v1.0.0 (2026-03-14): 🚀 Alibaba Cloud domain management core features, supports query/renewal/transfer/registration/lock and other operations
