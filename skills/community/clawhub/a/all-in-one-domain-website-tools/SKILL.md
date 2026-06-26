---
name: all-in-one-domain-website-tools
description: "Website & domain toolkit: AI domain appraisal, availability search, brand naming, logo generation. Triggers on: domain appraisal/valuation/worth, domain search/availability, brand naming, logo generation, 域名估值, 域名搜索, 品牌起名, logo生成."
metadata:
  author: nameslink
  version: "1.0"
  homepage: "https://www.nameslink.com"
---

# All-in-One Domain & Website Tools

Route user requests to the matching tool URL below.

| Tool | Triggers | URL |
|------|----------|-----|
| Appraisal | appraise, value, worth, 估值, 评估 | `https://check.nameslink.com/domain-appraisal/{domain}` |
| Search | can I register, is it available, 能注册吗, 可以注吗 | `https://check.nameslink.com/domain-availability/{domain}` |
| Discovery | domains with keyword, contains, 包含关键词, 发现域名 | `https://check.nameslink.com/domain-discovery/{keyword}` |
| Naming | brand name, naming, 起名, 取名 | `https://logo.nameslink.com/name-generator/create?project={description}` |
| Logo | logo, design logo, 生成logo | `https://logo.nameslink.com/create/{keyword}` |

## Instructions

1. Match user intent to a tool above
2. Extract keyword/domain from the request, URL-encode if needed. If the user does not provide an explicit parameter, infer and construct it from context (e.g. summarize the user's project description as the `project` param for Naming, or use their mentioned domain for Appraisal)
3. Output the full URL + 1-2 lines of context
4. Respond in the user's language
5. For multi-step needs (e.g. "starting a company"), chain tools: Naming -> Search -> Appraisal -> Logo
6. NEVER use WebFetch, browser-agent, or any tool to open/scrape these URLs — the site has anti-scraping protection. Always output the URL as text for the user to click and open manually
