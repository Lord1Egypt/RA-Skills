## Description:

A seven-step WeChat Official Account article workflow for topic selection, research, drafting, style cleanup, image generation, HTML layout, and draft submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beneclaw](https://clawhub.ai/user/beneclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and agents use this skill to produce WeChat Official Account articles from initial topic discovery through formatted HTML and optional draft submission. It is aimed at repeatable publication workflows that require article text, supporting images, and platform-ready layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat credentials and generated draft metadata can expose account access details.

Mitigation: Configure credentials outside shared workspaces, restrict access to generated draft.json files, and delete draft.json after recording the draft ID.

Risk: Draft submission can upload local image files referenced by article HTML.

Mitigation: Run submission only on trusted HTML and keep article images confined to the intended output directory before uploading.

Risk: The skill can create drafts in a live WeChat Official Account.

Mitigation: Keep the documented user review checkpoint before running draft submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beneclaw/skills/article-factory-wechat)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)
- [HTML style guide](references/html-style-guide.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML/CSS templates, shell commands, article files, image assets, and WeChat draft metadata when submission is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented workflow writes article outputs under a dated article directory and may create draft.json after draft submission.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
