## Description:

Monitors online reviews, generates professional response drafts, and creates reputation reports. Covers review aggregation, sentiment analysis, and strategic response planning across major platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

External reputation managers, agencies, and business operators use this skill to audit public review platforms, draft platform-specific review responses, and assemble reputation reports with sentiment, topic, trend, and action-plan sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external npm CLI.

Mitigation: Pin and independently review the cashclaw npm package before installation, and run it with minimal filesystem and credential access.

Risk: Ongoing review monitoring may collect public review text and personal data without explicit handling limits.

Mitigation: Confirm review-platform terms and privacy obligations before use, and set retention, deletion, and access rules for collected review data.

Risk: Generated response drafts or reports could misstate review facts or expose private customer details.

Mitigation: Human-review all drafts against source reviews before posting, avoid private customer details in public replies, and make report branding opt-in.

## Reference(s):

- [Cashclaw Reputation Manager on ClawHub](https://clawhub.ai/andreataide86/skills/cashclaw-reputation-manager)
- [Publisher profile: andreataide86](https://clawhub.ai/user/andreataide86)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and response drafts with JSON/YAML-style data examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reputation reports, review response drafts, brief summaries, monitoring setup guidance, and prioritized action plans.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
