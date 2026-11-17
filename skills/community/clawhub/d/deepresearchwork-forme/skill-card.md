## Description:

Generates Chinese product and industry research reports by coordinating deep research, Markdown formatting, and Mermaid chart rendering into PNG assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinelp100](https://clawhub.ai/user/shinelp100)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to produce structured Chinese research reports for industry analysis, company deep dives, competitive landscape reviews, technology trend analysis, market research, and investment memos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically download and execute an unpinned npm Mermaid CLI package during chart conversion.

Mitigation: Review before installation and use a pinned, reviewed Mermaid CLI package or a sandboxed chart conversion path.

Risk: Research reports may contain inaccurate, outdated, or misleading findings if source data is weak or stale.

Mitigation: Review generated reports, verify important claims against authoritative sources, and preserve source citations and timestamps.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with generated PNG chart assets and optional shell commands for Mermaid conversion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs a topic-named research report and a mermaid_charts directory when chart conversion is used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
