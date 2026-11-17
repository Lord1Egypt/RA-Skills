## Description:

Provides an FDE workflow assistant for customer audit, technical evaluation, and deployment planning so teams can move enterprise AI projects from discovery to business-value delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, forward deployed engineers, and AI solution teams use this skill to plan customer discovery, translate business needs into technical evaluations, design deployment paths, and generate industry-specific audit questionnaires for enterprise AI rollouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports enterprise deployment planning in regulated or customer environments, where poor authorization or data handling can create compliance and privacy risk.

Mitigation: Confirm written authorization, collect only necessary metadata, use desensitized test data, protect secrets, and require normal security, compliance, change approval, and rollback reviews before production use.

Risk: The methodology can influence production AI architecture and deployment decisions without independently validated evaluation artifacts.

Mitigation: Treat generated plans and questionnaires as review inputs, validate assumptions with stakeholders, run scoped POCs, and document acceptance criteria before deployment.

## Reference(s):

- [FDE methodology framework](references/fde-framework.md)
- [FDE technical toolkit](references/fde-toolkit.md)
- [FDE industry case library](references/fde-cases.md)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/fde)
- [Publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline commands and generated questionnaire text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate customer audit questionnaires to stdout or a user-specified Markdown file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
