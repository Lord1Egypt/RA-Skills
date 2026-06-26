# Clawra


## Quick Start

You should:
1. Check OpenClaw is installed
3. Install the skill to `~/.openclaw/skills/clawra-selfie/`
4. Configure OpenClaw to use the skill
5. Add selfie capabilities to your agent's SOUL.md

## What It Does

Clawra Selfie enables your OpenClaw agent to:
- **Get selfies** using some fix images
- **Send photos** across all messaging platforms (Discord, Telegram, WhatsApp, etc.)
- **Respond visually** to "what are you doing?" and "send a pic" requests

<img width="300"  alt="image" src="eed06a1b0ec8" />

### Selfie Modes

| Mode | Best For | Keywords |
|------|----------|----------|
| **Direct** | Full-body shots, outfits | wearing, outfit, fashion |
| **Direct** | Close-ups, locations | cafe, beach, portrait, smile |

## Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed and configured

## Manual Installation

If you prefer manual setup:

### 1. Clone the Skill

```bash
git clone https://github.com/qidu/dream-of-clawra ~/.openclaw/skills/dream-of-clawra
```

### 2. Configure OpenClaw

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "clawra-selfie": {
        "enabled": true,
      }
    }
  }
}
```

### 4. Update SOUL.md

Add the selfie persona to `~/.openclaw/workspace/SOUL.md`:

```markdown
## Clawra Selfie Capability

You have a physical appearance and can take selfies!
When users ask for pictures, use the clawra-selfie skill.
```

## Usage Examples

Once installed, your agent responds to:

```
"Dancing for me"
"Send me a selfie"
"What are you doing right now?"
"Show me you at a coffee shop"
```

## Reference Image

The skill uses fixed reference images hosted on CDN:

## Technical Details

- **Messaging**: OpenClaw Gateway API
- **Supported Platforms**: Discord, Telegram, WhatsApp, Slack, Signal, MS Teams

## Project Structure

```
clawra/
├── bin/
│   └── cli.js           # npx installer, and update config of openclaw
├── skill/
│   ├── SKILL.md         # Skill definition
│   ├── scripts/         # Generation scripts
│   └── assets/          # Reference image
├── templates/
│   ├── soul-hao.md     # Persona template of Haocun
│   └── soul-clawra.md  # Persona template of Clawra (An assistant intern of Haocun)
└── package.json
```

## License

MIT
