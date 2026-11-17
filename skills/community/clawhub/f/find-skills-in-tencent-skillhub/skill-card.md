## Description:

Search, install, upgrade, and manage agent skills using skillhub CLI. Use when you need to discover new skills, install skills by slug, upgrade installed skills, list available skills, or self-upgrade the skillhub CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhonglei](https://clawhub.ai/user/wuhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to search ClawHub-backed skill listings, install skills by slug, list local skills, and preview or apply skill and Skillhub CLI upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading skills can change future agent behavior through externally retrieved content.

Mitigation: Review the Skillhub CLI source and installation instructions before installation, and use check_only before upgrades.

Risk: Forced installs can replace an existing skill directory.

Mitigation: Avoid force unless replacement is intentional and the target skill has been reviewed.

Risk: Self-upgrade and upgrade-all operations can alter the Skillhub CLI or multiple installed skills at once.

Mitigation: Treat self-upgrade and upgrade-all as trust-changing operations and review the proposed changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhonglei/skills/find-skills-in-tencent-skillhub)
- [Skillhub CLI installation guide](https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/skillhub.md)
- [Publisher profile](https://clawhub.ai/user/wuhonglei)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command output from the Skillhub CLI wrapper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include search, install, upgrade, list, and self-upgrade; some actions can modify installed agent skills or the Skillhub CLI.]

## Skill Version(s):

1.0.4 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
