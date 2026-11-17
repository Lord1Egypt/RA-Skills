## Description:

Render BestYou health data as visual Dark Glass dashboards via OpenClaw canvas, including daily briefings, action plans, progress snapshots, weekly summaries, meal analysis, and workout plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kentsteffen](https://clawhub.ai/user/kentsteffen)

### License/Terms of Use:

MIT-0

## Use Case:

External BestYou users and OpenClaw agents use this skill to fetch BestYou MCP health summaries and turn them into visual coaching dashboards with short actionable text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to install mcporter globally without pinning a version.

Mitigation: Review before installing and use a pinned, verified mcporter version where possible.

Risk: A live BestYou health-data API key may be stored in plaintext configuration or exposed through chat.

Mitigation: Avoid pasting the live key into chat, store configuration with restrictive permissions, and revoke and rotate the key if it is exposed.

Risk: Rendered widgets may contact Google Fonts and the BestYou CDN.

Mitigation: Review network access expectations before deployment and account for those external asset requests.

Risk: Workout and nutrition outputs may be mistaken for professional health advice.

Mitigation: Treat coaching guidance as informational unless reviewed by an appropriate professional.

## Reference(s):

- [BestYou OpenClaw setup](https://bestyou.ai/openclaw-setup)
- [Setup reference](references/setup.md)
- [Security and privacy reference](references/security.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML canvas widgets with brief Markdown text and inline shell commands during setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses BestYou MCP API responses and local HTML/CSS templates; rendered widgets may load Google Fonts and BestYou CDN images.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
