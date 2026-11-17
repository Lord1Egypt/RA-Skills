## Description:

End-to-end safe coding-agent workflow using BuiltByEcho CLIs: repo-agent-brief for repo preflight, agent-runlog for command evidence, trustlog for final receipts, and add-ci dry-run for CI planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to orient within repositories, capture command evidence, produce final work receipts, and plan CI changes with a dry-run before modifying project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs third-party npm tools inside a repository.

Mitigation: Use pinned or locally locked tool versions and run commands in a least-privilege environment before trusting the resulting changes or logs.

Risk: Generated logs and receipts may contain sensitive repository details or secrets.

Mitigation: Inspect and redact generated artifacts before sharing them or uploading them outside the repository.

Risk: The Vaultline upload path can send selected work artifacts to an external service.

Mitigation: Treat uploads as explicit opt-in only after reviewing the exact artifact contents and destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/builtbyecho/skills/agent-work-receipts)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local audit artifacts such as repository briefs, run logs, trust receipts, CI dry-run plans, and optional uploaded artifact references.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
