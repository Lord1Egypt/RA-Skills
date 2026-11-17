## Description:

Use Engrm memory deliberately before coding, during coding, and when saving reusable lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dr12hes](https://clawhub.ai/user/dr12hes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to consult available Engrm memory before and during work on an existing codebase, then save only durable decisions, bugfixes, and reusable lessons after coding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project memory can retain sensitive secrets or low-value temporary details if saved indiscriminately.

Mitigation: Use Engrm only where persistent project memory is desired, and save durable decisions, bugfixes, and reusable lessons instead of secrets or temporary noise.

Risk: Agents may invent unsupported Engrm shell commands or setup steps when the integration is unavailable.

Mitigation: Confirm Engrm is connected in the current environment and avoid fabricating CLI commands or fallback setup instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dr12hes/skills/engrm-memory)
- [Publisher profile](https://clawhub.ai/user/dr12hes)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance for agent memory workflow decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No hidden code, installs, network payloads, or destructive behavior identified by security evidence.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
