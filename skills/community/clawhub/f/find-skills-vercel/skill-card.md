## Description:

Helps users discover and install agent skills for specialized tasks by searching, evaluating, and presenting relevant options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachary2024](https://clawhub.ai/user/zachary2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to identify suitable installable skills, assess basic quality signals, and provide install or follow-up guidance when a user's request may match an existing skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package-manager commands may fetch unexpected versions or behavior.

Mitigation: Prefer locally installed or version-pinned Skills CLI commands and inspect the selected skill before installation.

Risk: Global installs with skipped confirmation can modify user-wide agent behavior without another prompt.

Mitigation: Avoid `-g -y` unless the user explicitly approves a global, non-interactive install.

Risk: Updating all installed skills can introduce unreviewed changes.

Mitigation: Review what will change before allowing the agent to update installed skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zachary2024/skills/find-skills-vercel)
- [Skills Directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill names, quality signals, install commands, and links for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
