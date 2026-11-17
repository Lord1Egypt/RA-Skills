## Description:

Creates local digital friend personas from private chat records and relationship details for companion-style simulated conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to build and test local JSON friend personas from authorized private chats or relationship notes for companion, conversation rehearsal, memory, and opinion-simulation scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted friend names can cause files to be written outside the intended friends folder.

Mitigation: Review before installing or running, and do not run the builder with untrusted names or JSON files until filename sanitization is fixed.

Risk: The skill processes private chat logs and relationship details.

Mitigation: Use only chat logs and relationship details you are authorized to process, and avoid importing group chats or third-party private conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/friend-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON persona files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include locally saved friend persona JSON derived from user-provided chat records and relationship details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
