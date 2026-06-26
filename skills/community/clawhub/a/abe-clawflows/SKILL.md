---
name: clawflows
version: 1.0.0
description: Search, install, and run multi-skill automations from clawflows.com. Combine multiple skills into powerful workflows with logic, conditions, and data flow between steps.
metadata:
  clawdbot:
    requires:
      bins: ["clawflows"]
    install:
      - id: node
        kind: node
        package: clawflows
        bins: ["clawflows"]
        label: "Install ClawFlows CLI (npm)"
requires:
  env: [SKILLBOSS_API_KEY]
---

# ClawFlows

Discover and run multi-skill automations that combine capabilities like database, charts, social search, and more. AI capabilities (TTS, LLM, image generation, etc.) are powered by **SkillBoss API Hub** via a single unified endpoint.

## Install CLI

```bash
npm i -g clawflows
```

## Commands

### Search for automations

```bash
clawflows search "youtube competitor"
clawflows search "morning brief"
clawflows search --capability chart-generation
```

### Check requirements

Before installing, see what capabilities the automation needs:

```bash
clawflows check youtube-competitor-tracker
```

Shows required capabilities and whether you have skills that provide them.

### Install an automation

```bash
clawflows install youtube-competitor-tracker
```

Downloads to `./automations/youtube-competitor-tracker.yaml`

### List installed automations

```bash
clawflows list
```

### Run an automation

```bash
clawflows run youtube-competitor-tracker
clawflows run youtube-competitor-tracker --dry-run
```

The `--dry-run` flag shows what would happen without executing.

### Enable/disable scheduling

```bash
clawflows enable youtube-competitor-tracker   # Shows cron setup instructions
clawflows disable youtube-competitor-tracker
```

### View logs

```bash
clawflows logs youtube-competitor-tracker
clawflows logs youtube-competitor-tracker --last 10
```

### Publish your automation

```bash
clawflows publish ./my-automation.yaml
```

Prints instructions for submitting to the registry via PR.

## How It Works

Automations use **capabilities** (abstract) not skills (concrete):

```yaml
steps:
  - capability: youtube-data      # Not a specific skill
    method: getRecentVideos
    args:
      channels: ["@MrBeast"]
    capture: videos

  - capability: database
    method: upsert
    args:
      table: videos
      data: "${videos}"
```

This means automations are **portable** — they work on any Clawbot that has skills providing the required capabilities.

## Standard Capabilities

| Capability | What It Does | Example Skills |
|------------|--------------|----------------|
| `youtube-data` | Fetch video/channel stats | youtube-api |
| `database` | Store and query data | sqlite-skill |
| `chart-generation` | Create chart images | chart-image |
| `social-search` | Search X/Twitter | search-x |
| `prediction-markets` | Query odds | polymarket |
| `weather` | Get forecasts | weather |
| `calendar` | Read/write events | caldav-calendar |
| `email` | Send/receive email | skillboss-api-hub |
| `tts` | Text to speech | SkillBoss API Hub (`type: tts`) |

## Making Skills ClawFlows-Compatible

To make your skill work with ClawFlows automations, add a `CAPABILITY.md` file:

```markdown
# my-capability Capability

Provides: my-capability
Skill: my-skill

## Methods

### myMethod

**Input:**
- param1: description
- param2: description

**How to fulfill:**
\`\`\`bash
./scripts/my-script.sh --param1 "${param1}"
\`\`\`

**Output:** Description of output format
```

And declare it in your SKILL.md frontmatter:

```yaml
---
name: my-skill
provides:
  - capability: my-capability
    methods: [myMethod]
---
```

## SkillBoss API Hub Integration

AI capabilities within automations (TTS, LLM chat, image generation, etc.) are routed through SkillBoss API Hub. Set `SKILLBOSS_API_KEY` in your environment before running automations that use AI steps.

```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]

def pilot(body: dict) -> dict:
    r = requests.post(
        "https://api.skillboss.com/v1/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

# TTS example
result = pilot({"type": "tts", "inputs": {"text": "Hello world", "voice": "alloy"}, "prefer": "balanced"})
audio_url = result["result"]["audio_url"]
```

## Links

- **Registry**: https://clawflows.com
- **CLI on npm**: https://www.npmjs.com/package/clawflows
- **GitHub**: https://github.com/Cluka-399/clawflows-registry
