## Description:

Extracts coworkers' AI tool usage from WeChat chat text or screenshots and organizes relevant messages into structured records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmf515](https://clawhub.ai/user/gmf515)

### License/Terms of Use:

MIT-0

## Use Case:

Team AI adoption leads, HR or administrative staff, and product managers use this skill to summarize WeChat reports of AI tool usage into spreadsheet-ready records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat messages may include coworker names or unrelated sensitive chat content.

Mitigation: Process only authorized messages, minimize unrelated content, and anonymize names when possible.

Risk: The generated CSV may be shared beyond the intended audience.

Mitigation: Restrict distribution of the CSV to people authorized to view the underlying coworker AI-usage data.

Risk: Spreadsheet software may interpret cells beginning with =, +, -, or @ as formulas.

Mitigation: Review and neutralize formula-like cells before opening or sharing the CSV in spreadsheet tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmf515/skills/ai-usage-collector)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain-text CSV rows with a brief Markdown note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV rows omit a header and use empty fields when source data is missing.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
