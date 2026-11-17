## Description:

Use the locally installed source version of Agent Orchestrator (AO) through a stable OpenClaw wrapper for health checks, service management, session control, review feedback, and source updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate a local Agent Orchestrator checkout from OpenClaw without repeatedly typing long source-entrypoint commands. It is intended for AO status, health, service, session, messaging, review-check, and update workflows on the configured local machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper executes code from a local Agent Orchestrator checkout and its dependencies, including update and build commands.

Mitigation: Install and use the skill only when you control and trust the referenced checkout; review the Git remote and pending changes before updates or dependency installation.

Risk: The configured paths are hardcoded to one user's local machine layout.

Mitigation: Confirm the local AO path before use and avoid installing the skill unchanged on unrelated machines.

## Reference(s):

- [AO command cookbook](references/commands.md)
- [ClawHub skill page](https://clawhub.ai/chaoyang78/skills/ao-op)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides command execution against a hardcoded local AO source checkout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
