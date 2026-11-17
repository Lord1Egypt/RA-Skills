## Description:

A multi-agent research war room where personas debate in sequential turns across ideation and proposal-writing phases with persona persistence and drift detection enforced every turn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankaging](https://clawhub.ai/user/frankaging)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, research leads, and proposal-writing agents use this skill to run structured persona debates, converge on a research idea, and draft a concise proposal with logs, checkpoints, and final proposal outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional monitor launch uses unsafe shell command construction.

Mitigation: Do not let the agent auto-run the monitor command as written; run it manually with safely quoted paths in an isolated Python environment with pinned dependencies.

Risk: The workflow persistently records discussion logs and private persona memos.

Mitigation: Use the skill only where persistent logs and private memos are acceptable, and avoid placing sensitive secrets in the war-room context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankaging/skills/auto-research-proposal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, discussion logs, checkpoints, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent memory files, private persona memos, and copied results under the active project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
