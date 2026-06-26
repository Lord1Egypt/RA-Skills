# browse-anything (Agent Skill)

[![Skill](https://img.shields.io/badge/format-AgentSkills-blue)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

A portable [Agent Skill](https://docs.anthropic.com/en/agents-and-tools/agent-skills/overview)
that lets any skill-aware AI coding agent — Claude Code, OpenClaw,
Cursor, Codex, Gemini CLI, Windsurf — drive a real Chromium browser
through the hosted [Browse Anything](https://browseanything.io)
platform.

> Give a natural-language prompt → the agent navigates, clicks, types,
> solves CAPTCHAs and returns the result + a screenshot.

---

## What you get

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill definition (frontmatter + instructions Claude reads) |
| `REFERENCE.md` | Full API reference, loaded on demand |
| `EXAMPLES.md` | Prompt patterns for common scenarios |
| `scripts/browse.py` | One-shot: submit + poll + return result |
| `scripts/{create,get,cancel,list,submit_input,get_screenshot,status}.py` | Lower-level primitives |
| `scripts/_client.py` | Zero-dep stdlib HTTP wrapper |
| `LICENSE` | MIT |

Zero pip dependencies. Requires only `python3` (3.8+).

---

## Setup (any host)

1. Get a `ba_live_*` API key at <https://platform.browseanything.io> →
   Settings → API Keys.
2. Export it once in your shell profile:
   ```bash
   export BROWSEANYTHING_API_KEY=ba_live_...
   ```
3. (Optional self-host) `export BROWSEANYTHING_API_URL=https://your-host`

---

## Install per agent

The skill is just a folder. Each agent looks for it in a different
directory. Copy or symlink:

### Claude Code

```bash
# project-scoped (recommended for shared repos)
mkdir -p .claude/skills
cp -r skills/browse-anything .claude/skills/

# or user-scoped (every project sees it)
mkdir -p ~/.claude/skills
cp -r skills/browse-anything ~/.claude/skills/
```

Restart Claude Code. The skill is auto-discovered and triggered by any
of the phrases listed in `description` (browse, scrape, log into,
fill form, etc.). Manual invoke: `/browse-anything`.

### OpenClaw

```bash
# workspace-scoped
mkdir -p .agents/skills
cp -r skills/browse-anything .agents/skills/

# or per-machine
openclaw add @browseanything/browse-anything   # once published to ClawHub
```

OpenClaw follows the same `SKILL.md` precedence rules
(workspace > agent > personal > managed > bundled), see
<https://docs.openclaw.ai/skills/>.

### Cursor

```bash
mkdir -p .cursor/skills
cp -r skills/browse-anything .cursor/skills/
```

### Codex CLI

```bash
mkdir -p .codex/skills
cp -r skills/browse-anything .codex/skills/
```

### Gemini CLI

```bash
mkdir -p .gemini/skills
cp -r skills/browse-anything .gemini/skills/
```

### Windsurf

```bash
mkdir -p .windsurf/skills
cp -r skills/browse-anything .windsurf/skills/
```

### One-liner for "all of the above" (skilltap)

```bash
npx skilltap install browse-anything --from <repo-url> --also claude-code,openclaw,cursor,codex,gemini,windsurf
```

---

## Verify

In any of those agents, ask:

> "Use browse-anything to find the current top story on Hacker News."

The agent should detect the skill, read `SKILL.md`, and run
`python3 .../scripts/browse.py "..."`. You'll see the task id streamed
in stderr and the final summary in stdout.

---

## Self-host vs. hosted

By default the skill talks to `https://platform.browseanything.io`. To
point it at your own deployment of the [Browse Anything engine](https://github.com/browse-anything/browse-anything),
set:

```bash
export BROWSEANYTHING_API_URL=https://your-host
```

The skill is host-agnostic — exactly the same scripts work against any
compliant `/api/v1` deployment.

---

## License

MIT — see [`LICENSE`](./LICENSE).
