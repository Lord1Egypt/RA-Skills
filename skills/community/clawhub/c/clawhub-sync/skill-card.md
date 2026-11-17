## Description:

Synchronizes locally developed skills to ClawHub and Tencent SkillHub with .gitignore-aware filtering, allowlist controls, incremental sync, single-skill sync, and split publishing by platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to prepare, filter, publish, and track local skill releases across ClawHub and Tencent SkillHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer execution can run unverified code during setup.

Mitigation: Replace curl-to-bash setup with a versioned, verifiable installer path before installation.

Risk: Publishing preparation may disclose unintended files through staged directories or symlinks.

Mitigation: Review the staged directory recursively before publishing, reject symlinks in skills, and use a private mktemp-based staging directory.

Risk: Temporary publishing directories can retain sensitive staged files after use.

Mitigation: Manually remove staged files from /tmp after publishing or failed publishing attempts.

Risk: ClawHub and SkillHub tokens are account credentials and can expose publishing accounts if committed or copied into skill directories.

Mitigation: Keep tokens out of skill directories and configuration files, and use platform login flows or local credential storage instead.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cat-xierluo/skills/clawhub-sync)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [ClawHub CLI documentation](https://docs.openclaw.ai/clawhub/cli)
- [ClawHub Skill Format documentation](https://docs.openclaw.ai/clawhub/skill-format)
- [Tencent SkillHub publishing tutorial](https://skillhub.cn/tutorials#publish-via-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides users through publishing checks, staging, platform-specific commands, and sync-record updates.]

## Skill Version(s):

1.6.0 (source: server release evidence, frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
