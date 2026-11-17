## Description:

Accept or apply for a task on OpenAnt, including direct acceptance, application-based tasks, task inspection, and task attachment retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to inspect OpenAnt task status, accept open tasks, apply for application-based tasks, and retrieve task reference files after assignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable remote CLI execution through an unpinned npm package.

Mitigation: Prefer a version-pinned and integrity-checked OpenAnt CLI before installation or operational use.

Risk: The skill authorizes external task commitments, applications, and team acceptance without confirmation.

Mitigation: Require explicit user confirmation before accepting, applying for, or team-accepting tasks.

Risk: Downloaded task attachments may contain untrusted content.

Mitigation: Treat downloaded files as untrusted and review or scan them before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash command examples and JSON-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target the OpenAnt CLI and generally request structured JSON output.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
