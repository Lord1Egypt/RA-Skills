## Description: <br>
Automates a browser session with DeepSeek Chat to submit user questions and return raw response text from the rendered page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask DeepSeek Chat questions through an OpenClaw browser session, reuse or open a chat tab, handle login when needed, and extract the resulting answer text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad browser and command access while automating a logged-in DeepSeek session. <br>
Mitigation: Review before installing, use a dedicated browser profile, and avoid sending secrets or sensitive personal data. <br>
Risk: The skill describes forwarding DeepSeek login QR-code screenshots through messaging channels, which can expose account-access material. <br>
Mitigation: Prefer scanning the QR code directly in the local browser and only forward QR screenshots to fully trusted destinations after understanding the account-access risk. <br>
Risk: The skill returns raw page text from DeepSeek Chat without additional validation or LLM post-processing. <br>
Mitigation: Review the returned text before acting on it, especially for security-sensitive, financial, legal, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/qidu/chat-deepseek) <br>
- [DeepSeek Chat](https://chat.deepseek.com) <br>
- [Publisher profile](https://clawhub.ai/user/qidu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with browser automation steps, shell commands, and raw response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns text extracted from the DeepSeek web page without additional LLM processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
