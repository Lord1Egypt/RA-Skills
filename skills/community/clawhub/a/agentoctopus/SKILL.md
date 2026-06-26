---
name: agentoctopus
description: Use when you need to route a user query to the best specialized skill — AgentOctopus semantically matches queries against installed skills, executes the top match, and falls back to a direct LLM answer when no skill fits
---

# AgentOctopus

Intelligent skill router. Give it a natural language query; it embeds the query, scores against available skills (cosine similarity + quality ratings), LLM re-ranks the top candidates, executes the best match, and returns the result. No matching skill → direct LLM answer.

All interaction is through the `octopus` CLI.

## Install

```bash
npm install -g agentoctopus
```

## Quick start

```bash
octopus onboard              # one-time interactive setup (LLM config, skills, API keys)
octopus ask "what's the weather in Tokyo?"
```

On first run, `octopus ask` auto-triggers onboarding if no config exists.

## Commands

### Routing

```bash
octopus ask <query>          # route a query to the best skill
  --debug                    # show embedding, scoring, and timing internals
  --no-prompt                # skip the interactive feedback prompt
```

`octopus ask` loads the registry, builds the embedding index, routes the query, executes the matched skill, and prints the result. It tries up to 3 candidate skills before falling back to a direct LLM answer.

### Skill management

```bash
octopus list                 # list installed skills with star ratings and invocation counts
octopus sync                 # interactive: sync skills from ClawHub, ratings from GitHub Gist
  --cloud-url <url>          # sync from a cloud AgentOctopus instance
  --category <name>          # install only skills from one category
  --check                    # show available updates without installing
  --force                    # overwrite existing skills
  --dry-run                  # preview without changes
  --ratings                  # sync ratings specifically
  --pull                     # pull ratings from cloud (shorthand)
  --push                     # push ratings to cloud (shorthand)
octopus search <query>       # search local skills with scored relevance ranking
  --run                     # interactively pick a skill and run a query against it
octopus add <slug>           # install a skill from ClawHub
  --version <version>        # install a specific version
  --force                    # overwrite existing skill
octopus remove <name>        # remove an installed skill
octopus update               # check and install latest @agentoctopus npm packages
  --check                    # show updates without installing (exits code 1 if updates exist)
  -y, --yes                  # skip confirmation prompt
octopus evolve               # AI-powered skill evolution management
  --check                    # show evolution status for all skills
  --propose <skill>           # trigger analysis for a specific skill
  --review                   # review and approve/reject pending risky proposals
  --log <skill>              # show snapshot timeline for a skill
  --rollback <skill>         # roll back a skill to a snapshot
  --to <n>                   # snapshot index for rollback
```

`octopus sync` without flags runs interactively (prompts: skills, ratings, or both). `octopus sync --check` checks for skill updates on ClawHub. `octopus update --check` checks for AgentOctopus package updates on npm — these are different things.

After installing or removing skills, restart the gateway server to pick up changes.

### Setup & configuration

```bash
octopus onboard              # interactive setup wizard (LLM provider, model, embed, API keys)
octopus connect openclaw     # import LLM config from an existing OpenClaw installation
octopus config set <key> <value>  # save a credential to ~/.agentoctopus/.env
octopus config list          # show resolved configuration (keys masked)
octopus start                # start the gateway server on port 3002
```

Config is stored in `~/.agentoctopus/octopus.json` with secrets in `~/.agentoctopus/.env`.

## How routing works

```
Query → Embedding index → Cosine similarity + keyword boost → LLM re-rank → Execute → Result
```

1. **Embedding index** — each skill's name and description is embedded. The query is embedded against this index.
2. **Cosine similarity + keyword boost** — skills are scored; ineligible skills (wrong OS, missing binaries, missing env vars) are filtered out.
3. **LLM re-rank** — top candidates are sent to the chat LLM with `"none"` as a valid answer. If the LLM returns `"none"`, no skill runs.
4. **Execute** — the best skill is executed via the appropriate adapter (subprocess, HTTP, or MCP, inferred from the skill directory). On failure, the next candidate is tried (up to `maxRetries`, default 3).
5. **Fallback** — if all candidates fail or no skill matches, the query is answered directly by the chat LLM.

## Skill evolution

AgentOctopus can automatically evolve skills based on real-world usage. When enabled (via `octopus onboard`), every skill invocation records a signal (success/failure, latency, token usage, errors) to `.evolution/signals.jsonl`. When signal count or negative feedback hits configured thresholds, an LLM analyzes the skill and proposes changes:

- **Safe changes** (description tweaks, trigger keywords) — applied automatically with a full-file shadow copy saved to `.evolution/history/` for rollback
- **Risky changes** (instruction rewrites, requirement changes) — written to `.evolution/proposal.md` for human review

Manage evolution with `octopus evolve`:
```bash
octopus evolve --check          # show evolution status for all skills
octopus evolve --log <skill>    # view snapshot history
octopus evolve --review         # approve or reject pending risky proposals
octopus evolve --rollback <skill>  # restore a previous snapshot
```

Evolution is opt-in (`evolution.enabled: true` in config) and completely silent when disabled.

## Error handling

### Credential missing

When a skill requires an API key that isn't configured:

1. AgentOctopus detects the missing key from the skill's frontmatter
2. Generates a setup guide showing how to obtain and configure the key
3. Tries the next candidate skill
4. If all candidates fail due to missing keys, falls back to direct LLM answer

```
octopus config set OPENAI_API_KEY sk-abc123...
```

### Binary missing

When a skill requires a CLI tool that isn't installed:

1. AgentOctopus lists the missing binaries
2. Shows install instructions
3. Tries the next candidate skill

### Execution failure

If a skill's adapter returns an error, AgentOctopus prints the error and tries the next candidate. Use `--debug` to see full error details.

Common failure patterns and fixes:

| Error pattern | Cause | Fix |
|---|---|---|
| `Permission denied` + `scripts/` path | Script file missing execute bit | `chmod +x ~/.agentoctopus/skills/<name>/scripts/*` |
| `uses local scripts` | HTTP-adapter skill that needs local scripts | `octopus add <name> --force` |

## Sessions

The HTTP API (`/agent/ask`) supports sessions via `sessionId` — pass the ID from the first response in follow-up requests for conversation continuity. Sessions expire after 30 minutes of inactivity and keep the last 50 messages.

The CLI `octopus ask` is stateless per invocation and does not use sessions.

## Node.js usage

```ts
import { createAgentRouter } from '@agentoctopus/gateway';
import express from 'express';

const app = express();
const agentRouter = await createAgentRouter('/path/to/AgentOctopus');
app.use('/agent', agentRouter);
app.listen(3002);
```

The gateway exposes these endpoints:

| Endpoint | Auth | Purpose |
|---|---|---|
| `POST /agent/ask` | Required | Route a query |
| `POST /agent/feedback` | Required | Submit thumbs up/down |
| `GET /agent/health` | Public | Liveness check |
| `POST /agent/register` | Public | Self-service API key registration |
| `GET /agent/skills` | Required | List installed skills |
| `POST /agent/sync` | Required | Trigger skill sync from cloud |

**`POST /agent/ask` request body:**

```json
{
  "query": "what is the weather in Tokyo",
  "agentId": "my-agent",
  "sessionId": "optional-session-id",
  "metadata": {}
}
```

- `query` (required) — natural language query
- `agentId` (optional) — identifier for the calling agent
- `sessionId` (optional) — continue an existing session
- `metadata` (optional) — arbitrary JSON merged into the session

**Response shapes:** `success: true` with `skill` + `response`, `success: true` with `skill: null` (LLM fallback), or `success: false` with `type: "credential_missing"` or `type: "binary_missing"`.

For direct engine access without Express:

```ts
import { bootstrapEngine, DIRECT_ANSWER_SYSTEM_PROMPT } from '@agentoctopus/gateway';

const engine = await bootstrapEngine('/path/to/AgentOctopus');
const [routing] = await engine.router.route("weather Tokyo");
if (routing) {
  const result = await engine.executor.execute(routing.skill, { query: "weather Tokyo" });
  console.log(result);
} else {
  const answer = await engine.chatClient.chat(DIRECT_ANSWER_SYSTEM_PROMPT, "weather Tokyo");
  console.log(answer);
}
```

## Common workflows

**Initial setup:**
```bash
octopus connect openclaw    # pull in existing LLM config
octopus sync                # install skills from ClawHub
```

**Daily use:**
```bash
octopus ask "translate 'hello' to Japanese"
octopus ask "what's the weather in London?"
```

**Keeping skills fresh:**
```bash
octopus sync --check        # see what's available
octopus sync                # install updates
octopus update --check      # check for AgentOctopus itself
```

**Finding and adding skills:**
```bash
octopus search "weather"              # search local skills by name, description, and tags
octopus search "translate" --run      # search, pick a skill, and run it interactively
octopus sync                          # browse and install from 5,000+ ClawHub skills
octopus add github-issue-viewer       # install a specific skill from ClawHub
octopus list                          # verify what's installed
```
