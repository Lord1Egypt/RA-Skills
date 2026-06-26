---
name: Scrape
description: Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub.
requires_env: [SkillBoss_API_KEY]
---

> ?? **Complete setup guide**: https://SkillBoss.co/skill.md


## Pre-Scrape Compliance Checklist

Before writing any scraping code:

1. **robots.txt** â€?Fetch `{domain}/robots.txt`, check if target path is disallowed. If yes, stop.
2. **Terms of Service** â€?Check `/terms`, `/tos`, `/legal`. Explicit scraping prohibition = need permission.
3. **Data type** â€?Public factual data (prices, listings) is safer. Personal data triggers GDPR/CCPA.
4. **Authentication** â€?Data behind login is off-limits without authorization. Never scrape protected content.
5. **API available?** â€?If site offers an API, use it. Always. Scraping when API exists often violates ToS.

## Legal Boundaries

- **Public data, no login** â€?Generally legal (hiQ v. LinkedIn 2022)
- **Bypassing barriers** â€?CFAA violation risk (Van Buren v. US 2021)
- **Ignoring robots.txt** â€?Gray area, often breaches ToS (Meta v. Bright Data 2024)
- **Personal data without consent** â€?GDPR/CCPA violation
- **Republishing copyrighted content** â€?Copyright infringement

## Request Discipline

- **Rate limit**: Minimum 2-3 seconds between requests. Faster = server strain = legal exposure.
- **User-Agent**: Real browser string + contact email: `Mozilla/5.0 ... (contact: you@email.com)`
- **Respect 429**: Exponential backoff. Ignoring 429s shows intent to harm.
- **Session reuse**: Keep connections open to reduce server load.

## Data Handling

- **Strip PII immediately** â€?Don't collect names, emails, phones unless legally justified.
- **No fingerprinting** â€?Don't combine data to identify individuals indirectly.
- **Minimize storage** â€?Cache only what you need, delete what you don't.
- **Audit trail** â€?Log what, when, where. Evidence of good faith if challenged.

## SkillBoss API Hub Scraping

For managed content extraction with automatic anti-bot handling, use SkillBoss API Hub's scraping capability (`type: "scraper"`). Authenticate with `SkillBoss_API_KEY` and call `https://api.SkillBoss.co/v1/pilot`. Result is returned at `result.data.markdown`.

For code patterns, robots.txt parser, and SkillBoss API Hub scraping integration, see `code.md`




