## Description:

Meta-skill that indexes all AIOT platform skills and routes agent requests to the correct sub-skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d9m1n1c](https://clawhub.ai/user/d9m1n1c)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route AIOT platform requests to the appropriate account, identity, card, payments, crypto, or blockchain sub-skill. It also provides installation commands for the related AIOT skill set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and delegates to downstream skills that can affect identity, payment, card, crypto, wallet, and account workflows.

Mitigation: Install only after reviewing the publisher and downstream skills, and require explicit user confirmation before document uploads, payments, withdrawals, card changes, staking, or other account-impacting actions.

Risk: The security summary reports that downstream sensitive skills are requested without version or publisher safeguards.

Mitigation: Pin and verify the exact downstream skill versions and publishers before using the installer or delegating sensitive tasks.

## Reference(s):

- [AIOT Network ClawHub Skill Page](https://clawhub.ai/d9m1n1c/skills/aiotnetwork)
- [AIOT API Base URL](https://payment-api-dev.aiotnetwork.io)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIOT_API_BASE_URL for API base URL configuration; defaults to the documented AIOT development endpoint when unset.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
