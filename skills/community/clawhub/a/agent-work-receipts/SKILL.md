---
name: agent-work-receipts
description: End-to-end safe coding-agent workflow using BuiltByEcho CLIs: repo-agent-brief for repo preflight, agent-runlog for command evidence, trustlog for final receipts, and add-ci dry-run for CI planning. Use for agent handoffs, auditable repo changes, safer PR work, test/build proof, or making AI coding work inspectable.
---

# Agent Work Receipts Skill

Use this meta-workflow when a coding task needs reliable orientation, command evidence, and human-readable proof.

## Recommended flow

### 1. Preflight the repo

```bash
npx repo-agent-brief . > AGENT_BRIEF.md
sed -n '1,220p' AGENT_BRIEF.md
```

For branch handoffs:

```bash
npx repo-agent-brief . --diff origin/main > AGENT_HANDOFF.md
```

### 2. Run important commands with logs

```bash
npx agent-runlog -- npm test
npx agent-runlog -- npm run lint
npx agent-runlog -- npm run build
```

Use runlogs for noisy debugging and CI reproduction.

### 3. Produce final receipts

```bash
npx @builtbyecho/trustlog run -- npm test
npx @builtbyecho/trustlog verify .trustlog/latest.json
```

Use Trust Log as concise final evidence for the user, PR, issue, or next agent.

### 4. If CI is missing, preview before modifying

```bash
npx @builtbyecho/add-ci . --tier 2 --dry-run
```

Only rerun without `--dry-run` after the user/project owner agrees with the plan.

## Decision guide

- Need orientation? `repo-agent-brief`.
- Need full command logs? `agent-runlog`.
- Need final proof/receipt? `trustlog`.
- Need CI scaffold planning? `add-ci --dry-run`.

## Safety rules

- Check git identity before commits/pushes.
- Do not run destructive commands without explicit approval.
- Keep `.agent-runs/`, `.trustlog/`, `AGENT_BRIEF.md`, and `AGENT_HANDOFF.md` local unless the user wants them committed or shared.
- Inspect generated artifacts before public posting; redaction helps but is not a guarantee.

## Vaultline integration

When this workflow produces artifacts needed across sessions, upload key outputs to Vaultline at the end:

- `AGENT_BRIEF.md` or `AGENT_HANDOFF.md`
- `.agent-runs/.../report.md`
- `.trustlog/latest.md`

Example upload:

```bash
node -e '
const fs = require("node:fs");
const { Vaultline } = require("@builtbyecho/vaultline-sdk");
const filePath = ".trustlog/latest.md";
const content = fs.readFileSync(filePath, "utf8");
const vault = new Vaultline({ apiKey: process.env.VAULTLINE_API_KEY });
vault.files.upload({
  path: `agent-work-receipts/${Date.now()}-latest.md`,
  content,
  contentType: "text/markdown"
}).then(r => console.log("Vaultline fileId:", r.fileId));
'
```

This gives one durable artifact reference for PRs, tickets, and handoffs.
