## Description:

A general-purpose feature development planning skill used to generate executable, verifiable, and iterative development plans before coding, and to capture lessons learned after each conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naname-zz](https://clawhub.ai/user/naname-zz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze implementation context, define scope, create verifiable feature plans, and capture reusable lessons after implementation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived lessons may be written into local skill files and affect future behavior without clear opt-in controls.

Mitigation: Review or disable the auto-iteration behavior, and inspect changes to evolution.json, custom_prompts, and SKILL.md before reusing the skill.

Risk: Plans can be misleading when they are produced before confirming the current code, data sources, and state transitions.

Mitigation: Require the context scan and verification checklist before implementation, and clearly state when a conclusion could not be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/naname-zz/skills/featureplanningautopilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown plans, checklists, risk notes, and local lesson-capture updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scoped execution plans with verification criteria and may update local evolution files when auto-iteration is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
