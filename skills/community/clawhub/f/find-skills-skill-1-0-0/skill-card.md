## Description:

Search and discover OpenClaw skills from various sources. Use when: user wants to find available skills, search for specific functionality, or discover new skills to install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lq-productor](https://clawhub.ai/user/lq-productor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find OpenClaw skills by task, category, provider, or popularity before choosing whether to install or use them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote CLI execution through npx may run code that has not been reviewed for the target environment.

Mitigation: Use a pinned, reviewed clawhub version or a trusted local install, and avoid unpinned npx commands in sensitive environments.

Risk: Skill search results may point users to third-party skills with unknown quality or security posture.

Mitigation: Review each candidate skill's documentation, requirements, publisher, and scan results before installation or production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lq-productor/skills/find-skills-skill-1-0-0)
- [ClawHub](https://clawhub.com)
- [OpenClaw Directory Skills](https://www.openclawdirectory.dev/skills)
- [LobeHub Skills Marketplace](https://lobehub.com/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links to skill marketplaces, community sources, and suggested search commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
