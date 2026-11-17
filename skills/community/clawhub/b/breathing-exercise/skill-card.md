## Description:

Breathing Exercise helps users run guided breathing routines, including 4-7-8 breathing, box breathing, custom rhythms, relaxation guidance, and usage statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for guided breathing exercises and related ClawHub commands for relaxation, focus, sleep support, or custom breathing rhythms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact metadata requires curl, but the inspected files do not explain why that binary is needed.

Mitigation: Clarify the curl requirement with the publisher before deployment and run the skill in an environment where network access is reviewed.

Risk: The documented install command uses the latest ClawHub CLI version, which can change over time.

Mitigation: Use a pinned and trusted ClawHub CLI version for installation in controlled environments.

Risk: The skill documentation is primarily Chinese, which may reduce reviewer understanding in English-language review workflows.

Mitigation: Have a qualified reviewer confirm the translated behavior, commands, and pricing statements before approval.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
