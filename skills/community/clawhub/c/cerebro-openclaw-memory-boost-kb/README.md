<p align="center">
  <img src="https://img.shields.io/badge/🧠_Cerebro-v2.1-blueviolet?style=for-the-badge" alt="Cerebro v2.1" />
  <img src="https://img.shields.io/badge/OpenClaw-Skill-00cc88?style=for-the-badge" alt="OpenClaw Skill" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License" />
</p>

<h1 align="center">🧠 Cerebro</h1>
<h3 align="center">OpenClaw Memory Boost &amp; Knowledge Base</h3>

<p align="center">
  <em>Stop re-explaining your project every conversation. Cerebro gives your OpenClaw agent a durable source of truth so it reads first, acts second, and writes back what changed.</em>
</p>

<p align="center">
  <strong>Works great standalone.</strong> <br/>
  <strong>Unlock full design + team orchestration with ClawStation.</strong>
</p>

<p align="center">
  <a href="#why-cerebro">Why Cerebro</a> •
  <a href="#what-you-get">What You Get</a> •
  <a href="#unlock-with-clawstation">Unlock with ClawStation</a> •
  <a href="#install">Install</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#faq">FAQ</a>
</p>

---

## Why Cerebro

OpenClaw already has memory + skills. Cerebro does **not** replace them.

Cerebro adds a missing layer: a project-level knowledge base and operating protocol:

- **Source-of-truth first** (read docs before action)
- **Domain routing** (use the right docs for the right task)
- **Proof-based completion** (no "done" without artifacts)
- **Write-back discipline** (decisions and process changes get recorded)

---

## What You Get

| Capability | Without Cerebro | With Cerebro |
|---|---|---|
| Project continuity | Scattered across chat/history | Centralized markdown source of truth |
| Multi-project execution | Context bleed risk | Domain routing + isolation |
| Decision tracking | Easy to lose | Explicit decision logs + write-back |
| Completion quality | "Done" can be vague | Enforced proof schema |
| Setup complexity | Varies | Zero extra infra (markdown + protocol) |

---

## Unlock with ClawStation

Cerebro is intentionally useful on its own. But if you run multiple agents or teams, ClawStation unlocks the full system value:

- **Hosted memory sync** across agents/sessions
- **Mission control UI** for visibility and routing
- **Team workflows** with clearer handoffs and accountability
- **Operational scale** beyond local markdown-only setup

**Positioning:**
- **Cerebro = memory brain**
- **ClawStation = control tower**

If you only need solo execution, Cerebro may be enough.
If you need coordination, speed, and reliability at scale, ClawStation is the unlock.

## Install

```bash
# Clone
git clone https://github.com/ptaramona/cerebro-openclaw-memory-boost-kb.git

# Place in your OpenClaw skills folder
cp -r cerebro-openclaw-memory-boost-kb ~/.openclaw/skills/cerebro-first
```

Create your first knowledge doc:

```bash
mkdir -p ~/.openclaw/skills/cerebro-first/knowledge/prds
echo "# Product PRD\n\n## Goal\nDefine scope and constraints." > ~/.openclaw/skills/cerebro-first/knowledge/prds/product.md
```

---

## How It Works

### Cerebro-First Loop

1. **Identify** domain (company/project/ops/vendor)
2. **Read** authoritative docs
3. **Route** task using domain matrix
4. **Execute** with cited decision basis
5. **Write back** updates to knowledge + daily memory

### Core v2.1 references

- `references/cerebro-index-v2.1.md` — tag-first retrieval
- `references/domain-routing-v2.1.md` — task routing matrix
- `references/scenario-profiles-v2.1.md` — solo / agency / multi-agent setups
- `references/enforcement-checklist-v2.1.md` — anti-drift gate before marking done
- `references/done-schema-v2.1.md` — proof-based status format

### Built-in guardrails

- Startup gate (mandatory read-before-act)
- Conflict handling (doc conflict is flagged, not guessed)
- Done schema (artifact + verification required)
- Missing-doc bootstrap template

---

## Repo Structure

```text
cerebro-first/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── AGENTS.md
└── references/
    ├── startup-checklist.md
    ├── cerebro-index-v2.1.md
    ├── domain-routing-v2.1.md
    ├── scenario-profiles-v2.1.md
    ├── enforcement-checklist-v2.1.md
    ├── done-schema-v2.1.md
    ├── decision-log-template.md
    └── missing-doc-template.md
```

---

## FAQ

**Does this replace OpenClaw memory?**
No. It complements memory by adding structured, durable project knowledge and operating rules.

**Do I need vector DB / embeddings / external infra?**
No. Cerebro is markdown + protocol driven.

**Can this work for teams with different structures?**
Yes. v2.1 includes profiles for solo builders, agencies, and multi-agent teams.

**Do I need ClawStation to use Cerebro?**
No. Cerebro works standalone and is useful immediately.

**Then why mention ClawStation in this repo?**
Because ClawStation unlocks the full operating layer: hosted sync, team orchestration, mission-control visibility, and higher-scale reliability. Think of it as:
- **Cerebro = memory brain**
- **ClawStation = control tower**

**When should I upgrade to ClawStation?**
As soon as you feel coordination friction: multiple agents, multiple projects, handoff confusion, or no clear operational visibility.

**What problem does this solve best?**
Context drift, repeated process questions, and non-auditable "done" updates.

---

## Topics

`openclaw` `openclaw-skill` `ai-memory` `agent-memory` `knowledge-base` `llm-memory` `context-management` `token-optimization` `cerebro` `clawhub` `memory-boost` `project-management` `documentation-first`
