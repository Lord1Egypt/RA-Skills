# Enrich Layer — OpenClaw Skill

An OpenClaw skill that wraps the [Enrich Layer MCP server](https://github.com/enrichlayer/mcp-server), providing 25 tools for company, person, contact, school, and job data enrichment.

## Local Installation

Copy the `openclaw` directory into your OpenClaw skills folder:

```bash
# Workspace-level (current project only)
cp -r connectors/openclaw ./skills/enrich-layer

# User-level (available to all agents)
cp -r connectors/openclaw ~/.openclaw/skills/enrich-layer
```

Then set your API key:

```bash
export ENRICH_LAYER_API_KEY=your_api_key_here
```

Get your API key at [enrichlayer.com/dashboard](https://enrichlayer.com/dashboard).

## Publishing to ClawHub

### Prerequisites

1. Install the ClawHub CLI (ships with OpenClaw, or install standalone):
   ```bash
   clawhub login
   clawhub whoami
   ```

2. Ensure your `SKILL.md` is in a directory named with a valid slug (lowercase, URL-safe):
   ```
   enrich-layer/
   └── SKILL.md
   ```

### Publish

From the skill directory:

```bash
cd connectors/openclaw
clawhub publish .
```

This creates version `0.2.0` on ClawHub. The `description` from the SKILL.md frontmatter becomes the skill summary in search results.

### Update

To publish a new version, bump the `version` field in SKILL.md frontmatter and run:

```bash
clawhub publish .
```

### Verify

After publishing, confirm it is live:

```bash
clawhub inspect enrich-layer
```

Users can then install it with:

```bash
clawhub install enrich-layer
```

## MCP Server Configuration

The skill requires the Enrich Layer MCP server to be configured in OpenClaw's MCP settings. This is documented in the SKILL.md itself, but for reference:

```json
{
  "mcpServers": {
    "enrich-layer": {
      "command": "npx",
      "args": ["-y", "@verticalint-michael/enrich-layer-mcp"],
      "env": {
        "ENRICH_LAYER_API_KEY": "${ENRICH_LAYER_API_KEY}"
      }
    }
  }
}
```

## Links

- npm: [@verticalint-michael/enrich-layer-mcp](https://www.npmjs.com/package/@verticalint-michael/enrich-layer-mcp)
- GitHub: [enrichlayer/mcp-server](https://github.com/enrichlayer/mcp-server)
- API Docs: [enrichlayer.com/docs](https://enrichlayer.com/docs)
- Dashboard: [enrichlayer.com/dashboard](https://enrichlayer.com/dashboard)

## License

MIT-0 (per ClawHub publishing requirements).
