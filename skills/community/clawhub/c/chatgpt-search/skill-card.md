## Description:

Automates a browser session on ChatGPT to submit a user question and return the answer without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang040840219](https://clawhub.ai/user/yang040840219)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask ChatGPT questions through OpenClaw browser automation and receive text or JSON answers for knowledge lookup, code explanation, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save ChatGPT session screenshots locally without clear user notice or opt-out.

Mitigation: Avoid using it with secrets, personal data, proprietary code, or account-sensitive sessions unless screenshots are removed or made explicit opt-in with private storage and cleanup.

Risk: The CLI wrapper may not perform the advertised search automatically.

Mitigation: Verify behavior in a disposable browser session before relying on the result; treat generated browser steps as guidance when automation is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang040840219/skills/chatgpt-search)
- [ChatGPT](https://chatgpt.com)
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills)
- [OpenClaw browser tool documentation](https://docs.openclaw.ai/tools/browser)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON, with setup and troubleshooting guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include elapsed time, timestamp, browser-operation instructions, and local screenshot side effects.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
