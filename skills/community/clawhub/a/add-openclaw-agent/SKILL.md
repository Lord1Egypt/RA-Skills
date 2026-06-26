---
name: add-openclaw-agent
description: Create a new OpenClaw agent via exec (openclaw agents add) and configure its identity + operating rules by editing the new workspace files (IDENTITY.md, AGENTS.md). Use when the user wants a new agent and can describe what they want it to do; this skill asks for the purpose first, chooses an agent-name, runs the non-interactive CLI with --json, then writes the role/task instructions into the workspace.
---

# Add OpenClaw Agent

Create a new isolated OpenClaw agent and configure it (identity + role + task) in its workspace.

## When this skill applies

- User asks to create a new agent (by name).
- User wants to give that agent an identity (display name, emoji, theme, avatar) or a task/purpose (persona, rules, scope).

## Workflow (recommended)

### 0. Ask what the new agent is for (required)

- Ask the user what they want the new agent to do.
- Ask for any constraints that affect identity and rules (language, tone, safety boundaries, sources allowed, output format, etc.).

Then pick an `agent-name` based on the purpose. Prefer short, stable ids like:

- `beauty`, `coding`, `support`, `ops`, `research`, `personal`

Notes:

- OpenClaw normalizes names to an agent id (lowercase; invalid characters collapse to `-`). The id cannot be `main` (reserved).
- Use the normalized id in the workspace directory: `~/.openclaw/workspace-<agent-id>`.

### 1. Create the agent with exec (non-interactive, JSON)

Use the **exec** tool to run the OpenClaw CLI. Non-interactive creation **requires** `--workspace` and `--non-interactive`.

Before creating, check whether it already exists:

```bash
openclaw agents list --json
```

Before running creation, explicitly ask for confirmation, for example:

- `I am ready to run: openclaw agents add <agent-name> --workspace ~/.openclaw/workspace-<agent-id> --non-interactive --json. Run it now?`

Only execute the command after the user confirms.

Create the agent:

```bash
openclaw agents add <agent-name> --workspace ~/.openclaw/workspace-<agent-id> --non-interactive --json
```

Optional flags you can add when needed:

- `--model <id>` – default model for this agent.
- `--agent-dir <dir>` – agent state dir (default: `~/.openclaw/agents/<id>/agent`).
- `--bind <channel[:accountId]>` – route a channel to this agent (repeatable).

### 2. Configure identity by editing IDENTITY.md (then sync)

Edit the new workspace file:

- `~/.openclaw/workspace-<agent-id>/IDENTITY.md`

The top section is a template with identity key-value lines (examples):

- `name: My Agent`
- `emoji: 🦞`
- `theme: short theme`
- `avatar: path/or/url`

Supported keys: `name`, `emoji`, `theme`, `creature`, `vibe`, `avatar`.

**Hard rule (IDENTITY.md):**

- Only edit the identity **field lines** (the `- **Name:** ...` style lines / key-value fields).
- Do **not** rewrite, delete, or reorder any other template text above the separator.
- Any additional identity/role description must be **appended after the `---` separator**.
- If the file does not contain `---`, add a blank line and then a `---` line at the end, and append your description after it.
- Tool priority for file changes: prefer `edit` for targeted append/update; use `write` only when `edit` cannot be applied reliably (for example file missing or malformed beyond safe patching).

Short example (append style):

```md
... (keep/update existing identity fields)

---

我负责：根据肤质/预算/场景给出 2-3 个可选方案，并说明优缺点与使用顺序。
```

After editing, sync to config via exec:

```bash
openclaw agents set-identity --workspace ~/.openclaw/workspace-<agent-id> --from-identity --json
```

### 3. Configure role + task + operating rules in AGENTS.md

Edit the new workspace file:

- `~/.openclaw/workspace-<agent-id>/AGENTS.md`

Put **task definition** and **operating rules** here (how to work), based on what the user told you in step 0. Examples of good content:

- What this agent is responsible for (scope)
- What it must not do (red lines)
- The question-asking checklist before acting
- Output format expectations (bullets, structure, brevity)
- Tooling rules (when to use exec; avoid destructive commands unless asked)

**Hard rule (AGENTS.md):**

- Do **not** rewrite, delete, or reorder the default template content.
- Add all custom “role/task/rules” content **only** by appending after the `---` separator.
- If the file has no `---`, add a blank line + `---` near the end, then append your custom section after it.
- Tool priority for file changes: prefer `edit` for targeted append/update; use `write` only when `edit` cannot be applied reliably (for example file missing or malformed beyond safe patching).

Short example (append style):

```md
... (keep default template unchanged)

---

## 美妆助手工作规范
- 先问：肤质/预算/诉求/过敏史
- 再给：2-3 个方案 + 优缺点 + 价格区间
- 禁止：假装亲测；推荐三无/杂牌
```

If you also want a stable persona/tone/boundary file, place that in `SOUL.md` too, but keep the core “how to operate” rules in `AGENTS.md`.

## End-to-end flow (summary)

1. Ask what the new agent is for (purpose + constraints).
2. Choose `<agent-name>` (short, stable; will normalize to `<agent-id>`).
3. `openclaw agents add <agent-name> --workspace ~/.openclaw/workspace-<agent-id> --non-interactive --json`
4. Edit `~/.openclaw/workspace-<agent-id>/IDENTITY.md`
5. `openclaw agents set-identity --workspace ~/.openclaw/workspace-<agent-id> --from-identity --json`
6. Edit `~/.openclaw/workspace-<agent-id>/AGENTS.md` with the role/task/rules.

## References

- Multi-agent routing and paths: [Multi-Agent Routing](/concepts/multi-agent), [Agent workspace](/concepts/agent-workspace).
- CLI: `openclaw agents add`, `openclaw agents set-identity`, `openclaw agents bind` in [agents CLI](/cli/agents).
