## Description:

A Xiaohongshu note search and retrieval skill that helps agents find notes, fetch note details, and produce structured content analysis reports.

This skill is for research and development only.

## Publisher:

[champagne315](https://clawhub.ai/user/champagne315)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Xiaohongshu by keyword, retrieve note details with an authenticated web session, and summarize the collected posts into a structured analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Xiaohongshu web_session cookie and the artifact ships a populated session value.

Mitigation: Rotate or remove the shipped session value, store the cookie locally only, and avoid pasting reusable cookies into chat.

Risk: Authenticated scraping-style requests and anti-bot request behavior may violate site rules or trigger account controls.

Mitigation: Confirm authorization and applicable Xiaohongshu terms before use, limit request volume, and use only accounts approved for this activity.

Risk: Unsafe eval-based configuration parsing and unpinned dependencies increase installation and runtime risk.

Mitigation: Replace eval-based parsing with a safe parser, and pin and review dependencies before installation.

Risk: Runtime logs may expose session cookies during account or security failures.

Mitigation: Redact web_session and cookie values from logs before use.

## Reference(s):

- [Follow-XHS ClawHub release](https://clawhub.ai/champagne315/skills/follow-xhs)
- [Xiaohongshu website](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request a Xiaohongshu web_session cookie and local runtime configuration before producing search results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
