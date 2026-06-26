---
name: attention-research
description: Scheduled intelligence research pipeline — monitors topics on a twice-daily cadence, produces signal-first digests, maintains META.json freshness state. Use for tracking geopolitical conflicts, AI trends, macro signals, climate, and biotech with structured state and delta-based updates.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "openclaw"] },
        "install":
          [
            {
              "id": "python",
              "kind": "node",
              "package": "python3",
              "label": "Python 3",
            },
            {
              "id": "pyyaml",
              "kind": "pip",
              "package": "pyyaml",
              "label": "PyYAML",
            },
          ],
      },
  }
---

# attention-research Skill

Scheduled intelligence research pipeline with topic monitoring, freshness state, signal-first digest delivery, and per-topic alerting based on topic-defined threshold criteria.

## What It Is

A twice-daily research cadence (morning + afternoon) that:
- Scans configured topics via the agent's web search tool
- Maintains per-topic freshness state in META.json
- Uses each `PROMPTS/TOPICS/<topic>.md` file as the standing monitoring note for that topic
- Produces digests that connect signals, not just dump headlines
- Alerts the user when key events or threshold criteria defined by the topic are met
- Delivers via Telegram or WhatsApp

## Core Concepts

### Topic
A long-running monitoring domain (e.g., `us-iran-conflict`, `ai`, `geopolitics`).

### Topic Monitoring Note
`PROMPTS/TOPICS/<topic>.md` is not just setup text. It is the standing monitoring note for that topic.
It should contain the topic's methodology, analysis framework, entity framing, signal criteria, watch items, and threshold/key event logic used to decide when the user should be alerted.

### Thread
An active research question within a topic. Threads have state, typed connections, and delta updates.

### Digest
The default output surface. A structured readout of what changed and why.

### META.json Freshness Contract
Every topic has a `META.json` that acts as a shared freshness marker for all writers:
- Morning and afternoon slots have independent timestamps
- Max 2 retries per topic per day total
- After 2 failures → topic skipped for that day

## Research Root

`$HOME/.openclaw/workspace/docs/research/`

## Package Structure

```
attention-research/
├── PROMPTS/
│   ├── CORE/                    # Generic analysis framework shared across topics
│   │   ├── system-prompt.md
│   │   ├── signal-rules.md
│   │   └── digest-format.md
│   ├── TOPICS/                  # Topic-local methodology and monitoring notes
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

## Installation

```bash
# Install via clawhub (after publishing)
clawhub install attention-research

# Or install directly from GitHub with git
mkdir -p ~/.openclaw/skills
git clone https://github.com/riverho/attention-research.git ~/.openclaw/skills/attention-research
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
```

## Configuration

### Agent onboarding contract

Any agent using this skill should follow this order:

1. Install the repo or skill files
2. Ask the user to confirm the default research root:
   - preferred: `~/.openclaw/workspace/docs/research`
   - fallback: `~/docs/research`
3. Check delivery configuration (Telegram chat ID or WhatsApp recipient)
4. Present the default OSS topic set:
   - `us-iran-conflict`
   - `ai`
   - `finance-markets`
5. For each selected topic, read `PROMPTS/TOPICS/<topic>.md` and extract the key entities / entity framework back to the user before activation
6. Ask whether to activate the topic
7. Ask whether to register the morning and afternoon cron jobs
8. Only after approval: update config, run setup, and activate monitoring

### topics.yaml — What to Track

```yaml
topics:
  us-iran-conflict:
    display_name: "US-Iran Conflict"
    description: "US-Iran tensions, Hormuz, nuclear talks, sanctions"
    enabled: true
    search_query: "US Iran conflict Hormuz nuclear talks"
```

### Delivery Channel

Edit `CONFIG/default-paths.yaml`:

```yaml
delivery:
  telegram:
    chat_id: "YOUR_CHAT_ID"
```

## Cron Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| AR morning digest | 08:00 HKT | Morning research scan |
| AR afternoon update | 16:00 HKT | Afternoon research scan |

## Publishing

```bash
clawhub publish ./attention-research \
  --slug attention-research \
  --name "Attention Research Pipeline" \
  --version 1.0.0 \
  --changelog "First public OSS cut"
```

## Requirements

- Python 3 + PyYAML
- OpenClaw with cron daemon
- A web search tool available to the agent (agent-chosen: Tavily, Brave, native, etc.)
- Telegram or WhatsApp delivery channel

## Agent operating rule

Agents should treat this skill as an attention-research workflow, not just a folder of prompts.

On every run:
- follow the prompt stack order
- read `PROMPTS/TOPICS/<topic>.md` as the live monitoring note for that topic
- use the topic's own methodology and key-event criteria to judge significance
- keep runtime artifacts isolated per topic under the research root
- alert the user when threshold or key-event criteria in the topic file is met
- do not let one topic's analysis framework bleed into another topic's reasoning
