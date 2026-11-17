## Description:

Automates monitoring TikTok video comments for configured keywords and posting template-based replies.

This skill is for research and development only.

## Publisher:

[kamiguyi](https://clawhub.ai/user/kamiguyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use this skill to configure a Node.js workflow that searches TikTok content by keyword, reads comments, and issues low-volume template replies after credential setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok account credentials are required and may be exposed if real tokens are stored in the project directory.

Mitigation: Use a dedicated low-privilege TikTok app or test account, keep real tokens outside the project directory, and add config.json to .gitignore.

Risk: Dry-run behavior is presented as a safety control, but security evidence says it should not be relied on unless enforcement is fixed.

Mitigation: Review and fix dryRun enforcement before connecting real credentials, then validate behavior with a test account.

Risk: Watch mode can perform live social-media automation that may affect account standing.

Mitigation: Monitor account activity closely, keep reply rates low, and stop automation immediately if restrictions or abnormal behavior appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kamiguyi/skills/dagugu-tiktok-auto-reply)
- [ClawHub publisher profile](https://clawhub.ai/user/kamiguyi)
- [TikTok for Developers](https://developers.tiktok.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational guidance for running one-time checks or continuous watch mode.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
