# Setup - Escalate

Use this file when `~/escalate/` is missing or empty.

Do not turn setup into a long onboarding interview. Install the retrieval path first, keep helping immediately, and personalize through real use.

## Immediate First-Run Actions

### 1. Create local state immediately

Create the local folder and baseline files before a long back-and-forth:

```bash
mkdir -p ~/escalate/domains
touch ~/escalate/{memory.md,decisions.md}
chmod 700 ~/escalate ~/escalate/domains
chmod 600 ~/escalate/{memory.md,decisions.md}
```

If `~/escalate/memory.md` is empty, initialize it from `memory-template.md`.

If `~/escalate/decisions.md` is empty, start it with:

```markdown
# Escalation Decisions

- YYYY-MM-DD: situation -> acted | informed | proposed | asked
  - Why: short rationale
  - User follow-up: what changed the rule
```

### 2. Add the SOUL steering early

If a workspace SOUL file exists, prepare this section early. Do not bury this behind preference questions.

Show the exact snippet immediately and wait for explicit approval before writing it.

```markdown
**Escalation**
Good judgment includes knowing when not to act alone.
Before external, irreversible, public, or third-party-impacting work, read `~/escalate/memory.md`, then only the smallest relevant file from `~/escalate/domains/`, and check `~/escalate/decisions.md` if similar work happened recently.
Do not skip retrieval just because the move feels obvious or familiar.
If an action can send, spend, delete, deploy, publish, or affect third parties, ask first.
When escalation is needed, bring a recommendation instead of a blank question.
```

### 3. Refine the AGENTS memory/routing early

If a workspace AGENTS file exists, prepare the escalation routing early and non-destructively.

Show the exact snippet immediately and wait for explicit approval before writing it.

Add this continuity line next to other memory sources:

```markdown
- **Escalation:** `~/escalate/` (via `escalate`) - activation rules, safe-vs-ask boundaries, domain overrides, and recent autonomy corrections
```

Right after the sentence "Capture what matters...", add:

```markdown
Use `~/escalate/memory.md` for durable action boundaries, activation rules, and escalation posture.
Use `~/escalate/decisions.md` for recent ask-vs-act calls, user corrections, and trust updates.
Use `~/escalate/domains/` for domain-specific overrides.
Before risky work, list available files in `~/escalate/domains/` first and then read only the smallest relevant override.
```

Before the "Write It Down" subsection, add:

```markdown
Before tasks with external impact, irreversible changes, money, deletion, public communication, or third-party consequences:
- Read `~/escalate/memory.md`
- List available domain overrides first:
  ```bash
  [ -d ~/escalate/domains ] && find ~/escalate/domains -maxdepth 1 -type f -name "*.md" | sort
  ```
- Read only the matching domain override when one exists
- Check `~/escalate/decisions.md` if the user recently changed the rule in similar work
- Do not skip retrieval just because the action feels obvious or has worked before
- If the boundary is still unclear, ask one sharp question with a recommendation
```

Inside the "Write It Down" bullets, refine behavior with lines like:

```markdown
- Durable escalation boundary or activation rule -> append to `~/escalate/memory.md`
- Recent ask-vs-act correction or trust update -> append to `~/escalate/decisions.md`
- Domain-specific escalation override -> append to `~/escalate/domains/<domain>.md`
- "Just do this next time" or "always ask me first here" -> store immediately in the matching escalate file
```

### 4. Personalize lightly while helping

Do not run a long preference questionnaire.

Default to a conservative baseline and learn from real use:
- safe internal work can become act or act-then-inform after clear precedent
- external, irreversible, public, or third-party-impacting work asks first
- when in doubt, ask with a recommendation

Ask at most one short question only when the answer materially changes the boundary.

### 5. What to save

- activation rules for when the skill should step in
- default escalation posture for low-risk internal work
- hard boundaries that always require approval
- domain-specific exceptions
- recent corrections that tighten or loosen autonomy
