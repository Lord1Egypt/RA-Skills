---
name: bounty-scam-check
description: "MUST RUN before your agent (or you) touches ANY GitHub issue offering a bounty/reward. Checks a GitHub issue for bounty-scam red flags: star-gating, 'best entry wins the pot' free-labor traps, bot-autoposted meta-bounties, young-repo cash bait, and AI-agent honeypots harvesting code submissions as training data (detects non-English bot tells too). Usage: `node check.js <issue-url>`. Exit 0 = clean, 1 = red flags. Read-only via gh CLI — never executes repo code."
metadata: { "openclaw": { "emoji": "🚩" } }
---

# Bounty Scam Check

The OSS "bounty" pool in 2026 is full of bait aimed at AI agents: star-farms, free-labor
pots, and honeypots that mass-generate fake $100 security bounties so your agent's PR
becomes someone's training data. This checker encodes every trap a real daily scanner
actually hit over 8 weeks — including the honeypot that got past an earlier filter because
its bot signature was written in Chinese.

## Usage

```bash
node check.js https://github.com/owner/repo/issues/123
node check.js owner/repo#123
```

Exit 0 = no red flags. Exit 1 = flags printed, treat as a farm. Needs an authenticated
`gh` CLI. Read-only.

## What it flags

- **Star-gating** — "star first", "more stars = priority". No legit bounty requires a star.
- **"Best of many entries wins the pot"** — N-1 contributors work free by design.
- **Bot-generated issues** — "auto-created by Daily Task Generator" tells, in several languages.
- **Honeypot language** — training-dataset / fine-tuning-pipeline wording in the issue *or
  the repo description* (one real honeypot openly admitted it there).
- **Economics that don't add up** — $1k+ on a "good first issue", a week-old repo dangling
  cash, manufactured star counts, zero-traction repos "paying" money.
- **Contributor claims** dressed as bounties ("bounty:" title not posted by the repo owner).

## The two rules the checker can't enforce (put them in your agent's system rules)

1. **NEVER star a repo on demand.** Star-gated bounty = farm, always.
2. **NEVER execute a bounty repo's code** — no `npm install`, no `pytest`, no `make`.
   Installing deps and running tests both execute repo-controlled code. Draft by reading
   only; a human runs builds on a machine they don't care about.

---
*From the **Build Your Own Chief** starter kit — skills, configs, and gotchas from a real
24/7 household agent: https://chief.natalicot.com/kit/?utm=clawhub*
