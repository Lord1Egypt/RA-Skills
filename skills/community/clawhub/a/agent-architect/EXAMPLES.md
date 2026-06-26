# ARCHITECT — Execution Examples

The difference between a tool that answers and an agent that delivers.

---

## Example 1: SaaS Landing Page (BUILD MODE)

```
User: Build me a landing page for my AI document analysis tool

⚙ ARCHITECT — MISSION BRIEF
Goal:        Production-ready landing page for AI SaaS
Success:     Complete HTML/CSS page optimized for conversions
Constraints: Must work without JS frameworks, mobile-first
Estimated:   6 tasks · HIGH complexity
Proceeding.

[T01 · RESEARCH]  ✓ Analyzed 3 top-performing AI tool landing pages
[T02 · STRUCTURE] ✓ 7-section outline: Hero → Problem → Solution →
                    Features → Social Proof → Pricing → CTA
[T03 · COPY]      ✓ Full copy written: headline, subheads, feature
                    descriptions, CTA variants
[T04 · DESIGN]    ✓ Design system: dark theme, #0A0F1A bg, cyan accent,
                    Space Grotesk + JetBrains Mono
[T05 · BUILD]     ✓ Complete HTML/CSS/JS — 847 lines
[T06 · REVIEW]    ✗ Failed — mobile nav broken on iOS Safari
                  Adapting: Rewrote nav with CSS-only hamburger
[T06 · REVIEW]    ✓ Done — all breakpoints clean, 94 Lighthouse score

⚙ MISSION COMPLETE — 6/6 tasks · 1 adapted

[Complete landing page delivered — copy-paste ready]
```

---

## Example 2: Competitor Research (RESEARCH MODE)

```
User: Research the top AI agent frameworks and tell me where the gaps are

⚙ ARCHITECT — MISSION BRIEF
Goal:        Competitive landscape + gap analysis for AI agent frameworks
Success:     Actionable positioning insights with evidence
Estimated:   5 tasks · MED complexity
Proceeding.

[T01 · SCOPE]     ✓ Defined: AutoGPT, LangGraph, CrewAI, OpenAgents,
                    ClawHub ecosystem
[T02 · GATHER]    ✓ Profiled each: architecture, strengths, weaknesses,
                    user complaints from GitHub issues
[T03 · ANALYZE]   ✓ Matrix built: setup complexity, autonomy level,
                    memory, multi-agent, cost
[T04 · GAPS]      ✓ 3 clear gaps: (1) no persistent memory standard,
                    (2) no cognitive quality layer, (3) setup too complex
                    for non-developers
[T05 · RECOMMEND] ✓ Positioning: "The zero-config autonomous agent stack"

⚙ MISSION COMPLETE — 5/5 tasks

GAP ANALYSIS:
Every framework requires either heavy setup (LangGraph, CrewAI)
or sacrifices autonomy (basic ChatGPT plugins). The gap:
a skill-based system that works with ANY model, needs NO config,
and handles cognition + memory + execution as modular layers.

That gap is exactly what apex-agent + agent-memoria + architect fills.
```

---

## Example 3: Code Audit (AUDIT MODE)

```
User: Review my FastAPI backend and find the problems

⚙ ARCHITECT — MISSION BRIEF
Goal:        Full code audit of FastAPI backend
Success:     Prioritized list of issues with specific fixes
Estimated:   4 tasks · MED complexity
Proceeding.

[T01 · UNDERSTAND] ✓ Architecture mapped: 3 routers, 12 endpoints,
                     PostgreSQL via SQLAlchemy, JWT auth
[T02 · EXAMINE]    ✓ Line-by-line review complete
[T03 · IDENTIFY]   ✓ Issues found and categorized
[T04 · RECOMMEND]  ✓ Fixes written for all HIGH priority items

⚙ MISSION COMPLETE — 4/4 tasks

FINDINGS (by severity):

HIGH — SQL Injection risk in /search endpoint (line 47)
  Current:  f"SELECT * FROM items WHERE name = '{query}'"
  Fix:      db.execute("SELECT * FROM items WHERE name = :q", {"q": query})

HIGH — JWT tokens never expire (no exp claim)
  Fix:      Add exp: datetime.utcnow() + timedelta(hours=24)

MED — N+1 query in /users/{id}/orders (loads orders in loop)
  Fix:      Use joinedload() or a single JOIN query

MED — No rate limiting on /auth/login (brute force possible)
  Fix:      Add slowapi: @limiter.limit("5/minute")

LOW — Missing indexes on frequently queried columns
LOW — Error messages expose stack traces in production
```

---

## Example 4: Full Stack (APEX + MEMORIA + ARCHITECT)

```
[APEX active — strategy mode]
[MEMORIA active — 23 entries loaded: Hlia, OmnimisChef, Vue3+FastAPI stack]
[ARCHITECT active]

User: I need to get my first paying customer this week

⚙ ARCHITECT — MISSION BRIEF
Goal:        First paying customer acquisition
Real goal:   Validate that someone will pay for OmnimisChef
Success:     At least 1 Gumroad purchase or committed intent
Constraints: Solo founder, limited time, no ad budget
Scope out:   New features, marketing campaigns, cold email sequences
Estimated:   4 tasks · MED complexity
Proceeding.

[MEMORIA note: Last attempted outreach 3 weeks ago — no follow-up done]
[APEX note: Revenue-first filter active — each task evaluated on direct revenue path]

[T01 · AUDIT]    ✓ Current assets: neurodoc.app live, Gumroad set up,
                   LinkedIn post from today (73 impressions, growing)
[T02 · IDENTIFY] ✓ 3 highest-probability paths ranked:
                   1. DM the 15 people who liked today's LinkedIn post
                   2. Post in 2 Greek F&B WhatsApp groups you're in
                   3. Offer free 30-min demo to 5 specific contacts
[T03 · EXECUTE]  ✓ 15 personalized DM drafts written — ready to send
                   5 demo offer messages written
                   F&B group post written in Greek
[T04 · TRACK]    ✓ Simple tracking: Google Sheet template created
                   Follow-up triggers set for 48h, 72h

⚙ MISSION COMPLETE — 4/4 tasks

Your fastest path to first payment is today's LinkedIn post.
15 people liked it. They're warm. DM them in the next 2 hours
while the post is still fresh. Script is ready — copy and send.
```

---

## The Trilogy in Action

```
GOAL:   "Take my product from idea to ready-to-launch"

APEX     breaks down the strategic decision tree
MEMORIA  knows your stack, constraints, and past decisions
ARCHITECT executes 12 tasks across 3 days, adapts 2 that fail,
          delivers a production-ready launch checklist, landing page,
          and outreach strategy — with full context of who you are
          and what you've already tried

This is not a chatbot. This is an autonomous colleague.
```

---

*Install the complete stack:*
```bash
clawhub install apex-agent
clawhub install agent-memoria
clawhub install architect
```
