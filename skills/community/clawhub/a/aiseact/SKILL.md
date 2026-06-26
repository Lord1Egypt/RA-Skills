---
name: aiseact
description: AI search enhancement tool. Prioritizes authoritative sources for research and fact-checking.
triggers:
  - explicit: "aiseact" / "use aiseact" / "enhanced search"
  - autonomous: when enabled in config
---
This is optional. You control when to use it.

# Quick Start
## Invoke
"Use AISEACT to search [topic]"
"用AISEACT搜索 [主题]"

## Override
"Skip AISEACT" / "不用AISEACT"
"Include [source name]" / "包含 [来源]"

# Priority
P0: Official/Primary - Gov sites, company filings, academic
P1: Authoritative - AP, Reuters, Caixin, BBC
P2: Professional - Industry journals, reports
P3: UGC/Blogs - Zhihu, Jianshu (verify)
P4: Content farms - Baijiahao, clickbait

# Quick Rules
1. Policy -> site:gov.cn
2. China companies -> site:cninfo.com.cn
3. HK companies -> site:hkexnews.hk
4. Tech -> docs > GitHub > StackOverflow
5. Fact-check -> Snopes / PolitiFact

# Sources
## Reliable
- Intl: AP, Reuters, BBC
- China Finance: Caixin, Yicai
- China Society: Zaobao, SCMP, Initium

## Avoid
- Content farms: Baijiahao, Toutiao
- Political propaganda: Guancha, Epoch Times
- Biased: Breitbart, InfoWars

# Workflow
Phase 0: Plan - decompose, predict sources
Phase 1: Broad - multiple keywords, filter P4
Phase 2: Assess - rate authority, find gaps
Phase 3: Target - site: for official, filetype:pdf for docs
Phase 4: Verify - multi-source support? conflicts?
Phase 5: Output - cite sources, note uncertainty
Phase 6: Format - [source]-[url]-[primary/secondary]

# Search Syntax
- Gov: site:gov.cn
- China A-share: site:cninfo.com.cn
- HK: site:hkexnews.hk
- US: site:sec.gov
- GitHub: site:github.com
- Docs: filetype:pdf

# References
- quick-reference.md - Quick lookup (recommended)
- unreliable-sources.md - Detailed ratings
- authority-sources.md - Scenario-based

# Checklist
- [ ] Authentic sources for key info?
- [ ] P4 content farms filtered?
- [ ] Sources cited with URLs?
- [ ] Uncertainty noted?

*AISEACT - for quality-critical searches*
