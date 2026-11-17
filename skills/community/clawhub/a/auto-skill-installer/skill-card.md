## Description:

Auto Skill Installer helps an agent understand a capability need, discover a suitable skill, install the best candidate, and verify the installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent find, evaluate, install, and verify reusable skills when a requested task needs a missing capability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add other skills to the agent environment from mutable external sources.

Mitigation: Prefer recommendation mode or require confirmation before installation; install only pinned or verified skills from trusted sources.

Risk: Global or shared installs can change the skill set visible to multiple agent sessions.

Mitigation: Avoid global installs unless explicitly intended, and verify the destination skill directory before relying on the installed skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/auto-skill-installer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend or run installation commands and report verification results.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
