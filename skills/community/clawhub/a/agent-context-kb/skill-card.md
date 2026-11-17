## Description:

Manage and explain a repository-local `.agent-kb/` knowledge base for coding agents, including setup, validation, note capture, compilation, trimming, and stats reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lesliebiubiubiu](https://clawhub.ai/user/lesliebiubiubiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent operators use this skill to set up and maintain a repository-local project knowledge base that agents read before work and update after durable project knowledge changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify repository instruction files and create persistent `.agent-kb/` state.

Mitigation: Review generated `AGENTS.md`, `CLAUDE.md`, and `.agent-kb/` changes before committing or sharing them.

Risk: The stats workflow can read local Claude/Codex transcript histories and keep derived activity records locally.

Mitigation: Skip transcript backfill when transcript-free statistics are desired, and periodically delete `.agent-kb/.log/` when local activity metadata should not persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lesliebiubiubiu/skills/agent-context-kb)
- [Server-resolved GitHub provenance](https://github.com/lesliebiubiubiu/agent-context-kb-skill/tree/main/skills/agent-context-kb)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated repository files/configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update `.agent-kb/`, `AGENTS.md`, and `CLAUDE.md`; stats can report transcript-derived ASCII charts.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
