---
title: "Automation, Delegation & Agents"
source:
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/quickstart
  - https://docs.github.com/en/copilot/concepts/agents/copilot-cli/autopilot
  - https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli
category: reference
---

Automation recipes, CI/CD, autopilot, `/delegate`, `/fleet`, and custom agents.

## Programmatic Recipes

```bash
# Minimal automation
copilot -p "PROMPT" --yolo --no-ask-user -s

# With specific permissions (preferred)
copilot -p "PROMPT" --allow-tool='shell(git:*), write' --no-ask-user -s

# Generate commit message
copilot -p 'Write a commit message for staged changes' -s --allow-tool='shell(git:*)'

# Write unit tests
copilot -p 'Write unit tests for src/utils/validators.ts' --allow-tool='write, shell(npm:*), shell(npx:*)'

# Code review a branch
copilot -p '/review changes on this branch vs main. Focus on bugs.' -s --allow-tool='shell(git:*)'

# Capture output
result=$(copilot -p 'Answer concisely.' -s)

# Batch processing
for file in src/api/*.ts; do
  copilot -p "Review $file" -s --allow-all-tools | tee -a review.md
done
```

## GitHub Actions Integration

```yaml
steps:
  - uses: actions/checkout@v5
    with:
      fetch-depth: 0
  - uses: actions/setup-node@v4
  - run: npm install -g @github/copilot
  - name: Run Copilot CLI
    env:
      COPILOT_GITHUB_TOKEN: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
    run: |
      copilot -p "YOUR PROMPT" --allow-tool='shell(git:*)' --allow-tool=write --no-ask-user
```

**Auth:** Fine-grained PAT with "Copilot Requests" permission, stored as repo secret.

**Key CI flags:** `--no-ask-user` (essential), `--allow-tool=TOOL`, `-s` (clean output).

## Autopilot Mode

Autonomous execution without waiting for input between steps.

**Activate:** `Shift+Tab` to cycle to autopilot (interactive) or `copilot --autopilot --yolo --max-autopilot-continues 10 -p "PROMPT"` (programmatic).

**Stops when:** task complete, blocking problem, `Ctrl+C`, or `--max-autopilot-continues` limit reached.

**Permissions:** On entering autopilot, prompted to choose: (1) Enable all permissions (recommended), (2) Continue with limited permissions, (3) Cancel. With limited permissions, tool requests requiring approval are auto-denied. Use `/allow-all` mid-session to upgrade (one-way — cannot toggle off).

**Premium requests:** Each autonomous continuation consumes premium requests (varies by model multiplier). CLI displays usage per step: `Continuing autonomously (3 premium requests)`.

**Best for:** well-defined tasks, multi-step sessions, batch ops. **Not for:** vague goals, nuanced judgment at each step.

**Typical workflow:** plan mode → create plan → "Accept plan and build on autopilot" → monitor.

### Comparing Flags

| Flag | Effect |
|------|--------|
| `--autopilot` | Full autonomous execution through successive steps |
| `--allow-all` / `--yolo` | Grants all permissions but stays interactive |
| `--no-ask-user` | Suppresses questions; doesn't auto-continue steps |

Combine all three for fully unattended execution.

## Task Delegation (`/delegate`)

Hands work to **Copilot coding agent on GitHub** (cloud, not local).

```
/delegate complete the API integration tests
```

What happens: commits unstaged changes → creates branch → opens draft PR → agent works in background → requests review when done.

**Use for:** handing off scoped work, tasks benefiting from CI integration, auto-tracked PRs.

| | Autopilot | Delegation |
|---|---|---|
| Runs | Locally | Remotely on GitHub |
| Output | Direct file changes | Draft PR |
| Interaction | Optional monitoring | Async review |

## Fleet (`/fleet`)

Parallel execution via subagents.

```
/fleet implement the plan
```

**Workflow:** plan mode → create plan → `/fleet implement the plan` or "Accept plan and build on autopilot + /fleet".

**Monitor:** `/tasks` — navigate with arrows, `Enter` for details, `k` to kill, `r` to remove.

**Subagent models:** default low-cost model. Override per-subtask in prompt (e.g., `Use GPT-5.3-Codex to create ...`) or via custom agent profile that specifies a model.

**Custom agents in fleet:** If custom agents are available, Copilot auto-selects based on fit. Force with `@CUSTOM-AGENT-NAME` in prompt: `Use @test-writer to create comprehensive unit tests for ...`

**Best for:** large tasks with independent steps, inherently parallelizable work. **Not for:** sequential dependencies, simple tasks.

**Cost:** each subagent uses premium requests independently — faster but potentially more expensive.

## Custom Agents

Specialized AI assistants defined by `.agent.md` files with YAML frontmatter.

### Built-in Agents

| Agent | Purpose |
|-------|---------|
| explore | Quick codebase analysis (read-only) |
| task | Command execution; brief on success, full on failure |
| general-purpose | Complex multi-step tasks in separate context |
| code-review | Reviews changes, surfaces genuine issues |
| research | Deep research across codebase, repos, and web |

### Agent File Format

```markdown
---
name: security-auditor
description: Checks code for security vulnerabilities.
tools: ["bash", "edit", "view"]
---

You are a specialized security assistant that...
```

**Fields:** `name` (required), `description` (required), `tools` (optional, defaults to all).

### Creating Agents

Use `/agent` → **Create new agent** → choose Project (`.github/agents/`) or User (`~/.copilot/agents/`). Options:
- **Copilot-assisted:** Describe expertise and Copilot generates the profile. Review, edit, continue.
- **Manual:** Guided prompts for name, description, instructions, and tool selection.

**Naming:** lowercase letters and hyphens recommended (e.g., `security-auditor`). Agent ID = filename without `.agent.md`.

### File Locations

| Scope | Location |
|-------|----------|
| User | `~/.copilot/agents/` |
| Repository | `.github/agents/` |
| Organization | `/agents/` in `.github-private` repo |

**Precedence:** system > user > repository > organization. Agent ID = filename without `.agent.md`.

### Invoking

```bash
/agent                                          # browse list
Use the security-auditor agent on /src/app      # explicit
copilot --agent security-auditor -p "Check..."  # programmatic
```

Copilot also auto-delegates based on agent description match.

## Timeout Sizing

| Complexity | Timeout |
|------------|---------|
| Simple (review, small fix) | 120–300s |
| Medium (single component) | 300–600s |
| Large (research + build) | 900–1800s |
| Very large (full redesign) | 1800s+ |

**Rule:** when in doubt, 1800s. A long wait beats a SIGTERM'd task.

## Prompt Tips for Automation

- Model attention fades on 2000+ char specs — put critical constraints at start AND end
- Use `CRITICAL:`, `REQUIREMENT:`, `MUST:` emphasis markers
- Number requirements for tracking
- For JSON output: add `Output ONLY JSON` at the end
- Add comment tag for traceability: `#my-task-name`
