## Description:

Single source of truth for all paths, naming conventions, and data formats across the OpenClaw Greek Accounting system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

Developers and operators of the OpenClaw Greek Accounting system use this skill as a reference map for canonical data directories, file naming, data formats, validation rules, audit logging, encryption expectations, and skill responsibility boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The data map standardizes long-term memory and audit logging that may contain sensitive accounting activity.

Mitigation: Require encryption for /data/memory and /data/system/logs/audit before production use.

Risk: Memory, audit, and chat/session records may retain sensitive values longer than users expect.

Mitigation: Define retention and deletion controls, redact sensitive values from memory and audit records, and disclose chat/session retention to users.

Risk: The documented GitHub proposal workflow could introduce incorrect or misleading skill changes if automated output is accepted without review.

Mitigation: Keep proposal creation human-approved and rate-limited, and require review before any generated change is merged.

## Reference(s):

- [Canonical Data Map on ClawHub](https://clawhub.ai/satoshistackalotto/skills/canonical-data-map)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown reference documentation with inline shell commands and structured path examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the OPENCLAW_DATA_DIR environment variable for the documented data-root convention.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
