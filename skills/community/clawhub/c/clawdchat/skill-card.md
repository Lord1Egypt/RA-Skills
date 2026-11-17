## Description:

ClawdChat browses and analyzes public Moltbook posts and comments to identify core AI-agent community questions, extracted solutions, trends, and a Markdown daily report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasyao1985](https://clawhub.ai/user/lucasyao1985)

### License/Terms of Use:

MIT

## Use Case:

Developers and community analysts use this skill in Claude Code to review public Moltbook discussions, filter low-value posts, extract recurring problems and solutions, and save a daily Markdown analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill browses public Moltbook pages and saves local reports, with optional raw data retention.

Mitigation: Review or change the destination path before use and disable or remove raw data retention when local copies are not desired.

Risk: Generated reports may summarize public discussion inaccurately or include unverified community claims.

Mitigation: Review the Markdown report and verify important claims or links before using the analysis for decisions or sharing it outside the intended audience.

Risk: Moltbook page structure may change and cause selectors or extraction logic to miss content.

Mitigation: Use browser snapshots to confirm current page structure and update references/selectors.md when extraction fails.

## Reference(s):

- [Moltbook](https://moltbook.com)
- [Moltbook selector reference](references/selectors.md)
- [Moltbook spam filtering rules](references/spam-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown daily report with concise chat status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves reports under ~/myassistant/chat/moltbook-daily/ and may optionally retain raw JSON data.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
