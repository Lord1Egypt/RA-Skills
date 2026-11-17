## Description:

Guides an agent through preparing WeChat Official Account articles and image-text drafts from Markdown, HTML, plain text, and image inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonight-su](https://clawhub.ai/user/tonight-su)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content publishers use this skill to have an agent prepare WeChat Official Account publishing workflows, setup preferences, article metadata, themes, image handling, and command suggestions. Users should verify the installed artifact before relying on publishing behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use WeChat publishing credentials or an existing logged-in Chrome profile to create drafts.

Mitigation: Use a dedicated WeChat account or browser profile, limit credential scope where possible, and review generated drafts before publication.

Risk: Credential material may be placed in configuration files such as EXTEND.md or environment files.

Mitigation: Keep AppSecrets out of EXTEND.md and store secrets in a protected secret manager or a tightly permissioned environment file.

Risk: The documented runtime fallback can execute Bun through npx.

Mitigation: Prefer a preinstalled trusted Bun runtime and avoid npx -y bun unless the package source and execution context are acceptable.

Risk: Server evidence says this release removed the internal scripts while the documentation still describes script-backed publishing features.

Mitigation: Verify the installed artifact contains the expected scripts before attempting a publishing workflow.

## Reference(s):

- [Article Posting](artifact/references/article-posting.md)
- [First-Time Setup](artifact/references/config/first-time-setup.md)
- [Image-Text Posting](artifact/references/image-text-posting.md)
- [ClawHub Skill Page](https://clawhub.ai/tonight-su/skills/baoyu-post-to-wechat-3)
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown drafts or preference files when used by an agent with file-writing access.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter version is 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
