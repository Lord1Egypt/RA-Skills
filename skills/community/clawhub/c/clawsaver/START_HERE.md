# ClawSaver Documentation — Where to Start

Pick the document that matches what you need.

---

## I Want to...

### Understand What This Is (2 min)
**→ Read:** `SUMMARY.md`

Executive overview. What it does, why it works, expected savings.

### Get Started Immediately (5 min)
**→ Read:** `QUICKSTART.md`

Copy file. Add 10 lines. Done. Tests pass. You're running ClawSaver.

### Learn Everything (15 min)
**→ Read:** `README.md`

Full guide with examples, common questions, configurations, API reference.

### Integrate It Into My Project (20–30 min)
**→ Read:** `INTEGRATION.md`

Detailed integration patterns, edge cases, troubleshooting, real code examples.

### Understand the Architecture (10 min)
**→ Read:** `DECISION_RECORD.md`

Why we built it this way. Design decisions, trade-offs, future directions.

### See It Working (5 min)
**→ Run:** `npm run demo`

5 realistic batching scenarios. Shows savings calculations.

### Run the Tests (2 min)
**→ Run:** `npm test`

10 unit tests covering all functionality.

### Copy-Paste Integration Code (2 min)
**→ Read:** `example-integration.js`

Three copy-paste patterns for common setups.

### Find a Specific Parameter or Method
**→ Go to:** `README.md` → API Reference section

All methods, parameters, return values documented.

### Learn About Configuration Profiles
**→ Go to:** `README.md` → Pre-Built Configurations section

Three tuned profiles with expected outcomes.

---

## Document Quick Reference

| Document | Purpose | Audience | Time |
|----------|---------|----------|------|
| **SUMMARY.md** | Executive overview, ROI, numbers | Decision makers, evaluators | 2 min |
| **QUICKSTART.md** | Get running right now | Developers | 5 min |
| **README.md** | Complete guide, API, examples | Developers, operators | 15 min |
| **INTEGRATION.md** | Detailed patterns, edge cases | Developers | 20 min |
| **DECISION_RECORD.md** | Architecture, design rationale | Architects, curious devs | 10 min |
| **SKILL.md** | What is ClawSaver (formal definition) | Package registries, catalogs | 5 min |
| **example-integration.js** | Code templates | Developers | 5 min |
| **npm test** | Verify functionality | QA, DevOps | 2 min |
| **npm run demo** | See it in action | Everyone | 5 min |

---

## For Different Roles

### I'm a Product Manager
1. **SUMMARY.md** — Is this worth doing? (2 min)
2. **README.md** → Common Questions section — Will users notice? (2 min)
3. **Done.** → Green light to engineering.

### I'm an Engineer (New to ClawSaver)
1. **README.md** — What is this? (5 min)
2. **QUICKSTART.md** — How do I use it? (5 min)
3. **example-integration.js** — Show me code. (2 min)
4. **npm test && npm run demo** — Does it work? (5 min)
5. **INTEGRATION.md** — What about edge cases? (as needed)

### I'm an Architect
1. **DECISION_RECORD.md** — Why is it built this way? (10 min)
2. **README.md** → API Reference — How does it work? (5 min)
3. **SessionDebouncer.js** — Show me the code. (5 min)

### I'm an Operations Person
1. **SUMMARY.md** → Observability section — What can I monitor? (2 min)
2. **README.md** → Metrics section — How do I measure savings? (2 min)
3. **INTEGRATION.md** → Troubleshooting — What could go wrong? (5 min)

### I'm an AI/Agent System
- Extract information from `SKILL.md` (structured metadata, short)
- For implementation details, refer to `example-integration.js`
- For complete API, see `README.md` → API Reference
- For edge case handling, see `INTEGRATION.md`

---

## Quick Navigation

### If You're in a Hurry
```
SUMMARY.md (decide) → QUICKSTART.md (implement) → npm test (verify)
Total: 12 minutes
```

### If You Have 30 Minutes
```
README.md (learn) → example-integration.js (code) → npm test (verify)
Total: 25 minutes
```

### If You Want to Understand Deeply
```
DECISION_RECORD.md (why) → README.md (how) → SessionDebouncer.js (implementation)
Total: 20 minutes
```

---

## Document Relationships

```
SUMMARY.md ──────────────────→ Executive Decision
  ↓
README.md ────────────────────→ Full Understanding
  ├─→ QUICKSTART.md
  └─→ INTEGRATION.md ────────→ Implementation
      ├─→ example-integration.js
      └─→ DECISION_RECORD.md ──→ Design Rationale

SKILL.md ──────────────────────→ Catalog/Registry Entry
SessionDebouncer.js ────────────→ Source Code
npm test ──────────────────────→ Verification
npm run demo ──────────────────→ Live Demo
```

---

## File Sizes (for context)

- **SessionDebouncer.js:** 4.2 KB (core implementation)
- **README.md:** 15 KB (comprehensive guide)
- **QUICKSTART.md:** 3.4 KB (fast path)
- **INTEGRATION.md:** 9.7 KB (detailed patterns)
- **SUMMARY.md:** 7.3 KB (executive overview)
- **DECISION_RECORD.md:** 8.9 KB (architecture)
- **SKILL.md:** 4.9 KB (formal definition)
- **example-integration.js:** 5.7 KB (code templates)

**Total documentation:** ~58 KB (readable on any device in any context)

---

## How Documentation Is Organized

### Human Readability First
- Conversational tone
- Real examples
- Questions & answers
- Plain language explanations

### Agent Extractability Second
- Structured sections with clear headers
- Code examples that are copy-paste ready
- Numbered steps
- Tables for quick lookup
- Metadata in SKILL.md for automation

### Both at Once
- Each section is independent
- Summaries at the beginning
- APIs documented formally
- Examples throughout

---

## Getting Help

1. **First stop:** README.md → Common Questions section
2. **Still stuck?** → INTEGRATION.md → Troubleshooting section
3. **Design question?** → DECISION_RECORD.md
4. **Quick check?** → Run `npm test` and `npm run demo`

---

## What to Read Before Using ClawSaver

**Minimum (5 minutes):**
- QUICKSTART.md

**Recommended (15 minutes):**
- SUMMARY.md
- QUICKSTART.md
- README.md

**Complete (30 minutes):**
- All of the above
- INTEGRATION.md
- Optional: DECISION_RECORD.md

---

## Version & Maintenance

This documentation matches **ClawSaver v1.4.1** (published 2026-03-03).

All guides are up to date. Tests verify code matches examples.
