## Description:

This skill provides AlphaClaw SkillHub CLI guidance for searching, installing, publishing, and managing Claude Code skills, including AK/SK authentication workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyunya](https://clawhub.ai/user/iyunya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to receive CLI commands and configuration guidance for discovering, installing, listing, publishing, commenting on, and favoriting SkillHub skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and trust an unpinned global npm package.

Mitigation: Review the npm package and publisher before installing, and prefer a pinned version.

Risk: The CLI handles AK/SK credentials and stores authentication material in ~/.alphaclaw/auth.json.

Mitigation: Protect ~/.alphaclaw/auth.json as a secret and avoid using the skill on shared machines.

Risk: Authenticated install and publish commands can change local skills or upload content.

Mitigation: Run authenticated install or publish commands only when you explicitly intend to change local skills or upload content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iyunya/skills/andrea-test-002)
- [AlphaClaw SkillHub website](https://skill.alphashop.cn/)
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands and setup notes for npm installation, authentication, search, install, publish, comment, and favorite workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
