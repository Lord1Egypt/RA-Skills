# Auto-Claw: WordPress AI Operations Platform

> **Your 24/7 AI team member for WordPress** — SEO, content, performance, and growth automation.

## What is Auto-Claw?

Auto-Claw is an autonomous WordPress operations agent built on OpenClaw. It directly modifies source files to implement, optimize, and maintain your WordPress site — without human intervention.

**The core advantage: closed-loop.** Most tools can monitor, alert, or recommend. Auto-Claw sees problems, decides on fixes, and writes the code.

---

## 19 Capabilities (All Implemented ✅)

| Category | Capability | File | Description |
|----------|-----------|------|-------------|
| **SEO** | Meta Tag Scanner | `src/seo.py` | Scans title, description, H1-H6, alt tags, OG tags |
| **SEO** | Fix Generator | `src/seo_fix.py` | Generates WP-CLI commands to fix SEO issues |
| **SEO** | Schema.org Generator | `src/schema.py` | Article/Product/FAQ/Breadcrumb/Org/Website JSON-LD |
| **Content** | Quality Auditor | `src/content_audit.py` | Flesch-Kincaid readability, E-E-A-T signals |
| **Performance** | Diagnostic | `src/performance_diag.py` | Core Web Vitals, TTFB, LCP, CLS, PHP-FPM |
| **Performance** | Cache Optimizer | `src/cache_optimizer.py` | Multi-level cache analysis & recommendations |
| **Performance** | Image Optimizer | `src/image_optimizer.py` | JPG/PNG/WebP compression analysis |
| **Growth** | A/B Tester | `src/ab_tester.py` | Multi-variant testing with Bayesian significance |
| **Growth** | Exit Intent | `src/exit_intent.py` | Popup intervention with geo/cart targeting |
| **Growth** | Journey Personalizer | `src/journey_personalizer.py` | User segment-based content personalization |
| **Growth** | GEO Targeting | `src/geo_targeting.py` | IP-based geo content + dynamic pricing |
| **Growth** | Smart Landing Page | `src/landing_page.py` | High-conversion landing page generator |
| **Growth** | Review Summarizer | `src/landing_page.py` | Sentiment analysis on customer reviews |
| **Growth** | Dynamic FAQ | `src/dynamic_faq.py` | FAQ with Schema.org + real-time help widgets |
| **Growth** | Promo Switcher | `src/promo_switcher.py` | Auto campaign calendar (Black Friday/618/双11) |
| **Operations** | AI Content Generator | `src/ai_content_generator.py` | Generate blog/product/landing copy with AI |
| **Operations** | Competitor Monitor | `src/competitor_monitor.py` | Price/content/SEO change detection |
| **Core** | WordPress CRUD | `src/wordpress.py` | Posts, plugins, themes, schema injection |
| **Core** | Vault + Gate + Audit | `src/vault.py`, `pipeline.py`, `audit.py` | Security framework |

---

## Quick Start

```bash
cd /root/.openclaw/workspace/auto-company/projects/auto-claw

# Run full site audit (all 19 capabilities)
python3 cli.py full-audit

# Individual capabilities
python3 cli.py seo --url http://yoursite.com --web-root /var/www/html
python3 cli.py performance --url http://yoursite.com --web-root /var/www/html
python3 cli.py geo --city 北京 --base-price 99
python3 cli.py ab-test --url http://yoursite.com/landing --element headline
python3 cli.py promo
python3 cli.py wp status --web-root /var/www/html
```

---

## Architecture

```
src/
├── agent.py           WordPressAgent — unified orchestration
├── wordpress.py        WP-CLI client — local + remote SSH
├── vault.py           Credentials vault (1Password/HashiCorp/fallback)
├── pipeline.py        Gate Pipeline — LOW/MEDIUM/HIGH risk classification
├── audit.py           JSONL audit logging
├── seo.py             SEO scanner (PageMeta, SEOReport, SEOAnalyzer)
├── seo_fix.py         Fix generator (SEOMetaGenerator, SEODiff)
├── schema.py          Schema.org JSON-LD generator
├── content_audit.py    Content quality auditor
├── performance_diag.py Performance diagnostic
├── cache_optimizer.py  Cache optimizer
├── image_optimizer.py  Image optimizer
├── ab_tester.py        A/B testing engine
├── exit_intent.py      Exit intent intervention
├── journey_personalizer.py User journey personalization
├── geo_targeting.py    GEO targeting + dynamic pricing
├── landing_page.py     Landing page generator + review summarizer
├── dynamic_faq.py       Dynamic FAQ system
├── promo_switcher.py    Campaign calendar
├── ai_content_generator.py AI content generation
└── competitor_monitor.py Competitor monitoring
```

---

## Security Architecture

- **Vault**: Credentials never in code — stored in HashiCorp Vault or 1Password Business
- **Gate Pipeline**: Every destructive action requires approval
  - 🔓 `LOW` risk (GET operations) → auto-execute
  - ⚠️ `MEDIUM` risk (create/update) → requires approval
  - 🔒 `HIGH` risk (delete/core updates) → always blocked
- **Audit Log**: Every action logged to `logs/audit.jsonl` with timestamp, actor, action, result

---

## Target Customer

**D2C brands on WooCommerce, $500K-$5M revenue, 1-5 person teams.**

- No time for SEO/performance optimization
- Can't afford full-time specialists
- Need 24/7 automated operations

**Pricing anchor**: $500-2,000/month as "AI team member" (not "tool")

---

## Real Test Site

```
URL: http://linghangyuan1234.dpdns.org
WordPress: 6.9.4
PHP: 8.2.28
Theme: twentytwentyfive v1.4
Posts: 4 published
Users: 2 admins
```

---

## Next Steps

- [ ] ClawhHub publish (requires `--token` from https://clawhub.ai)
- [ ] SSH remote WordPress management
- [ ] Vault production configuration
- [ ] Real LLM integration for content generation

---

## License

Proprietary — auto-company internal use.
