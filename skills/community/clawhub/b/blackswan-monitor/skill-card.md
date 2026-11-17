## Description:

Generates a daily A-share black swan hedge strategy monitoring report by fetching market data, checking option implied-volatility and margin-balance signals, and sending summaries by email or Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankski818](https://clawhub.ai/user/frankski818)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-monitoring operators can use this skill to generate daily Chinese A-share hedge-monitoring reports that summarize index prices, implied volatility, margin-balance changes, strategy signals, alerts, and suggested actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and error details can be sent automatically to a hardcoded QQ mailbox.

Mitigation: Require sender and recipient addresses to be configured by the user and disable outbound email by default.

Risk: An embedded SMTP credential is present in the skill artifact.

Mitigation: Remove the credential from the release, rotate it before use, and load mail credentials only from user-managed secrets.

Risk: Error tracebacks may disclose operational details through outbound notifications.

Mitigation: Avoid sending raw tracebacks and document exactly what data is sent to email or Feishu.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain-text or Markdown-style monitoring reports with shell commands and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send reports or error details by outbound email and Feishu webhook when configured.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
