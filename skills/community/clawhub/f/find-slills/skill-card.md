## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rumengkai](https://clawhub.ai/user/rumengkai)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to discover relevant installable skills, run Skills CLI searches, and present install options when a request may map to an existing skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends broad-triggered, unpinned remote installs of other skills, including global no-confirm installs.

Mitigation: Review installs manually, prefer pinned CLI versions and exact skill revisions, use local or scoped installs when possible, and avoid no-confirm global installs for untrusted skills.

Risk: Search results and install candidates can come from third-party publishers.

Mitigation: Confirm the source and publisher before installation and prefer visible confirmation steps that identify the package being installed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rumengkai/skills/find-slills)
- [Skills directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline bash commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill names, install commands, and links to skill pages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
