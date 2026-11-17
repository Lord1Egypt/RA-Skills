# Cliphi skill

Teach any agent to turn the user's long videos into ready-to-post vertical clips
with captions and branding, via the [Cliphi](https://www.cliphi.com) API.

- **Skill file:** [`SKILL.md`](./SKILL.md) (AgentSkills standard)
- **Requires:** a Cliphi API key in `CLIPHI_API_KEY`
  (create one at https://www.cliphi.com/studio/settings/api-keys)
- **Try without a key:** `curl https://www.cliphi.com/api/v1/demo`
- **API reference:** https://www.cliphi.com/cliphi-actions.json
- **MCP server** (if your agent speaks MCP instead):
  `https://www.cliphi.com/api/mcp` — chat clients sign in via OAuth when
  they connect; CLIs can send the same key as a bearer token

Submitting a job bills a small per-minute processing charge; previews are
free; rendering is the discretionary spend and always states its cost
first. The skill bakes in previews-first and confirm-before-render.

This skill calls only `https://www.cliphi.com`: no installers, no scripts,
no dependencies.

License: MIT-0.
