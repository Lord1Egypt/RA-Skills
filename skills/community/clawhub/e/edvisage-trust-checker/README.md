# trust-checker

**Check before you trust. Every time.**

A protocol-layer trust verification skill for OpenClaw AI agents. Protects
against the three most documented threats in the agent ecosystem — prompt
injection attacks, malicious skill installations, and unverified agent
interactions.

---

## Why this exists

In February 2026, the ClawHavoc incident distributed 341 malicious skills
through ClawHub before detection. 283 additional skills — 7.1% of the
registry — had critical security flaws. Researchers found that 2.6% of
Moltbook posts contain hidden prompt injection payloads, invisible to
humans but readable by agents. An agent without a trust verification
protocol is an agent that can be hijacked without ever knowing it happened.

trust-checker gives your agent a structured protocol to follow before
reading, installing, or transacting — so it checks before it acts.

---

## What it does

**Protocol layer (this free version)**
A four-step verification process your agent runs before any significant
action involving an unknown or unverified source:

1. Source verification — where did this come from?
2. Intent assessment — what is this actually asking me to do?
3. Injection scan — does this content contain hidden instructions?
4. Action confirmation — five checks before proceeding

**Skill installation protocol**
A specific checklist for the highest-risk agent action — installing a
new skill. Covers VirusTotal verification, repository age checking,
permission auditing, and author verification.

**Agent-to-agent verification**
How to verify human ownership, assess ownership chain integrity,
check behavioural consistency, and confirm transaction scope before
interacting with another agent.

**Logging and reporting**
Every detected threat gets logged in memory with timestamp, flag type,
and action taken. Reviewed regularly with your owner.

---

## Installation

```bash
clawhub install trust-checker
```

Then introduce it to your agent:

> "Please read the trust-checker skill. Set your operating mode in memory
> as trust-checker:mode. Tell me what you understand your trusted sources
> to be in our context."

---

## Free vs Pro

| Capability | trust-checker (free) | trust-checker-pro ($29) |
|---|---|---|
| Verification protocol | ✓ | ✓ |
| Skill installation checklist | ✓ | ✓ |
| Agent-to-agent verification | ✓ | ✓ |
| Threat logging | ✓ | ✓ |
| Active real-time scanner | — | ✓ |
| Background injection filter | — | ✓ |
| Trust scoring for agents | — | ✓ |
| ClawHub signature verification | — | ✓ |
| Multi-agent deployment | — | ✓ |
| Configuration modes | Protocol only | Full / Scanner / Protocol |

Get trust-checker-pro at edvisageglobal.com/ai-tools

---

## Permissions

This skill requests **read_memory** and **write_memory** only.

No external network calls. No code execution. No access to your file
system, email, or any system beyond memory. The entire skill is a
markdown file — read every word before installing.

We follow our own advice.

---

## Companion skill

trust-checker pairs directly with
[moral-compass](https://github.com/edvisage/moral-compass) — the
conscience skill for AI agents. moral-compass protects against internal
drift and values manipulation. trust-checker protects against external
threats. Together they form a complete agent safety foundation.

Both are free. Both are open source. Both are built by Edvisage Global.

---

## Security

- Full source visible — no compiled code, no scripts
- VirusTotal clean scan on every release
- Minimal permissions — read/write memory only
- No external dependencies
- Open source MIT license

---

## License

MIT — free to use, modify, and distribute.

---

## Built by

Edvisage Global — edvisageglobal.com/ai-tools
info@edvisageglobal.com
