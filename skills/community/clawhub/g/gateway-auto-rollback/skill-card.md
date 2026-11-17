## Description:

Automatic configuration rollback mechanism for OpenClaw Gateway that backs up critical configuration files, validates JSON and gateway health, and can restore from backups after failed changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to protect OpenClaw Gateway configuration files such as openclaw.json, exec-approvals.json, and skills.json during manual, scripted, or scheduled changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence says the rollback safety claims are stronger than the implementation.

Mitigation: Review backups and test restore behavior before relying on automatic rollback for production configuration changes.

Risk: The skill touches important OpenClaw Gateway configuration, approval, and skill registry files.

Mitigation: Inspect all affected files before restoring or overwriting them, and avoid running the test script as a privileged user.

Risk: The included health check only probes the local Gateway health endpoint.

Mitigation: Use a stronger health check when adapting the skill for operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/gateway-auto-rollback)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance and scripts for OpenClaw Gateway backup, validation, rollback, watch mode, cron setup, and testing.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
