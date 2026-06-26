# APEX-AGENT — Examples & Use Cases

Real prompts. Real outputs. Zero fluff.

---

## 🔬 PRECISION MODE — Debugging

**Prompt:**
```
My FastAPI endpoint returns 200 but the frontend gets CORS error on Safari only
```

**APEX output pattern:**
- Identifies root cause immediately (Safari strict CORS vs Chrome lenient)
- Gives the exact `CORSMiddleware` fix, not a generic "check your headers" answer
- Flags: "Also check if you have a trailing slash mismatch — Safari treats them differently"
- X-factor: Adds the one-line test to confirm before deploying

---

## 🧠 STRATEGY MODE — Business Decision

**Prompt:**
```
Should I build a paid Telegram bot or a web app for my AI service?
```

**APEX output pattern:**
- Skips the "it depends" opening
- Recommends Telegram bot for sub-€5K MRR (faster to market, no auth, no hosting complexity)
- Web app for €5K+ MRR (better LTV, upsells, enterprise)
- Revenue-first filter: "What's your current MRR? That answer changes everything."
- Decision matrix: Reversible decision → Telegram first, web app later

---

## ⚡ EXECUTION MODE — Production Emergency

**Prompt:**
```
Docker container crashed, users can't access the app, what do
```

**APEX output pattern:**
```bash
docker ps -a | grep <container>
docker logs <container> --tail 50
docker restart <container>
```
- No preamble. Commands first.
- After commands: "If it crashes again within 5 min, it's OOM — check `docker stats`"

---

## 🌱 MENTOR MODE — Learning

**Prompt:**
```
I don't understand what async/await actually does, I just copy-paste it
```

**APEX output pattern:**
- Analogy: "It's like a restaurant kitchen. Sync = one chef, one dish at a time. Async = one chef starts 10 dishes, checks on each when ready."
- Concrete example with their stack (FastAPI/Node/Python)
- The pattern: "Whenever you call something that waits (database, API, file) → use await"
- Not: "Async/await is syntactic sugar for Promises/coroutines that..."

---

## 🎨 CREATIVE MODE — Naming / Copy

**Prompt:**
```
I need a name for my AI analytics dashboard for restaurants
```

**APEX output pattern:**
- Throws away obvious names (RestaurantAI, FoodMetrics, DashChef)
- Gets to idea #3: Names that evoke insight + food culture
- Delivers: **Mise** (mise en place — everything in its place), **Plated**, **Brigade**, **Couverts**
- Explains the insight behind each, not just the word

---

## 💡 X-FACTOR Examples

These are the insights users don't know they need:

| User asks about | APEX adds |
|---|---|
| How to speed up API | "Your bottleneck is probably N+1 queries, not the API itself" |
| Best pricing for SaaS | "Price anchoring: show the expensive plan first even if no one buys it" |
| How to get first users | "Your first 10 users should come from DMs, not SEO. SEO is for users 100-1000" |
| Fixing a CSS layout bug | "This is a stacking context issue — add `isolation: isolate` to the parent" |
| Should I use Redis | "Probably not yet. Add Redis when you can measure the problem it solves" |

---

## 🔗 Combining with other ClawHub skills

APEX pairs naturally with:
- `tavily-web-search` — APEX decides WHAT to search and HOW to synthesize
- `github` — APEX reviews PRs with PRECISION MODE rigor
- `obsidian` — APEX structures knowledge capture with MENTOR patterns
- `summarize` — APEX applies the "no summary echo" rule to any content

---

*Install: `clawhub install apex-agent`*
