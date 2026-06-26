# Amazon Category Research Skill

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-orange)

> [中文](README.md) | **English**

> 🤖 **OpenClaw Agent Skill** — Turn Amazon category research from "a full day" into "10 minutes". Auto-collect data, auto-generate Feishu reports.

***

## Table of Contents

- [💥 Why Install?](#-why-install)
- [⚡ One-Click Install & Use](#-one-click-install--use)
- [🤖 Agent Execution Standard (Agent Required Reading)](#-agent-execution-standard-agent-required-reading)
  - [1. Installation Flow (Upon Install Request)](#1-installation-flow-upon-install-request)
  - [2. Research Flow (Upon Research Request)](#2-research-flow-upon-research-request)
  - [3. Browser Operation Constraints](#3-browser-operation-constraints)
  - [4. Configuration Checklist](#4-configuration-checklist)
  - [5. Error Handling](#5-error-handling)
- [🎯 Research Capabilities](#-research-capabilities)
- [📊 Report Content](#-report-content)
- [📁 Project Structure](#-project-structure)
- [⚠️ Requirements](#-requirements)
- [📄 License](#-license)

***

## 💥 Why Install?

**Manual category research → at least 1 day. With this Skill → 10 minutes.**

| Your Pain                                    | After Installing                               |
| -------------------------------------------- | ---------------------------------------------- |
| Copy-pasting SellerSprite / SIF data by hand | Agent auto-collects, 6s per ASIN               |
| Data scattered across platforms              | Multi-source data merged into one table        |
| Manual report writing, messy formatting      | Auto-generated Feishu doc, professional layout |
| Missing data after a full day of research    | Systematic collection with auto-validation     |

***

## 🎬 Demo

> Tested with **GLM-5.1** — a full round (20 ASINs) takes about **5 minutes**. May be longer under network congestion or LLM latency.

| Stage | Screenshot |
| :--- | :--- |
| 🚀 **Start** — Send keywords/ASINs, Agent kicks off collection | ![Start](Demo/start.png) |
| ⏳ **In Progress** — Collecting SellerSprite + SIF data per ASIN | ![Progress 1](Demo/progress1.png) |
| ⏳ **In Progress** — Data validation & auto-correction | ![Progress 2](Demo/progress2.png) |
| ✅ **Done** — Feishu research report generated, link returned | ![Done](Demo/end.png) |

***

## ⚡ One-Click Install & Use

### Install (One Time Only)

Simply tell the Agent (OpenClaw user):

```text
Install the Amazon Category Research Skill: clawhub install amz-cat-research
```

The Agent will sequentially:

1. `clawhub install amz-cat-research` → install from ClawHub
2. Reload to load SKILL.md
3. Launch browser → execute `scripts/init.py check` → detect SellerSprite and SIF plugin status
4. Based on the check results, automatically guide you to install/log in to plugins
5. Reply "Ready to research" once everything is set

> ⚠️ The first installation will automatically run init.py for configuration check. **For subsequent use, the Agent skips the check and goes directly to data collection.**

### Use (Daily)

After installation, simply send a research request to the Agent:

```text
Research the camping lantern category, site US
```

Or provide an ASIN list:

```text
Category: outdoor camping lantern | Keywords: camping lantern
ASINs: B07VGRJDFY, B08N5WRWNW, B09G9HD6YF | Site: US
```

The Agent will auto-collect → validate → generate Feishu cloud doc → reply with the link. **Takes only 10 minutes.**

***

## 🤖 Agent Execution Standard (Agent Required Reading)

> The following content is for the Agent only. Upon receiving a user request, the Agent MUST strictly follow this standard.

### 1. Installation Flow (Upon Install Request)

```
Step 1 — Repository Deployment
  ├─ git clone → skill directory
  ├─ Reload to load Skill
  └─ Confirm SKILL.md is loaded

Step 2 — Initialization Config Check (init.py)
  ├─ browser navigate → Amazon test product page (e.g., /dp/B0CC27124P?th=1)
  ├─ Wait 5 seconds
  ├─ python3 scripts/init.py check → generate check JS
  ├─ browser act(kind="evaluate", fn=checkJS) → get results
  ├─ python3 scripts/init.py report '<json>' → generate report
  └─ Reply to user based on branching logic
```

**Branching Logic:**

| Status      | Meaning                                       | Agent Action                                         |
| ----------- | --------------------------------------------- | ---------------------------------------------------- |
| **ready**   | Browser OK, all plugins installed & logged in | ✅ Reply ready message, prompt user to start research |
| **partial** | Plugins installed but not logged in           | ⚠️ Reply partial message, guide user to log in       |
| **blocked** | Missing required plugins                      | ❌ Reply blocked message, provide installation steps  |

**Guidance Scripts:**

<details>
<summary>Status = ready</summary>

```
✅ Amazon Category Research Skill installed successfully!

All configuration checks passed:
- Chrome Browser: Ready
- SellerSprite Plugin: Installed ✅ Logged In ✅
- SIF Plugin: Installed ✅ Logged In ✅

You can now start using it. For example:
"Research the camping lantern category, site US"
```

</details>

<details>
<summary>Status = partial (SellerSprite not logged in as example)</summary>

```
⚠️ Skill installed, but configuration is not fully ready.

Check Results:
- SellerSprite Plugin: Installed ✅ Not Logged In ❌
- SIF Plugin: Installed ✅ Logged In ✅

Please log in to your SellerSprite account in the browser, then reply "continue".
You can also reply "skip" to proceed (some fields will be missing).
```

</details>

<details>
<summary>Status = blocked (SellerSprite not installed as example)</summary>

```
❌ Skill installed, but required plugins are missing.

Check Results:
- SellerSprite Plugin: Not Installed ❌

Please follow these steps:
1. Visit https://www.sellersprite.com/ to download the plugin
2. Install it in Chrome browser (OpenClaw profile)
3. Log in to your SellerSprite account
4. Reply "continue" to re-run the check
```

</details>

### 2. Research Flow (Upon Research Request)

Fully aligned with the [SKILL.md](SKILL.md) "Execution Steps" section:

```
Step 0 ─ Feishu Authorization Check (Mandatory)
  ├─ Check the current user's Feishu OAuth authorization status
  ├─ If incomplete → feishu_oauth_batch_auth for one-time full authorization
  └─ Must create documents with user identity, NOT bot identity

Step 1 ─ Parse Input + Determine ASIN List
  ├─ Scenario A: User provides ASINs directly → validate format, proceed to Step 3
  ├─ Scenario B: User provides keywords only → navigate search results page → evaluate to extract ASINs
  ├─ Scenario C: User provides category name only → navigate BSR page → evaluate to extract ASINs
  └─ Max 20 ASINs, inform user of the collection scope once confirmed

Step 2 ─ Confirm Browser Availability
  ├─ browser status → confirm openclaw profile is available
  ├─ If abnormal → browser start to re-take control
  └─ Triple verification: tabs → navigate → snapshot

Step 3 ─ Generate Extraction JS
  ├─ python3 scripts/run_all.py generate → merged collection JS
  └─ JS is in IIFE format (() => { ... })()

Step 4 ─ Collect Data Per ASIN
  ├─ browser navigate → product detail page (?th=1)
  ├─ Wait 6 seconds (anti-bot + plugin injection)
  ├─ browser act(kind="evaluate", fn=collectionJS)
  ├─ python3 scripts/parse_raw.py all '<json>' → parse
  ├─ python3 scripts/validate.py '<parsedJSON>' → validate
  ├─ If validation reports missing → proceed to Step 5 self-healing
  └─ Pause 20 seconds every 2-3 ASINs

Step 5 ─ Self-Healing Flow (Conditional)
  ├─ python3 scripts/healer.py diagnose '<missing_ids>'
  ├─ browser act(kind="evaluate", fn=diagnosisJS)
  ├─ python3 scripts/healer.py propose '<diagnosis_result>'
  └─ After confirmation: python3 scripts/healer.py apply <field_id> <new_selector>

Step 6 ─ Generate Feishu Document
  ├─ Aggregate all ASINs → assemble Markdown content
  ├─ Save MD source file to workspace (authoritative backup)
  ├─ feishu_create_doc to create cloud document
  └─ Title format: Amazon Category Research｜{Keywords}｜{YYYY-MM-DD}

Step 7 ─ Reply to User
  ├─ DM only: document link + summary within 200 characters
  └─ Do NOT send full report content in DM
```

### 3. Browser Operation Constraints

| Constraint     | Detail                                                                    |
| -------------- | ------------------------------------------------------------------------- |
| **profile**    | MUST use `profile=openclaw`, NOT `profile=user`                           |
| **ports**      | Do NOT connect to 9222 / 9229 directly                                    |
| **web\_fetch** | Do NOT use `web_fetch` on Amazon pages                                    |
| **execution**  | JS runs via `browser act(kind="evaluate", fn=js)`                         |
| **scripts**    | Local Python scripts only generate JS / parse data, do NOT launch browser |

### 4. Configuration Checklist

| # | Item                   | How to Check                            | Success Criteria           |
| - | ---------------------- | --------------------------------------- | -------------------------- |
| 1 | Chrome browser         | `browser navigate`                      | Page loads successfully    |
| 2 | SellerSprite plugin    | Execute JS generated by `init.py check` | `spirit_installed == true` |
| 3 | SellerSprite logged in | Execute JS generated by `init.py check` | `spirit_logged_in == true` |
| 4 | SIF plugin             | Execute JS generated by `init.py check` | `sif_installed == true`    |
| 5 | SIF logged in          | Execute JS generated by `init.py check` | `sif_logged_in == true`    |
| 6 | Feishu configuration   | Check Feishu Token availability         | Can create documents       |

### 5. Error Handling

| Exception               | Strategy                                                              |
| ----------------------- | --------------------------------------------------------------------- |
| Anti-bot page           | Wait 15s, refresh once, if still fails mark as anti-bot               |
| navigate timeout        | Check tabs for reuse, retry once, if still fails mark as load failure |
| evaluate returns empty  | Check targetId, use snapshot(compact=true) for cross-check            |
| Field extraction failed | Record "Not Retrieved / Needs Manual Review" + source method          |
| Plugin not loaded       | Mark "Requires SellerSprite/SIF Plugin"                               |
| Browser control chain exception | browser start to restart, if still fails → stop, output partial |
| Selector failure | healer.py self-healing |

***

## 🎯 Research Capabilities

### Five Research Dimensions

| Dimension              | Data Collected                                                               | Source                 |
| ---------------------- | ---------------------------------------------------------------------------- | ---------------------- |
| **Product Info**       | Title, Price, Rating, Reviews, Brand, Seller, Variants, Promotions           | Amazon Frontend        |
| **SellerSprite**       | 30-day Sales (Parent/Child), FBA Fee, Margin, Listing Date, BSR              | SellerSprite Extension |
| **SIF**                | Total Keywords, Organic/Ad Traffic, SP/SB/SBV/AC Ad Analysis, Monthly Trends | SIF Extension          |
| **Competitor Power**   | Brand Matrix, Store Count, Seller Location, Product Lines, Trademarks        | Amazon + Trademarkia   |
| **Operation Strategy** | Regular/Deal/Lowest Price, Sales Trends, Launch Process Analysis             | SIF + SellerSprite     |

### Data Reliability

- ✅ **Trusted Source**: Data directly from SellerSprite and SIF official extensions, identical to plugin interface
- ✅ **Real-time**: Fetched live from Amazon frontend for high freshness
- ✅ **Multi-layer Validation**: Auto-detect completeness and anomalies
- ✅ **Verifiable**: Critical data supports manual secondary verification

***

## 📊 Report Content

After research completes, a Feishu cloud document is auto-generated (with local Markdown backup):

| Module                     | Content                                                               |
| -------------------------- | --------------------------------------------------------------------- |
| 📋 **Input Summary**       | Category Name, Keywords, ASIN List, Collection Time                   |
| ✅ **Data Completeness**    | Collected / Needs Review / Missing field statistics                   |
| 📦 **Product Info**        | ASIN, Main Image, Title, Brand, Price, Rating, Reviews, Variants, BSR |
| 🏢 **Competitor Power**    | Brand Matrix, Store Count, Seller Location Assessment                 |
| 🔍 **Traffic Structure**   | Organic/Ad Traffic, Keyword Distribution, Ad Trends                   |
| 📈 **Operation Strategy**  | Price History, Sales Trends, Launch Process Review                    |
| 🎯 **Category Evaluation** | Recommended Strategy, Launch Tips, Risks, Timeline, Extensions        |

> 💡 Feishu docs support team collaboration, comments, version history — far better than Excel.

***

## 📁 Project Structure

```
amazon-category-research/
├── scripts/                 # Core scripts (10 files)
│   ├── init.py              # Agent init & config check
│   ├── run_all.py           # Collection orchestrator
│   ├── selector_registry.py # DOM selector registry
│   ├── gen_product.py       # Product fields JS generator
│   ├── gen_spirit.py        # SellerSprite fields JS generator
│   ├── gen_sif.py           # SIF fields JS generator
│   ├── gen_variants.py      # Variant fields JS generator
│   ├── gen_bsr.py           # BSR fields JS generator
│   ├── parse_raw.py         # Raw plugin data parser
│   ├── validate.py          # Data validator
│   └── healer.py            # Self-healing diagnosis
├── references/              # Reference docs
├── SKILL.md                 # OpenClaw Skill definition
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md                # Chinese docs
└── README.en.md             # English docs (this file)
```

***

## ⚠️ Requirements

| Item         | Requirement                   | Note                                                    |
| ------------ | ----------------------------- | ------------------------------------------------------- |
| Framework    | **OpenClaw Framework**        | Required, provides browser control                      |
| Browser      | Chrome `profile=openclaw`     | Auto-launched by Agent                                  |
| SellerSprite | Browser extension + logged in | Provides sales / FBA fee data                           |
| SIF          | Browser extension + logged in | Provides traffic / ad analysis data                     |
| Feishu       | Feishu account                | Strongly recommended, generates professional cloud docs |
| Python       | 3.8+                          | Local scripts only (JS generation / data parsing)       |

***

## 📄 License

MIT License — see [LICENSE](LICENSE).

***

## 🔗 Related Links

- [ClawHub Skill Page](https://clawhub.ai/yuancheng888/amz-cat-research)
- [OpenClaw Framework](https://github.com/openclaw)
- [SellerSprite](https://www.sellersprite.com/)
- [SIF](https://www.sif.com/)

***

*Built for Amazon Sellers — Give your time back to strategy, let the Agent handle the data.*

*Disclaimer: This project is for learning and reference purposes only.*
