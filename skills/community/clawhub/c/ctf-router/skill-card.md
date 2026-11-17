## Description:

Routes new CTF challenges by identifying the likely category, such as pwn, crypto, misc, web, reverse, or forensics, and directing the agent toward the appropriate solving entry point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxy050208](https://clawhub.ai/user/yxy050208)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, security learners, and CTF participants use this skill to triage challenge artifacts and choose the right solving workflow before deeper exploitation, cryptography, web, reverse engineering, or forensics work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CTF triage and tooling guidance can be misused outside authorized practice or contests.

Mitigation: Use only for legitimate CTF practice, competitions that allow AI assistance, training, or post-event review.

Risk: Environment setup guidance may lead users to run package installation or system tooling commands.

Mitigation: Review generated pip or system package commands before execution and prefer an isolated virtual environment or disposable container.

Risk: Security tools and challenge files may touch untrusted or hostile inputs.

Mitigation: Run analysis in a constrained environment and avoid elevated shells unless clearly required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yxy050208/skills/ctf-router)
- [Publisher Profile](https://clawhub.ai/user/yxy050208)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment setup checks, routing decisions, and next-step recommendations for authorized CTF practice.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
