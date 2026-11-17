## Description:

Provides China Postal Savings Bank enterprise banking direct-connection API guidance for balance inquiries, transaction history queries, and payment approval operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypersonal](https://clawhub.ai/user/hypersonal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and banking-integration teams use this skill to prepare PSBC enterprise-bank direct connection parameters for account balance checks, historical transaction queries, and payment approval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes enterprise banking balance access and payment approval without clear authorization or confirmation safeguards.

Mitigation: Use only in a controlled PSBC enterprise banking workflow, require explicit user confirmation before payment operations, and verify the bank-side authorization and approval flow before deployment.

Risk: Placeholder gateway and credential configuration is incomplete for a live banking integration.

Mitigation: Have the responsible banking-integration owner review the configuration, keep credentials least-privileged, and restrict account access before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hypersonal/skills/cpef-psbc)
- [ClawHub publisher profile](https://clawhub.ai/user/hypersonal)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code]

**Output Format:** [Markdown with parameter descriptions and JavaScript configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operation names, account and currency parameters, date ranges, amount fields, and placeholder PSBC gateway credentials.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
