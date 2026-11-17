## Description:

Automates DeepSeek Chat in a browser to submit a user's question and return the response extracted from the page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to ask DeepSeek Chat questions through browser automation when they want responses returned through their agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can attach to the user's browser profile and submit prompts to DeepSeek Chat.

Mitigation: Use an isolated browser profile where possible and review browser attachment permissions before execution.

Risk: Login QR screenshots and personal contact data may be sent through local messaging tools.

Mitigation: Require explicit recipient confirmation and avoid forwarding login QR codes through messaging apps unless the user has approved the channel.

Risk: Broad shell, network, and file permissions increase the impact of unintended behavior.

Mitigation: Remove unnecessary permissions before deployment and review proposed commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qidu/skills/freechat-deepseek)
- [DeepSeek Chat](https://chat.deepseek.com)
- [OpenClaw Browser Relay Chrome extension](https://chromewebstore.google.com/detail/openclaw-browser-relay/nglingapjinhecnfejdcpihlpneeadjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript and shell command examples, and extracted DeepSeek response text during use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require browser login, browser profile configuration, and user confirmation for QR-code or messaging flows.]

## Skill Version(s):

1.0.4 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
