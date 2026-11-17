## Description:

Manage secrets and environment variables via Doppler CLI - secrets, projects, configs, environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melvynx](https://clawhub.ai/user/melvynx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get Doppler CLI guidance for managing secrets, projects, configs, environments, and activity logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to view, export, change, or delete secrets.

Mitigation: Review Doppler operations before execution, require confirmation for delete and bulk export commands, and use scoped project and config flags.

Risk: Secret values may be printed into chat, terminal output, or logs.

Mitigation: Avoid requesting or displaying plain secret values, and prefer workflows that keep secret material out of agent-visible output.

## Reference(s):

- [Doppler CLI installation documentation](https://docs.doppler.com/docs/install-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use JSON output for programmatic use where supported and avoid exposing secret values in chat or logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
