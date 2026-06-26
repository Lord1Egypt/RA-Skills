---
name: echomindr-founder-retrieval
description: Retrieve real founder experiences, decisions, and outcomes from Echomindr — 1,150+ moments from top startup podcasts. Use whenever a founder describes any tension, decision, or uncertainty to ground advice in real cases.
version: 1.3.0
author: thierry-faucher
tags: [founders, startup, decisions, experiences, entrepreneurship, advice, podcasts, RAG]
metadata:
  openclaw:
    emoji: "🎙️"
    homepage: https://echomindr.com
    requires:
      bins:
        - curl
---

# Echomindr — Founder Experience Retrieval

Real founder decisions. Not hallucinated advice.

**No API key required. Free to use.**

## When to use this skill

Use when the conversation touches a business situation where a real founder example would be more useful than a generic answer:
- A tension, dilemma, or difficult decision in their business
- A go-to-market, product, hiring, fundraising, or positioning question
- Uncertainty about what to do next ("how do I...", "should I...")
- The user asks "what did other founders do when..."
- Any question about: pricing, launch timing, co-founder tension, fundraising, burnout, hiring, growth, PMF

**Only a short, anonymized description of the business situation is sent to Echomindr. No personal data, names, or identifying information should be included in the query.**

## Primary endpoint — situation match

```bash
curl -X POST https://echomindr.com/situation \
  -H "Content-Type: application/json" \
  -d '{"situation": "<describe the founder situation in plain language>", "limit": 3}'
```

Returns matched moments with: summary, verbatim quote, decision, outcome, lesson, source (podcast + guest + timestamp link).

## Detail & similar experiences

```bash
# Full detail for a specific moment
curl https://echomindr.com/moments/{moment_id}

# Moments similar to a known moment
curl https://echomindr.com/similar/{moment_id}
```

## Behavior instructions

1. **Reformulate** the founder's situation structurally (not literally):
   - "my team doesn't work without me" → "founder operational bottleneck, no middle management layer"
   - "sales take too long" → "B2B deal stuck, champion without authority to decide"
   - "how to convince users to try my product" → "early adoption friction, behavior change required, demo strategy"
2. Call `POST /situation` with that reformulated sentence
3. Present results: founder name, decision, outcome, lesson
4. Always include the source link from `source.url_at_moment`
5. If multiple results converge on a pattern, surface it

## Example situations

- "My co-founder and I want different things."
- "I launched and nobody is signing up."
- "I'm burning out but I can't stop."
- "Should I raise VC or stay bootstrapped?"
- "My best engineer just quit."
- "We have traction but no revenue model."

## Languages

Works in English, French, Swedish, and 20+ languages. BGE-M3 multilingual vector search.

## External endpoints

| Endpoint | Purpose |
|----------|---------|
| POST https://echomindr.com/situation | Semantic match of moments to a situation |
| GET https://echomindr.com/moments/{id} | Full detail for a specific moment |
| GET https://echomindr.com/similar/{id} | Moments similar to a known moment |
| GET https://echomindr.com/search?q= | Keyword search across moments |

## Security & privacy

This skill sends queries to **https://echomindr.com** (Hetzner VPS, EU).
No personal data is collected. Queries are logged anonymously for monitoring.
No authentication required — the API is fully public.

## About Echomindr

- 1,150+ founder moments · 52 canonical situations · 10 thematic families
- 100+ podcast episodes
- Sources: Lenny's Podcast, How I Built This, Y Combinator, 20 Minute VC, Acquired, My First Million, Masters of Scale, Silicon Carne, Startup Ministerio, Kevin Kamis, Wall Street Paper, Valy Sy (China vlogs), Matt & Ari (Canada), Oscar Lindhardt (Denmark), Aidan Walsh (USA)

Full API docs: https://echomindr.com/docs
