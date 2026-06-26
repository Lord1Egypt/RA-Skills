## Description: <br>
Uses browser automation to ask questions on ChatGPT and retrieve AI answers, with basic use available without logging in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang040840219](https://clawhub.ai/user/yang040840219) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to ask ChatGPT questions from an agent session or Node script and receive answers for knowledge lookup, code explanation, concept learning, troubleshooting, and current-information queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to ChatGPT through browser automation and may disclose sensitive, private, customer, or proprietary information. <br>
Mitigation: Do not submit secrets, credentials, private customer data, or proprietary material; use a separate browser profile when evaluating or deploying the skill. <br>
Risk: The handler saves screenshots of ChatGPT sessions to local disk by default. <br>
Mitigation: Regularly delete /tmp/chatgpt-screenshots, change the screenshot directory to an approved location, or modify the skill so screenshots are opt-in. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang040840219/chatgpt-search) <br>
- [ChatGPT](https://chatgpt.com) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/skills) <br>
- [OpenClaw Skill creation guide](https://docs.openclaw.ai/skills/creating) <br>
- [OpenClaw browser tools documentation](https://docs.openclaw.ai/tools/browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON, with usage examples and browser-action guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and a Chromium browser with remote debugging on port 18800; the handler saves screenshots under /tmp/chatgpt-screenshots by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
