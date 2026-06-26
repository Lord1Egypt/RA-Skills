# GEO.SKILL - Generative Engine Optimization Skill

> 🚀 **Let AI understand and trust your park**

简体中文 | [English](./README.md)

---

## 📖 Table of Contents

- [Introduction](#introduction)
- [Quick Start](#quick-start)
- [Skill Structure](#skill-structure)
- [Usage Guide](#usage-guide)
- [Templates](#templates)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [FAQ](#faq)

---

## Introduction

### What is GEO

**GEO (Generative Engine Optimization)** is a set of optimization technologies that help AI systems (such as DeepSeek, Doubao, Kimi, etc.) accurately understand, trust, and prioritize your content.

### Why Parks Need GEO.SKILL

```
┌────────────────────────────────────────────────────────────────┐
│                   AI Search vs Traditional Search               │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Traditional (Google/Baidu)      AI Search (DeepSeek/豆包)      │
│  ┌─────────────────┐            ┌─────────────────┐           │
│  │ Returns 10 links │            │ Direct answers   │           │
│  │ User judges      │     →      │ AI integrates    │           │
│  │ Need to click   │            │ Traceable source │           │
│  └─────────────────┘            └─────────────────┘           │
│                                                                 │
│  Challenges for parks:                                           │
│  • Park info may be missing in AI search                        │
│  • Website lacks structured data, hard for AI to parse          │
│  • Content fragmented, can't form trusted answers               │
│  • Competitor parks have higher AI visibility                  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### What GEO.SKILL Can Do

| Module | Description |
|--------|-------------|
| 🏗️ Infrastructure | llms.txt deployment, Schema structured data, Trusted source matrix |
| 📝 Content | Question graph generation, Inverted pyramid writing, Multi-modal content |
| 🛠️ Tools | Diagnostic tools, Content distribution, Monitoring |
| 📈 Operations | T+7 verification, Negative repair, Data closed loop |

---

## Quick Start

### Step 1: Prepare Park Information

Prepare the following information:

```yaml
Required:
  - Official park name
  - Short name/alias
  - Detailed address
  - Phone number
  - Email
  - Website URL
  
Optional:
  - Industry positioning
  - Core advantages
  - Product types
  - Price range
  - Preferential policies
```

### Step 2: Generate llms.txt

1. Open `templates/llms.txt` template
2. Fill in park information
3. Upload to website root directory
4. Verify at `https://yourpark.com/llms.txt`

### Step 3: Deploy Schema

1. Choose Schema type:
   - **Organization** - Park basic info
   - **Product** - Factory/office product
   - **Event** - Investment event

2. Find template in `templates/schema/`
3. Fill in JSON-LD parameters
4. Add code to page `<head>` section

### Step 4: Produce Content

1. Use **Question Graph Generator** to create core question list
2. Use **Inverted Pyramid Writing Template** to produce content
3. Add tables, lists, and other structured elements
4. Distribute across platforms

### Step 5: Start Monitoring

1. Configure core monitoring keywords
2. Set up weekly/monthly monitoring reports
3. Establish issue resolution process

---

## Skill Structure

```
geo-skill/
├── SKILL.md                      # Complete skill definition
├── README.md                     # User guide
├── README_EN.md                  # English user guide
├── clawhub.yaml                  # Publish configuration
│
├── templates/                    # Template directory
│   ├── llms.txt                  # llms.txt template
│   ├── schema/                   # Schema templates
│   │   ├── organization.json     # Organization Schema
│   │   ├── product.json          # Product Schema
│   │   └── event.json           # Event Schema
│   ├── content/                  # Content templates
│   │   ├── question_graph.md     # Question graph
│   │   └── pyramid_writing.md    # Inverted pyramid writing
│   └── monitoring/               # Monitoring templates
│       └── report_template.md    # Report template
│
├── examples/                     # Example directory
│   ├── park_example/             # Complete park example
│   │   ├── llms.txt
│   │   └── schema/
│   └── content_example/         # Content example
│       └── articles/
│
└── scripts/                      # Script directory
    ├── generator.py              # llms.txt generator
    ├── diagnostic.py             # Diagnostic tool
    └── monitor.py               # Monitoring tool
```

---

## Usage Guide

### Template Usage

#### llms.txt Template

```markdown
# [Park Name]

## About Us
[Park positioning, core industries, geographical advantages]

## Core Industries
- [Industry 1]
- [Industry 2]
- [Industry 3]

## Product Types
- Detached office building
- Standard factory
- Customized space

## Contact Information
- Address: [Detailed address]
- Phone: [Phone number]
- Email: [Email]
- Website: [URL]

## Latest News
[Important updates in recent 3 months]

## Data Summary
- Land area: [X] mu
- Companies: [X]
- Annual output: [X] billion yuan
```

### Script Usage

#### llms.txt Generator

```bash
python scripts/generator.py --config park_config.json --output llms.txt
```

#### Diagnostic Tool

```bash
python scripts/diagnostic.py --url https://yourpark.com --output report.md
```

#### Monitoring Tool

```bash
python scripts/monitor.py --config geo_monitor_config.json --output report.md
```

---

## Examples

### Complete Park Example

See `examples/park_example/`:

```
examples/park_example/
├── llms.txt                           # Complete llms.txt example
└── schema/
    ├── organization.json             # Park organization info
    ├── product_building_a.json       # A-building product
    ├── product_building_b.json       # B-building product
    └── event_2025_q1.json           # 2025Q1 investment event
```

### Content Example

See `examples/content_example/`:

```
examples/content_example/
└── articles/
    ├── rent_guide.md                  # Rent guide
    ├── policy_faq.md                 # Policy FAQ
    └── company_interview.md          # Company interview
```

---

## Best Practices

### ✅ Recommended

| Practice | Description |
|----------|-------------|
| Regular updates | Update llms.txt monthly |
| Precise data | Use exact numbers, avoid "approximately" |
| Consistency | Keep contact info consistent across platforms |
| Answer first | Put core answer at the beginning |
| Proactive distribution | Answer questions on Zhihu actively |
| Continuous monitoring | Establish weekly/monthly monitoring |

### ❌ Avoid

| Practice | Description |
|----------|-------------|
| Outdated info | Avoid using expired prices and policies |
| Vague descriptions | Avoid empty phrases like "beautiful environment" |
| Subjective comparison | Avoid subjective comparisons with other parks |
| Conflicting info | Avoid publishing different info on multiple platforms |
| Ignoring feedback | Don't ignore user questions |

### Key Metrics

| Metric | Target | Frequency |
|--------|--------|-----------|
| AI citation rate | >80% | Weekly |
| Info accuracy rate | >95% | Monthly |
| Top 3 ranking rate | >60% | Weekly |
| Content coverage | >90% | Quarterly |

---

## FAQ

### Q1: What's the difference between llms.txt and robots.txt?

| Comparison | robots.txt | llms.txt |
|------------|------------|----------|
| Target user | Search engine crawlers | AI systems |
| Content | Crawling rules | Content summary |
| Location | Website root | Website root |
| Format | TXT | Markdown |

### Q2: Do I need to deploy both Schema and llms.txt?

Yes, both are recommended for best results:
- **llms.txt** provides overall overview, suitable for AI quick understanding
- **Schema** provides structured data, suitable for precise information extraction

### Q3: How often should I update content?

| Content Type | Update Frequency |
|--------------|------------------|
| llms.txt | Monthly |
| Schema products | As changed |
| Investment articles | Weekly |
| Event info | 2 weeks before event |
| Policy explanations | Within 1 week of policy release |

### Q4: How to verify GEO effectiveness?

1. Search core keywords on DeepSeek/Doubao/Kimi
2. Check if park info appears
3. Verify info accuracy
4. Track ranking changes

### Q5: How to handle negative information?

1. Assess issue severity
2. Develop fix plan
3. Update llms.txt and content
4. Publish positive content
5. Continuous monitoring

---

## Getting Help

- 📖 See [SKILL.md](./SKILL.md) for complete documentation
- 🐛 Report issues: [GitHub Issues](https://github.com/openclaw/geo-skill/issues)
- 📧 Contact: support@openclaw.ai

---

## License

MIT-0 License - Free to use, modify, and distribute without attribution.

---

*© 2025 OpenClaw AI Team*
