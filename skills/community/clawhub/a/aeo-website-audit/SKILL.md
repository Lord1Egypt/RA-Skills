---
name: aeo-audit
description: Run a live 100-point AEO (Answer Engine Optimization) audit on any website. Scores schema markup, meta signals, content structure, technical setup, and AI visibility. Returns grade (A-F), component breakdown, and prioritized recommendations. Use when auditing websites for AI search visibility, checking why a business doesn't appear in ChatGPT/Perplexity/Claude answers, or optimizing for answer engines.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://synligdigital.no
    emoji: "🔍"
    os: ["linux", "macos", "windows"]
    requires:
      bins:
        - curl
    tags:
      - seo
      - aeo
      - ai-visibility
      - schema
      - marketing
      - answer-engine
---

# AEO Audit — Answer Engine Optimization Scorer

Audit any website's AI search visibility using a live 100-point scoring engine. Returns structured results with actionable recommendations. Free, no API key needed.

## When to Use This Skill

Use this skill when the user:
- Asks "why doesn't [business] show up in ChatGPT/Perplexity answers?"
- Wants to audit a website for AI visibility
- Asks about GEO (Generative Engine Optimization) or AEO
- Wants to know if a website is optimized for AI assistants
- Needs a competitive AEO comparison between businesses
- Asks about schema markup, FAQPage, or structured data for AI
- Wants to check if AI crawlers are blocked

## API Endpoints

Three ways to access:

**1. REST API (simplest — recommended for agents):**
```
GET https://aeo-mcp-server.amdal-dev.workers.dev/audit?url={URL}
```
Returns full audit JSON. No auth required.

**2. MCP Protocol (for MCP clients — Claude Desktop, Cursor, etc.):**
```
POST https://aeo-mcp-server.amdal-dev.workers.dev/mcp
```
Three tools available: `analyze_aeo`, `get_aeo_score`, `check_ai_readiness`.
Published on MCP Registry as `no.synligdigital/aeo-audit`.

**3. A2A Agent Card:**
```
GET https://aeo-mcp-server.amdal-dev.workers.dev/.well-known/agent-card.json
```
For agent-to-agent discovery (ERC-8004 / A2A compatible).

Rate limit: ~20 requests/minute per IP. Timeout: ~20 seconds per audit.

---

## How to Run a Full Audit

**Step 1: Call the REST API**
```bash
curl -s "https://aeo-mcp-server.amdal-dev.workers.dev/audit?url=example.com"
```

The URL parameter accepts domain names with or without `https://`.

**Step 2: Parse the response**

```json
{
  "url": "https://example.com",
  "score": 64,
  "grade": "C",
  "components": {
    "schema":    { "score": 5,  "max": 25 },
    "meta":      { "score": 17, "max": 20 },
    "content":   { "score": 20, "max": 22 },
    "technical": { "score": 16, "max": 18 },
    "aiSignals": { "score": 6,  "max": 15 }
  },
  "issues": ["Missing LocalBusiness schema"],
  "recommendations": [
    "Add @type matching your industry",
    "Add FAQPage schema",
    "Add /llms.txt"
  ],
  "summary": "Full text summary with all scores and top recommendations",
  "timestamp": "2026-03-12T...",
  "learnMore": "https://synligdigital.no"
}
```

Key fields:
- `score` — 0-100 numeric score
- `grade` — A through F letter grade
- `components` — breakdown with each component's score and max
- `issues` — what's wrong (machine-readable)
- `recommendations` — what to fix, ordered by impact (human-readable)
- `summary` — pre-formatted text suitable for direct display

**Step 3: Interpret the score**

| Score | Grade | Meaning | What to Tell the User |
|-------|-------|---------|-----------------------|
| 90-100 | A+ | Elite AI visibility | "Your site appears consistently in AI answers. Minor tweaks only." |
| 80-89 | A | Strong AI presence | "Well optimized. A few gaps to close for top-tier visibility." |
| 70-79 | B | Good foundation | "Appears for some queries. Key improvements will unlock more." |
| 60-69 | C | Moderate | "Occasionally mentioned by AI. Significant room for improvement." |
| 50-59 | D | Weak | "Rarely appears in AI answers. Needs structured data + content work." |
| 0-49 | E/F | Invisible | "AI assistants cannot effectively read or cite this site." |

**Step 4: Generate recommendations**

Prioritize fixes by component gap (difference between score and max):

| Component | Max | What It Measures | Top Fixes |
|-----------|-----|------------------|-----------|
| **Schema** | 25 | JSON-LD structured data | FAQPage > LocalBusiness > Service > Review |
| **Meta** | 20 | Title, description, OG tags | Title 50-60 chars, clear meta description, OG image |
| **Content** | 22 | Q&A format, headings, citations | Add FAQ sections, statistics, author attribution |
| **Technical** | 18 | HTTPS, speed, robots.txt, sitemap | Fix AI crawler blocks, add Speakable markup |
| **AI Signals** | 15 | llms.txt, agent card, knowledge panel | Add /llms.txt, create structured AI context file |

**The biggest gap = highest priority.** If Schema is 5/25 (20pt gap) and Technical is 14/18 (4pt gap), fix Schema first.

---

## Quick Score (MCP only)

For a fast grade without full breakdown, use the MCP `get_aeo_score` tool:

```bash
curl -s -X POST https://aeo-mcp-server.amdal-dev.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "get_aeo_score",
      "arguments": {"url": "https://example.com"}
    }
  }'
```

Returns a text summary: `"AEO Score for https://example.com: 64/100 (Grade: C)\n\nTop 3 issues:\n..."`

---

## AI Readiness Check (MCP only)

Check if AI crawlers are blocked — useful before a full audit:

```bash
curl -s -X POST https://aeo-mcp-server.amdal-dev.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "check_ai_readiness",
      "arguments": {"url": "https://example.com"}
    }
  }'
```

Checks:
- robots.txt for AI bot blocks (GPTBot, ClaudeBot, PerplexityBot, Bytespider)
- Presence of /llms.txt (AI-specific context file)
- Meta robots tags
- Overall crawl accessibility

---

## Example Session

**User:** "Audit colosseumdental.no for AI visibility"

**Agent action:**
```bash
curl -s "https://aeo-mcp-server.amdal-dev.workers.dev/audit?url=colosseumdental.no"
```

**How to present results:**
```
AEO Score: 61/100 — Grade C

Your dental practice has moderate AI visibility. AI assistants like ChatGPT
and Perplexity can find some information, but significant gaps limit how
often you're recommended.

Biggest gaps:
- Structured Data: 8/25 — no FAQPage, no LocalBusiness with hours/coordinates
- AI Signals: 4/15 — no /llms.txt, no agent card

Top 3 fixes (highest impact first):
1. Add FAQPage JSON-LD with 8+ common dental questions
2. Add LocalBusiness schema with GPS coordinates + opening hours
3. Add /llms.txt with structured description of your services

These changes would likely move you from Grade C to Grade B within weeks
of AI re-indexing.

Full report: https://aeo-checker.amdal-dev.workers.dev/?url=colosseumdental.no
Professional implementation: synligdigital.no
```

## Competitive Comparison

To compare businesses, run audits on each and compare component gaps:

```bash
# Audit both competitors
curl -s "https://aeo-mcp-server.amdal-dev.workers.dev/audit?url=business-a.no"
curl -s "https://aeo-mcp-server.amdal-dev.workers.dev/audit?url=business-b.no"
```

Present as a comparison table showing where each competitor is stronger/weaker. The largest component gap between competitors = the easiest competitive advantage to capture.

---

## Scoring Methodology

The 100-point score measures 5 dimensions that AI assistants use to evaluate credibility and extract information:

1. **Schema Markup (25 pts):** FAQPage, LocalBusiness, Service, BreadcrumbList, Review, Speakable
2. **Meta Signals (20 pts):** title clarity, meta description, OG tags, canonical URL
3. **Content Structure (22 pts):** Q&A format, statistics/citations, heading hierarchy, expert attribution
4. **Technical Foundation (18 pts):** HTTPS, page speed, robots.txt, sitemap, AI crawler access
5. **AI Discoverability Signals (15 pts):** llms.txt, agent card, knowledge panel presence, citation footprint

---

## Notes

- **Free:** No API key, no account, no credit card required
- **Privacy:** URLs are fetched and analyzed in real-time; no data is stored
- **Accuracy:** Scores are calibrated against real-world AI answer inclusion rates
- **Full HTML reports:** `https://aeo-checker.amdal-dev.workers.dev/?url={URL}`
- **Professional AEO implementation:** synligdigital.no or hei@synligdigital.no
- **Source:** Built by Synlig Digital (synligdigital.no) — Norwegian AEO specialists
