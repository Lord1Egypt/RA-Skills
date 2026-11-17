## Description:

Provides A-share stock monitoring, price alerts, technical analysis, automated reports, and risk-profile-based portfolio guidance using multiple public market data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjianghua117](https://clawhub.ai/user/chenjianghua117)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor A-share equities, generate formatted market and holdings reports, set price alerts, and receive technical and risk analysis for informational investing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data is fetched over unauthenticated HTTP and should not be treated as authoritative for trading decisions.

Mitigation: Use the skill for informational monitoring only and verify prices or signals against authoritative market data before making investment decisions.

Risk: Portfolio, holdings, alert, and cache data can be stored locally in plaintext.

Mitigation: Avoid entering sensitive portfolio details unless local plaintext storage is acceptable, and review or delete local configuration and cache files when needed.

Risk: Notification helpers can send alert or report content to external DingTalk-style endpoints.

Mitigation: Configure only trusted notification destinations and avoid sending sensitive portfolio or account details through alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjianghua117/skills/a-stock-watcher)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Plain text and Markdown-style reports, with optional JSON configuration or cache entries and chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data and analysis are informational only; outputs may include delayed quotes, holdings summaries, alerts, risk profiles, and technical indicators.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
