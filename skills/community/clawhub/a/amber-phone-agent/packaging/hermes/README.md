# Amber for Hermes Agent

This directory packages Amber as a Hermes-compatible AgentSkill wrapper.

Amber's phone runtime remains the same platform-agnostic Node service. Hermes integration happens through:

1. this `SKILL.md`, installed under `~/.hermes/skills/amber-phone-agent/`
2. Amber's existing MCP server at `runtime/dist/mcp-server.js`
3. a Hermes `mcp_servers` config entry pointing at that MCP server

## Local install

From the Amber repo:

```bash
mkdir -p ~/.hermes/skills/amber-phone-agent
cp packaging/hermes/SKILL.md ~/.hermes/skills/amber-phone-agent/SKILL.md
```

Then add the MCP snippet from `mcp_servers.yaml` to your Hermes config, changing paths as needed.

## Publish path

HermesHub appears to install skills from GitHub paths, for example:

```bash
hermes skills install github:<owner>/<repo>/skills/<skill-name>
```

For publishing, the cleanest structure is to expose this directory, or a copy of it, at a stable repo path such as:

```text
skills/amber-phone-agent/SKILL.md
```

If HermesHub requires contribution via PR to `amanning3390/hermeshub`, copy this skill directory into that repository's `skills/amber-phone-agent/` path and include security notes about Twilio/OpenAI, local logs, CRM, calendar, and MCP tool confirmation.
