## Description:

Audit and slim down always-loaded context files (AGENTS.md, TOOLS.md, USER.md, MEMORY.md, HEARTBEAT.md, SOUL.md, IDENTITY.md).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sundevilatb](https://clawhub.ai/user/sundevilatb)

### License/Terms of Use:


## Use Case:

Developers and agent maintainers use this skill to audit always-loaded workspace context files, estimate token cost, and produce recommendations to move, remove, or compress context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may affect sensitive always-loaded agent instruction or memory files.

Mitigation: Review proposed edits to AGENTS.md, MEMORY.md, USER.md, SOUL.md, HEARTBEAT.md, TOOLS.md, and IDENTITY.md before applying them.

Risk: Token counts are approximate because the bundled measurement script estimates tokens from byte counts.

Mitigation: Use the report for triage and validate final token budgets with the tokenizer or runtime that will consume the files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sundevilatb/skills/context-slimmer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with inline shell commands and tabular measurement output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current size, projected size, savings by file, and recommendations grouped by move, remove, or compress.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
