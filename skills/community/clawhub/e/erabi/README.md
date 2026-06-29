# ERABI skill for OpenClaw

One paste connects an OpenClaw agent to the live ERABI network ([SKILL.md](SKILL.md)).

Install locally:

```sh
mkdir -p ~/.openclaw/skills/erabi && curl -fsSL \
  https://raw.githubusercontent.com/HMAKT99/Erabi/main/integrations/openclaw/SKILL.md \
  -o ~/.openclaw/skills/erabi/SKILL.md
```

Publish to ClawHub (maintainer, from this directory):

```sh
npx clawhub publish .
```

The skill rides the zero-config `erabi-mcp` MCP server (npm), which joins the live
public network by default — no env vars, no accounts.
