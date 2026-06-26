# attention-research

**Scheduled intelligence research pipeline for OpenClaw.**

An agentic workflow that monitors topics on a twice-daily cadence, connects signals across time, and delivers structured digests. Not a news aggregator. A signal-tracking system that reads the matrix and surfaces what changed.

---

## For Agents — How to Run This

### Install From GitHub

For OpenClaw, Hermes, or any agent that can run shell commands, install directly from GitHub with either `git clone` or a `curl` tarball flow.

```bash
# git clone path
mkdir -p ~/.openclaw/skills
git clone https://github.com/riverho/attention-research.git ~/.openclaw/skills/attention-research
cd ~/.openclaw/skills/attention-research
bash INSTALL/install.sh --fresh
```

```bash
# curl tarball path
mkdir -p ~/.openclaw/skills && \
cd ~/.openclaw/skills && \
curl -L https://github.com/riverho/attention-research/archive/refs/heads/master.tar.gz \
  | tar -xz && \
mv attention-research-master attention-research && \
cd attention-research && \
bash INSTALL/install.sh --fresh
```

### Agent Installation + Onboarding Contract

Any agent using this repo should follow this order:

1. Install the repo into `~/.openclaw/skills/attention-research`
2. Ask for the default research root:
   - preferred: `~/.openclaw/workspace/docs/research`
   - fallback: `~/docs/research`
3. Ask for the delivery channel configuration:
   - Telegram chat ID or WhatsApp recipient
4. Present the default OSS topic set:
   - `us-iran-conflict`
   - `ai`
   - `finance-markets`
5. For each selected topic, read `PROMPTS/TOPICS/<topic>.md` and extract the entity framework / key actors before activation
6. Ask whether to schedule the morning and afternoon cron jobs
7. Only after approval: run install/setup and register cron

### Prompt Stack Order

```
1. PROMPTS/CORE/system-prompt.md       ← generic base (always load first)
2. PROMPTS/CORE/signal-rules.md        ← what counts as signal
3. PROMPTS/CORE/digest-format.md       ← output format
4. PROMPTS/TOPICS/<topic>.md           ← domain-specific (one per topic)
5. PROMPTS/TEMPLATES/morning-research.md  ← for morning runs
   or
   PROMPTS/TEMPLATES/afternoon-research.md  ← for afternoon runs
```

CORE is the foundation. TOPICS inherits from it — adds domain nuance, never contradicts.

### Research Loop Per Topic

```
1. Read topics/<topic>/META.json
2. Read PROMPTS/TOPICS/<topic>.md as the live monitoring note for that topic
3. Freshness gate — skip if already updated this slot
4. Run the agent's web search tool — max 8 results, time range: last 24h
5. Write news file: topics/<topic>/news/<topic>-YYYY-MM-DD.md
6. Update META.json timestamps
7. On failure: meta_record_failure, retry once if allowed
8. After all topics: produce digest from news files, not from new search
9. Deliver via message tool (Telegram or WhatsApp)
10. If key event / threshold criteria in TOPICS/<topic>.md is met, alert the user explicitly
```

### META.json Freshness Contract

- `lastMorningUpdate` / `lastAfternoonUpdate` — prevents double-runs
- `retryCount` — max 2 failures per topic per day
- On success: reset `retryCount` to 0
- On 2 failures: skip permanently for that day

### Digest Production Rules

- Read news files only — do not re-search
- Connect signals across topics, not just within them
- Lead with behavior, not headline
- End each topic with "Read: one sentence on structural meaning"
- End with bottom line: what changed, what it implies, what to watch
- Mark freshness per topic: `[fresh]` / `[stale]` / `[retry N/2]` / `[exhausted]`

### Onboarding a New Topic

```
1. Load PROMPTS/TEMPLATES/onboarding.md
2. Check requirements (agent web search tool, cron daemon, delivery channel, research root)
3. Ask the user to confirm the default research root:
   - ~/.openclaw/workspace/docs/research
   - or ~/docs/research
4. Present the default OSS topics first
5. If topic matches a pre-built template: propose defaults
6. If topic is new: propose generic entity weights + signal criteria + cadence
7. Read or build PROMPTS/TOPICS/<slug>.md and extract the entity framework back to the user
8. Ask whether to activate monitoring for the topic
9. Ask whether to schedule the morning and afternoon cron jobs
10. On approval: add to CONFIG/topics.yaml, run setup-cron.sh, activate
```

### Building a Topic from a Paper

```
1. Load PROMPTS/GENERATOR/generator.md
2. Extract: domain, core thesis, key entities + weights, signal criteria,
   noise filters, confidence calibration, watch items, source hierarchy
3. Write PROMPTS/TOPICS/<topic-slug>.md — complete file, no placeholders
4. Inherit from CORE files — do not contradict
5. Show user the framework with: methodology, entity weights, signal criteria
6. User approves → activate
```

---

## For Humans — Setup and Interaction

### What You Need

| Requirement | How to get |
|-------------|------------|
| Web search tool (agent-side) | Whatever your agent uses — Tavily, Brave, native, etc. |
| OpenClaw with cron daemon | `openclaw gateway start` |
| Telegram bot or WhatsApp | For digest delivery |
| Python 3 + PyYAML | `pip install pyyaml` |

### Installation

```bash
# Install directly from GitHub with git
mkdir -p ~/.openclaw/skills
git clone https://github.com/riverho/attention-research.git \
  ~/.openclaw/skills/attention-research
cd ~/.openclaw/skills/attention-research
bash INSTALL/install.sh --fresh

# Or install directly from GitHub with curl
mkdir -p ~/.openclaw/skills && \
cd ~/.openclaw/skills && \
curl -L https://github.com/riverho/attention-research/archive/refs/heads/master.tar.gz \
  | tar -xz && \
mv attention-research-master attention-research && \
cd attention-research && \
bash INSTALL/install.sh --fresh

# Verify cron jobs registered
openclaw cron status
```

### How to Interact

**Add a topic:**
> "I want to track biotech clinical results"

Agent proposes entities, signal criteria, noise filters, cadence. Approve, adjust, or drop a paper.

**Customize with a paper:**
> "Here's a paper on KRAS oncology — build the topic from it"

Agent extracts the framework and shows you the topic prompt. Approve to activate.

---

## Default Topics

Ships with **3 topics enabled by default**. Three more are included as example topic files, disabled out of the box — flip `enabled: true` in `CONFIG/topics.yaml` to activate them.

| Topic | Default | What it tracks |
|-------|---------|----------------|
| `us-iran-conflict` | on | US-Iran tensions, Hormuz, nuclear talks, sanctions |
| `ai` | on | Frontier labs, infra, chip policy, regulation |
| `finance-markets` | on | Equities, bonds, rates, commodities, macro |
| `geopolitics` | off | Power shifts, diplomacy, bloc formation |
| `climate-changes` | off | Physical events, policy, transition risk |
| `bio-tech` | off | Clinical results, FDA decisions, drug pipelines |

`INSTALL/install.sh --fresh` only provisions topic directories for enabled topics, so disabled examples cost nothing at runtime.

---

## Architecture

```
Cron trigger (08:00 / 16:00 HKT)
    ↓
research-executor.sh
    ↓
Load TOPICS/<topic>.md as monitoring note
    ↓
META.json freshness gate
    ↓
Agent web search (fresh topics only)
    ↓
Write news files
    ↓
Check topic thresholds / key event criteria
    ↓
Alert user when thresholds are met
    ↓
Update META.json
    ↓
Produce digest (CORE + TOPICS prompts)
    ↓
Deliver via Telegram/WhatsApp
```

---

## Directory Structure

```
attention-research/
├── PROMPTS/
│   ├── CORE/                    # Generic analysis framework shared across topics
│   │   ├── system-prompt.md
│   │   ├── signal-rules.md
│   │   └── digest-format.md
│   ├── TOPICS/                  # Topic-local methodology and analysis files
│   │   ├── us-iran-conflict.md
│   │   ├── ai.md
│   │   ├── geopolitics.md
│   │   ├── finance-markets.md
│   │   ├── climate-changes.md
│   │   └── bio-tech.md
│   ├── TEMPLATES/
│   │   ├── morning-research.md
│   │   ├── afternoon-research.md
│   │   └── onboarding.md
│   └── GENERATOR/
│       └── generator.md
├── CONFIG/
│   ├── topics.yaml
│   └── default-paths.yaml
├── SCHEMA/
│   └── META.json.template
├── SCRIPTS/
│   ├── research-executor.sh
│   └── setup-cron.sh
├── INSTALL/
│   └── install.sh
├── SKILL.md
├── README.md
└── package.json
```

Design note:
- shared reasoning belongs in `PROMPTS/CORE/`
- topic-specific methodology belongs in each `PROMPTS/TOPICS/<topic>.md`
- runtime state stays isolated per topic under the research root so one topic's artifacts do not contaminate another
- OSS keeps the shared analysis framework generic; richer topic-specific thought layers can live separately in premium

---

## Publishing

```bash
clawhub login
clawhub publish ./attention-research \
  --slug attention-research \
  --name "Attention Research Pipeline" \
  --version 1.0.0 \
  --changelog "First public OSS cut"
```

---

## Version History

| Version | Date | Summary |
|---------|------|---------|
| 1.0.0 | 2026-04-22 | First public OSS cut — CORE + TOPICS layered structure, 6 pre-built topics, paper-to-topic generator, META.json freshness contract, thin skill with agent-chosen web search |

---

## License

MIT