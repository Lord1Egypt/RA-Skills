## Description:

Learning Loop helps an agent maintain workspace-local journals, decision logs, lessons, reviews, and memory tiers so it can learn from corrections and reflect over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawmage](https://clawhub.ai/user/clawmage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an agent a structured, transparent learning loop for journaling, decision tracking, correction review, lesson lifecycle management, and memory tiering inside a workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to persist journals, lessons, and memory in the workspace over time.

Mitigation: Periodically review brain/ and MEMORY.md, and avoid storing sensitive personal data, credentials, financial data, medical data, biometrics, or location routines.

Risk: Corrections can be promoted into longer-lived behavioral rules.

Mitigation: Use scoped confirmations such as project-only or domain-only rules when making a correction permanent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawmage/skills/clawmage-learning-loop)
- [ClawMage homepage](https://clawmage.ai)
- [ClawMage publisher profile](https://clawhub.ai/user/clawmage)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown and workspace-local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is designed to create and maintain brain/, memory/, and related workspace-local notes without external services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
