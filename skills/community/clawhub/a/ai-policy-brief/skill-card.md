## Description:

Aggregates recent China AI policy updates from national agencies, Guangdong and Guangzhou sources, selected media, and a policy aggregator, then produces a concise structured brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitetin](https://clawhub.ai/user/whitetin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and policy teams use this skill to collect recent Chinese AI policy items and receive a categorized Markdown brief with source links, dates, key points, and trend analysis. The skill is useful for tracking national, Guangdong, Guangzhou, and broader regional policy activity without manually checking each source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler depends on live third-party websites, so availability, HTML changes, or crawler blocking can lead to missing or incomplete policy results.

Mitigation: Treat generated briefs as monitoring aids, rerun when sources fail, and confirm important items against the original official HTTPS pages.

Risk: Brief summaries may omit context or reflect stale or incomplete crawler data.

Mitigation: Use the included source links and publication dates to verify claims before relying on the brief for decisions.

Risk: Installing Python dependencies in a shared environment can create dependency or supply-chain exposure.

Mitigation: Install dependencies in a dedicated virtual environment and review dependency sources before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whitetin/skills/ai-policy-brief)
- [AI policy source list](references/policy_sources.md)
- [Publisher profile](https://clawhub.ai/user/whitetin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown brief with source links and JSON-backed collection results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated summaries, categorized policy tables, publication dates, original URLs, and trend analysis.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
