## Description:

Monitor and track unauthorized content republication across the web. Generates cease-and-desist letters, manages canonical tags, and maintains attribution records. Use when the user needs content protection, copyright enforcement, or citation management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, publishers, legal teams, and marketing teams use this skill to monitor unattributed republication, draft enforcement materials, manage canonical attribution, and report on content credit activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated legal enforcement drafts may be inaccurate or inappropriate for the user's jurisdiction or authorization.

Mitigation: Keep DMCA notices, cease-and-desist letters, and related filings in draft mode until reviewed by a qualified human or legal team.

Risk: Automatic canonical tag changes can incorrectly alter attribution or SEO behavior on managed sites.

Mitigation: Disable or tightly bound automatic canonical edits, require approval before publishing changes, and verify results in the site management and search console tools.

Risk: Search, plagiarism, notification, and publishing integrations require sensitive credentials.

Mitigation: Provide least-privilege credentials through environment variables or a secrets manager and avoid placing secrets in prompts, logs, or command-line arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/attribution-content-credit-tracker)
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
- [Copyscape API](https://www.copyscape.com/api/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON, HTML, CSV, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on configured API credentials and integrations for search, plagiarism checking, notifications, canonical tag workflows, and legal template access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
