---
name: aka-seo-wireframe
description: Generate 200+ page authority site content using the Authority-Knowledge-Answer (AKA) framework. Produces structured content, internal linking maps, and SEO metadata for any platform — WordPress, Webflow, Shopify, static sites, headless CMS, or anywhere. WordPress deployment is one optional export, not a requirement. Use when the user wants topical authority content, content hubs, pillar pages, programmatic SEO, or mentions "AKA framework", "authority site", "content wireframe", "200 page site", or "topical clustering".

credentials:
  - name: ANTHROPIC_API_KEY
    description: >
      Used for content generation (strategy, pages, internal linking) via claude-opus-4.
      Uses your agent's existing Anthropic API key — no separate key needed if already configured.
      Cost: ~$2–8 per hub, billed to your Anthropic account.
    required: true
    env: ANTHROPIC_API_KEY
  - name: WP_URL
    description: >
      OPTIONAL. Your WordPress site URL (e.g. https://example.com).
      Only needed if using the WordPress deploy step (Step 5).
      Steps 1–4 produce platform-agnostic output and require no WP credentials.
    required: false
    env: WP_URL
  - name: WP_USER
    description: >
      OPTIONAL. WordPress username for REST API access.
      Only needed for WordPress deploy step. Use a dedicated Editor-role account, not your main admin.
    required: false
    env: WP_USER
  - name: WP_PASS
    description: >
      OPTIONAL. WordPress Application Password (not your login password).
      Generate at: WP Admin → Users → Profile → Application Passwords → Add New.
      Only needed for WordPress deploy step. Revoke after use.
    required: false
    env: WP_PASS
---

# AKA SEO Wireframe

**A content architecture framework — not a WordPress tool.**

Generate 200+ pages of structured, SEO-optimized authority content using the Authority-Knowledge-Answer (AKA) framework. Output is platform-agnostic markdown and JSON — use it on WordPress, Webflow, Shopify, Next.js, Ghost, any headless CMS, or anywhere else.

WordPress deployment is one optional step. The core value is the content itself.

**Generate in 1-2 hours what typically takes 4-6 weeks manually.**

## Security & Safety Summary

| Question | Answer |
|----------|--------|
| Core workflow credentials | Anthropic API key only (uses your existing agent config) |
| WordPress credentials | Optional — only needed if you choose the WP deploy step |
| LLM used | claude-opus-4 (Anthropic) |
| API cost | ~$2–8 per hub, billed to your Anthropic account |
| Output format | Platform-agnostic markdown + JSON |
| Content review required? | Yes — review AI content before publishing |
| WordPress deploy safe? | Use --dry-run first; use staging before production |
| Theme included? | Yes — optional, all 8 PHP files in assets/aka-framework-theme.zip |

## The AKA Framework

```
Authority Pages (5-7 hubs)
├── 4,000 words, comprehensive guides
├── Head keywords, hub for all related content
│
├── Knowledge Pages (12-15 per hub)
│   ├── 2,000 words, deep-dive content
│   ├── Mid-tail keywords
│   └── Specific topics and solutions
│
└── Answer Pages (20-30 per hub)
    ├── 1,000 words, FAQ format
    ├── Long-tail questions
    └── Featured snippet optimized
```

## Output Per Hub (~20 minutes)
- 1 Authority page (4,000 words)
- 15 Knowledge pages (30,000 words)
- 25 Answer pages (25,000 words)
- 300+ internal links
- Complete SEO optimization

## Full Site (5 hubs, 1-2 hours)
- 5 Authority hubs
- 75 Knowledge pages
- 125 Answer pages
- **205 total pages**
- 1,500+ internal links

## Quick Start Workflow

### Step 1: Setup (5 min)
Collect 15 business variables:
1. Business name, industry, location, service radius
2. Primary + secondary services (→ Authority Hubs)
3. Target audience, pain points, brand voice, UVP
4. Contact info, hours, trust signals

Save to: `.factory/config/aka-wireframe/business-config.json`

### Step 2: Generate Strategy (2 min)
Create complete AKA wireframe with hub topics, URL structure, keyword mapping.
Save to: `.factory/config/aka-wireframe/aka-strategy-output.json`

### Step 3: Generate Content (8 min/hub)
Create all pages with variable injection. Placeholders used for internal links.
Save to: `generated-content/hub-N/`

### Step 4: Process Internal Links (2 min/hub)
Convert `[LINK:slug|anchor]` placeholders → real URLs. Add AI contextual links. Validate no orphans.

### Step 5: Export / Deploy (3 min/hub)
Output is markdown + JSON — import it anywhere:
- **WordPress**: REST API deploy (requires WP credentials, use `--dry-run` first)
- **Webflow / Shopify / Ghost**: Import via CSV or CMS API
- **Static sites / Next.js**: Use generated markdown files directly
- **Manual**: Copy-paste or hand off to a developer

## Reference Files

| Reference | When to Load |
|-----------|--------------|
| `references/orchestrator.md` | Coordinating full workflow |
| `references/strategy-planner.md` | Generating AKA strategy |
| `references/content-generator.md` | Creating page content |
| `references/internal-linker.md` | Processing links |
| `references/wordpress-deployer.md` | Deploying to WordPress |
| `references/seo-optimizer.md` | SEO auditing |

## Created By

**Rabih Rizk** — [rabihrizk.com](https://rabihrizk.com)
AI strategy, SaaS, and digital marketing systems.

Built with [Blockstorm.ai](https://blockstorm.ai) — AI-powered content and SEO automation.

## Learn More

- 📖 **Full breakdown**: [rabihrizk.com/aka-seo-wireframe](https://rabihrizk.com/aka-seo-wireframe)
- 💼 **LinkedIn post**: [What is the AKA SEO Wireframe?](https://www.linkedin.com/posts/robrizk_but-what-exactly-is-the-aka-seo-wireframe-activity-7363984056327229440-6Xyo)

---

## Industry Applications

Works for any vertical (see warnings for regulated industries):
- **Home Services**: HVAC, plumbing, roofing, landscaping
- **Professional Services**: Consulting, real estate, agencies
- **E-commerce**: Product category sites, local directories
- **Law / Medical / Financial**: Supported but requires professional content review before publishing

## WordPress Setup

1. Create a dedicated WordPress user with **Editor** role
2. Go to WP Admin → Users → Profile → Application Passwords → Add New
3. Copy the generated password → set as `WP_PASS`
4. Set `WP_URL` and `WP_USER` in your environment
5. After deployment, revoke the Application Password

## Theme (Optional)

The included theme (`assets/aka-framework-theme.zip`) contains:
- `style.css` — Theme stylesheet with AKA layout
- `functions.php` — Theme functions and template support
- `header.php` / `footer.php` — Site chrome
- `index.php` — Default template
- `page-authority-hub.php` — Authority Hub template
- `page-knowledge.php` — Knowledge page template
- `page-answer.php` — Answer page template

Install via WP Admin → Appearance → Themes → Upload Theme, or use `--skip-theme` with any existing theme.
