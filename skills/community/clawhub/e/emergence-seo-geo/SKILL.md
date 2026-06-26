---
slug: emergence-seo-geo
title: "Emergence SEO GEO: Generative Engine Optimization Auditor"
description: "Professional GEO/SEO website auditor skill evaluating LLM citation readiness, technical accessibility, and semantic authority."
version: 1.1.0
homepage: https://emergence.science/skills/emergence-seo-geo
---

# GEO/SEO Analysis & Audit Skill

This skill defines the technical methodology and analysis workflow for auditing websites against Generative Engine Optimization (GEO) and AI-native search engine (ChatGPT, Perplexity, Gemini, Claude, Copilot, Google AI Overviews) ranking behaviors.

---

## 🎯 Core Objective

Audit any target domain's visibility, technical crawlability, and semantic authority under conversational AI models, producing a standardized, high-value assessment report with actionable optimization roadmaps tailored to the type of web application (Agent-First vs. Human-First).

---

## 📊 Differentiated Scoring Scorecard (100 Points Total)

To cater to the distinct traversal paths of autonomous agents versus human-oriented conversational search, the audit uses a tailored metric weighting scheme:

| Metric | Max Points | Agent-First Heuristic | Human-First Heuristic |
|---|:---:|---|---|
| **1. Technical Accessibility** | 15 pts | - AI crawlers (`GPTBot`, `ClaudeBot`, `PerplexityBot`, etc.) permitted in `robots.txt`. | - Standard search engine crawlers (`Googlebot`, `Bingbot`, etc.) permitted in `robots.txt`. |
| **2. Structured Schema Quality** | 10 pts | - Validity of JSON-LD schemas mapped to agent capabilities or software specs. | - Presence and validity of schemas like `Product`, `FAQPage`, `Organization`, `HowTo`. |
| **3. Content Extractability** | 15 pts | - Section headings, markdown structures, bullet points, and data grids. | - Structured comparison layout, QA headers, H1/H2/H3 hierarchies. |
| **4. Answer Density (BLUF)** | 10 pts | - Concise summary blocks for machine ingestion. | - High-density 40-70 word answer blocks ("Bottom Line Up Front" formatting). |
| **5. Citations & Empirical Data** | 15 pts | - Hard data points, numeric parameters, and outbound documentation references. | - Specific numbers, percentages, trust factors, and reliable source linking. |
| **6. Expertise & Attribution (EEAT)** | 10 pts | - Developer/Publisher credentials, software repositories, and compliance/trust signals. | - Verified author credentials, profile bylines, customer review indicators. |
| **7. Off-Page Entity Footprint** | 15 pts | - Hyperlinked references in code repositories, developer registries, or package indexes. | - External citations on mainstream wikis, reddit homebrews, forum indices. |
| **8. Machine-Readable Discovery** | 10 pts | - Presence and compliance of `/llms.txt` and `/skill.md` at domain root. | - Presence of standard `/sitemap.xml` and OpenGraph/Twitter social meta tags. |

---

## 🛠️ Step-by-Step Auditing Workflow

### Step 1: Local & Automated Crawl Check
Run the automated python script `geo_audit.py` to calculate the baseline score and scan technical endpoints:
```bash
# Audit a B2B SaaS or E-commerce site (Human-first)
python3 geo_audit.py soldy.ai --type human --prompt "AI video generator"

# Audit an agent network app or dev protocol (Agent-first)
python3 geo_audit.py emergence.science --type agent --prompt "openclaw bounty market"
```

### Step 2: E2E Search Engine Indexation Verification (Optional)
To query live index footprints and rank tracking on Tavily, Brave Search, Google, and Bing, append the `--e2e` flag:
```bash
# Requires local CLI tools: `bx` (Brave Search) and `tvly` (Tavily Search)
python3 geo_audit.py emergence.science --type agent --prompt "openclaw bounty market" --e2e
```

### Step 3: Content Optimization Scan
1. Review target landing pages to check if answers are buried in non-indexable structures (dynamic client-side React code, login walls).
2. Count word length of key introductory paragraphs to check if they fit the 40-70 word extraction window.

### Step 4: Sourcing & EEAT Validation
Verify if claims rely on subjective marketing adjectives instead of verifiable scientific and quantitative facts.

---

## 📋 Standard Reporting Structure & Examples

Every generated report must include:
1. **Executive Summary**: Core highlights and final benchmark score.
2. **Current State Assessment**: Breakdown of the 8 metrics with specific website screenshots or parsed snippets.
3. **Competitor Citation Gap Analysis**: Why competitors get cited in ChatGPT/Perplexity for target keywords while the client is omitted.
4. **Actionable Roadmap**: Clear 30-60-90 day recommendations (Technical fixes, structural copy rewrite, schema implementation, agentic files integration).

### Live Example & Downloadable Report
- **Live Interactive Tool & Report Demo**: Visit [Emergence Science SEO-GEO Audit Tool](https://emergence.science/en/tools/seo-geo) to view live report examples and score calculations.
- **Reference Document**: An example of a generated English audit report is bundled with this skill at [examples/emergence_science_analysis_en.md](file:///Users/julian/operators/emergence_oracle/skills/emergence-seo-geo/examples/emergence_science_analysis_en.md) for direct reference and templates.
