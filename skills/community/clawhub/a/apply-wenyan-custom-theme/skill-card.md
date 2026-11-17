## Description:

AI-ready skill to test, register, and publish Markdown articles to WeChat Official Accounts using a local custom CSS theme via Wenyan CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caol64](https://clawhub.ai/user/caol64)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and publishing operators use this skill to preview Markdown with a local CSS theme, publish it to a WeChat Official Account draft, and optionally register the theme for reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing requires WeChat account credentials.

Mitigation: Keep WECHAT_APP_SECRET private, avoid printing environment variables, and verify credential setup outside shared logs.

Risk: The skill runs a third-party CLI to render, register, and publish content.

Mitigation: Prefer a pinned or project-local Wenyan CLI installation and confirm the exact Markdown and CSS files before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caol64/skills/apply-wenyan-custom-theme)
- [Publisher profile](https://clawhub.ai/user/caol64)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-oriented agent guidance for local files, Wenyan CLI usage, and WeChat credential setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
