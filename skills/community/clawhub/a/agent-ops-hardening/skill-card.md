## Description:

Production hardening patterns for AI agents running on OpenClaw, covering destructive command safety, session rotation, context window discipline, tool pre-flight checks, heartbeat batching with state-file gating, and memory trimming workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricksmartbrain-boop](https://clawhub.ai/user/ricksmartbrain-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to harden OpenClaw agent workspaces for production operation, audit common operational gaps, and apply routines for safer deletion, session rotation, context control, heartbeat checks, and persistent memory hygiene.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and heartbeat recommendations can shape future agent behavior.

Mitigation: Review and adapt those recommendations before adoption so they match the workspace's operating model and governance expectations.

Risk: The bundled audit script checks for expected workspace files and a rick-vault path that may not apply to every environment.

Mitigation: Run the script only in workspaces where those checks make sense and treat findings as prompts for review, not automatic changes.

## Reference(s):

- [Agent Ops Hardening on ClawHub](https://clawhub.ai/ricksmartbrain-boop/skills/agent-ops-hardening)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and a read-only shell audit script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit output is terminal text that reports workspace hardening checks and suggested fixes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
