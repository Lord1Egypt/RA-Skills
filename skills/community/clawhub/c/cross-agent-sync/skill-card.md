## Description:

Reconcile recent Claude Code and Codex sessions for one project, create a local evidence packet, and maintain a small curated progress ledger both harnesses can read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to reconcile recent Claude Code and Codex work, inspect bounded local evidence, surface conflicts, and record verified handoffs that future sessions can read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and persist sensitive agent transcript text or absolute local paths, especially when broad query search is used.

Mitigation: Use narrow project scoping, avoid broad query terms, inspect generated .agent-sync/imports files before use, and never commit raw imports.

Risk: Imported transcript excerpts may contain stale, conflicting, or unauthoritative claims from earlier sessions.

Mitigation: Treat imports as evidence only, inspect cited artifacts, surface conflicts, and record only verified decisions or next actions in the curated ledger.

Risk: Installing an unreviewed release may expose private local history to a parser or workflow the operator has not audited.

Mitigation: Install from a pinned reviewed commit or release where possible and review the skill before running it against private Claude or Codex history.

## Reference(s):

- [Session formats reference](references/session-formats.md)
- [Cross-Agent Sync on ClawHub](https://clawhub.ai/antreasantoniou/skills/cross-agent-sync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and project-local JSONL and Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates bounded local import packets and a curated progress ledger under .agent-sync; raw imports are local-only and should not be committed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
