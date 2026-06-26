# Auto-Claw — Autonomous WordPress Operations Agent

## What is This?

**Auto-Claw** is an autonomous AI agent that manages WordPress sites 24/7. It doesn't just monitor — it executes fixes, runs A/B tests, and optimizes continuously.

## Features (19 Capabilities)

### AI-Native Site Operations
- **SEO Scanner & Fixer** — 40+ point audit, WP-CLI fixes, Schema.org injection
- **Performance Diagnostic** — Core Web Vitals, TTFB, cache analysis
- **Content Auditor** — E-E-A-T scoring, readability analysis
- **Image Optimizer** — Compression analysis, lazy loading checks

### Conversion Flywheel
- **A/B Testing Engine** — Bayesian significance, multi-variant
- **Exit Intent Popup** — Geo-targeted intervention
- **Journey Personalizer** — Segment-based content
- **Smart Landing Pages** — High-conversion page generator
- **Dynamic FAQ** — Schema.org FAQPage generator

### Global Operations Center
- **GEO Targeting** — IP-based dynamic pricing/content
- **Competitor Monitor** — Price/content change alerts
- **Campaign Switcher** — Black Friday/618/双11 auto-activation
- **AI Content Generator** — E-E-A-T optimized blog posts

### Security Architecture
- **Vault** — Credentials never touch AI context
- **Gate Pipeline** — Destructive actions require approval
- **Soft Deletes** — Everything recoverable
- **Full Audit Log** — JSONL trail

## Requirements

- WordPress 5.8+ (self-hosted)
- PHP 7.4+ / 8.x
- WP-CLI installed
- SSH access (optional, for full capabilities)
- Redis (optional, for object caching)

## Installation

```bash
# Clone the project
git clone http://github.com/YOUR_ORG/auto-company
cd auto-company/projects/auto-claw

# Run full site audit
python3 cli.py full-audit --url http://yoursite.com --web-root /var/www/html

# Start autonomous monitoring
python3 cli.py monitor --continuous
```

## Quick Demo

```bash
# 19 capabilities demo (2 minutes)
python3 demo_complete.py

# Single capability
python3 cli.py seo
python3 cli.py performance
python3 cli.py ab-test
python3 cli.py competitor
```

## Live Example

Real WordPress site running Auto-Claw:
- URL: http://linghangyuan1234.dpdns.org
- SEO Score: 85/100
- Performance: 64/100
- A/B Tests: 1 active
- Competitor Monitor: 3 competitors tracked

## Pricing

| Plan | Price | Includes |
|------|-------|----------|
| Starter | $500/mo | SEO + Performance + Daily Audits |
| Growth | $1,000/mo | + A/B Testing + Competitor + GEO |
| Enterprise | $2,000/mo | All 19 capabilities + AI Content |

**Beta: Free for first 10 D2C brands.**

## Files

```
auto-claw/
├── cli.py              # Unified CLI (19 commands)
├── demo_complete.py    # All 19 capabilities demo
├── status.sh           # Quick status check
├── dashboard.html      # Visual dashboard
├── README.md          # Full documentation
├── QUICKREF.md       # CLI quick reference
├── src/
│   ├── seo.py
│   ├── performance_diag.py
│   ├── ab_tester.py
│   ├── competitor_monitor.py
│   ├── geo_targeting.py
│   ├── cache_optimizer.py
│   └── ...
└── docs/
    ├── hn-launch-draft.md    # Launch story
    ├── gtm-outreach-templates.md  # Sales templates
    └── one-pager.md         # Investor one-pager
```

## Security

- Credentials stored in Vault, never exposed to AI
- Destructive actions (delete, core updates) require human approval
- Full JSONL audit trail
- Soft deletes — nothing is permanently removed

## Use Cases

1. **D2C Brands** — Automate SEO, run A/B tests, monitor competitors
2. **WP Agencies** — Manage multiple client sites autonomously
3. **Solo Founders** — Get a "24/7 employee" for WordPress ops

## Support

- GitHub Issues: Report bugs, request features
- Beta Application: http://yoursite.com/auto-claw-beta-application/
