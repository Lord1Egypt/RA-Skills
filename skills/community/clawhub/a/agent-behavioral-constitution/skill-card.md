## Description:

Provides behavioral guidelines for AI agents covering safety, privacy, honesty, traceability, risk-aware operations, proactive status reporting, and decision logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaobu2020](https://clawhub.ai/user/xiaobu2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a behavioral constitution that guides an agent's safety, privacy, factuality, traceability, and proactive task-management habits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly governs agent behavior and may cause an agent to create persistent memory or status files without clear user control.

Mitigation: Install only when memory writes are restricted to explicit user-approved entries and status-file locations are defined.

Risk: The skill encourages proactive actions that may conflict with higher-priority instructions or current user intent.

Mitigation: Keep the skill subordinate to system, developer, and current user instructions, and require confirmation for file-changing or critical operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown behavioral rules and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applies as agent behavior guidance; no standalone runtime output.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
