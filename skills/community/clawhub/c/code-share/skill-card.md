## Description:

Share code via GitHub Gist instead of inline chat blocks. Use when code output exceeds 10 lines, when the user asks for copy-friendly code sharing in Discord/chat, or when preserving formatting is important.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeromestein](https://clawhub.ai/user/jeromestein)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to share longer code outputs through GitHub Gist when chat blocks would be hard to copy, preserve, or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files are uploaded to GitHub Gist, which can expose proprietary code, credentials, personal data, or other sensitive content if shared without review.

Mitigation: Review files before sharing, keep the default secret Gist setting unless public posting is intentional, and replace secrets or sensitive values with local placeholders.

## Reference(s):

- [Code Share on ClawHub](https://clawhub.ai/jeromestein/skills/code-share)
- [Publisher profile](https://clawhub.ai/user/jeromestein)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks and Gist URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers secret Gists by default and returns a concise three-line sharing response.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
