## Description:

Automates DeepSeek Chat in a browser by opening chat.deepseek.com, submitting user questions, and returning extracted response text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask DeepSeek Chat questions through a browser session and receive raw response text without using API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to DeepSeek through a logged-in browser session.

Mitigation: Use only with prompts approved for DeepSeek and review data-sharing expectations before installing.

Risk: Login QR-code screenshots may be forwarded through messaging channels.

Mitigation: Scan QR codes directly in the browser where possible and avoid forwarding login screenshots.

Risk: The skill requests broad command and file authority.

Mitigation: Review tool permissions before installation and narrow command, file, and outbound messaging access where supported.

Risk: Outbound messages may be sent through enabled messaging channels.

Mitigation: Require explicit destination confirmation before sending QR codes or responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qidu/skills/chat-deepseek)
- [DeepSeek Chat](https://chat.deepseek.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell and browser automation snippets; runtime responses are raw extracted text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a logged-in browser profile and sends prompts to DeepSeek Chat.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
