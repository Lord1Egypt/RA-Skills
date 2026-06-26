# Contractor Marketing Plugin

AI marketing department for contractors and home service businesses. Built by a contractor, not an agency.

Works with **Claude Cowork**, **Claude Code**, and **OpenClaw**.

## What it does

| Command | What it does |
|---------|-------------|
| `/contractor-marketing:onboard` | Sets up your business profile (run once) |
| `/contractor-marketing:gbp-post` | Generate + publish Google Business Profile posts |
| `/contractor-marketing:review-response` | Respond to customer reviews (batch supported) |
| `/contractor-marketing:social-batch` | Generate a week of social posts, schedule in Buffer |
| `/contractor-marketing:weekly-report` | SEO + ads performance report from your data |
| `/contractor-marketing:ad-creative` | Facebook, Instagram, and Google ad creatives |
| `/contractor-marketing:content-calendar` | Full month of content + 4 blog post drafts |
| `/contractor-marketing:competitor-audit` | Monthly competitor analysis |
| `/contractor-marketing:proposal` | Professional proposal from "Mike, 2 acres, $4,600" |
| `/contractor-marketing:job-cost` | Job profitability and margin tracking |
| `/contractor-marketing:email-sequence` | Automated email sequences for follow-up and retention |
| `/contractor-marketing:lead-followup` | Lead follow-up templates with timing |

## Background skills (loaded automatically)

Claude draws on these when relevant -- you don't need to invoke them:

- **contractor-seo** -- local SEO, citations, keywords, service area pages
- **contractor-ads** -- Meta/Google campaigns, budgets, creative angles
- **contractor-social** -- content strategy, platform rules, review responses
- **contractor-email** -- sequences, lead follow-up, newsletters, invoicing
- **contractor-operations** -- proposals, job costing, pricing, portfolios
- **contractor-positioning** -- UVP, messaging, competitive differentiation

## Includes: 74 proven strategies

Connected to the [Heavy Metric](https://heavymetric.com/strategies) strategy library via MCP. Claude automatically pulls relevant strategies when generating content, ads, or recommendations.

## Install

### Claude Cowork / Claude Code
```bash
claude plugin marketplace add blueprintstudioco/contractor-marketing
claude plugin install contractor-marketing
```

### OpenClaw
```bash
npx clawhub@latest install contractor-marketing
```

### Manual
Clone this repo and point Claude at it:
```bash
git clone https://github.com/blueprintstudioco/contractor-marketing.git
claude --plugin-dir ./contractor-marketing
```

## Set up scheduled tasks (Cowork)

After installing, set up these recurring tasks so Claude runs your marketing automatically:

| Task | Schedule | Command |
|------|----------|---------|
| GBP post + review check | Every Monday 7am | `/contractor-marketing:gbp-post` then check for new reviews |
| Social media batch | Every Sunday 6pm | `/contractor-marketing:social-batch` |
| Weekly performance report | Every Monday 8am | `/contractor-marketing:weekly-report` |
| Content calendar + blogs | 25th of each month | `/contractor-marketing:content-calendar` |
| Competitor audit | 15th of each month | `/contractor-marketing:competitor-audit` |

Use `/schedule` in Cowork to set these up, or just tell Claude: "Schedule a task to generate my GBP post every Monday at 7am."

## First time setup

1. Install the plugin
2. Run `/contractor-marketing:onboard` -- Claude asks 35 questions about your business
3. Save the generated `business-profile.md` file
4. Set up scheduled tasks (optional but recommended)
5. Start talking to Claude like it's your marketing employee

## Who this is for

Contractors and home service businesses: land clearing, landscaping, roofing, pressure washing, concrete, fencing, tree service, excavation, demolition, painting, HVAC, plumbing, electrical, and any trade that gets customers through local marketing.

## Who this is NOT for

SaaS companies, e-commerce, enterprise marketing teams. Use Anthropic's [official marketing plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/marketing) instead.

## Cost

The plugin is free. You need Claude Pro ($20/mo) or Claude Code to run it.

## Built by

[Heavy Metric](https://heavymetric.com) -- free marketing tools and strategies for contractors.

Built by a contractor who got tired of paying agencies.
