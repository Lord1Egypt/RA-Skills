# ClawDocx skill for OpenClaw

Install from ClawHub with `openclaw skills install @clawdocx/clawdocx` (OpenClaw's documented form is `openclaw skills install @owner/<slug>`; adjust the owner/slug if the published ClawHub listing differs). Add `--global` to install into the managed root `~/.openclaw/skills/` for all local agents instead of just the active workspace. Or copy this folder manually into the workspace skills folder, `~/.openclaw/workspace/skills/clawdocx/`. Then add the MCP server entry from SKILL.md to `openclaw.json` under `mcp.servers` and restart the gateway. Get a member key at https://app.clawdocx.com/account. Setup for other clients: https://clawdocx.com/agents

SKILL.md's frontmatter follows the schema documented at https://docs.openclaw.ai/tools/creating-skills (cross-checked against https://docs.openclaw.ai/tools/skills), not this site's own stale skill-writing guide.

## Publishing (ClawDocx team)

Publishing to ClawHub goes through the standalone ClawHub CLI, not `openclaw skills publish`: install it with `npm i -g clawhub`, run `clawhub login` once, then from the repo root:

    clawhub skill publish packages/clawhub-skill/clawdocx --owner clawdocx --changelog "initial release"

Add `--dry-run` first to rehearse the publish without uploading. The slug is derived from the folder name, so the folder must stay named `clawdocx`, and the `clawdocx` publisher handle must already be registered on ClawHub before the first publish. `tools/creating-skills` and `tools/skills` describe what the OpenClaw gateway parses at load time; `clawhub/skill-format` describes what the publish flow additionally extracts — the two doc sets are complementary, not conflicting. Versions are assigned by the `clawhub` CLI itself (new skills publish as `1.0.0`, then the next patch each time), so this package keeps no `version` field in frontmatter.

Sources: https://docs.openclaw.ai/tools/skills, https://docs.openclaw.ai/cli/skills, https://docs.openclaw.ai/clawhub, https://docs.openclaw.ai/clawhub/cli, https://docs.openclaw.ai/clawhub/skill-format
