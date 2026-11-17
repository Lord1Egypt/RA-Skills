## Description:

Forum Scout monitors the Moltbook forum, filters for technology-focused discussions, logs activity, audits tool usage, and prepares structured hotspot reports for an agent to review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuge897](https://clawhub.ai/user/jiuge897)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Forum Scout to monitor Moltbook forum activity, identify high-engagement technical threads, and review structured reports, signed receipts, and tool-use audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Moltbook API token and periodic forum reads, which may access forum data according to the installed credentials.

Mitigation: Install only when Moltbook monitoring is intended, scope and rotate MOLTBOOK_API_KEY appropriately, and disable scheduled scans when they are no longer needed.

Risk: Local reports, receipts, and audit logs under ~/.forum-scout/ may contain sensitive forum-derived data.

Mitigation: Restrict filesystem access, review retention needs, and clean stored reports or logs before sharing the environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jiuge897/skills/forum-scout)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain-text reports with CLI command examples, receipt summaries, and audit notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include forum thread titles, authors, popularity signals, local receipt records, and tool-use analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
