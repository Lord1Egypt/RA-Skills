## Description: <br>
Automates a browser session on chat.deepseek.com to submit user questions and return DeepSeek Chat responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate DeepSeek Chat through OpenClaw browser control, including opening or reusing a chat tab, submitting prompts, and extracting responses from the page DOM. It can require manual login through the browser before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a browser session and send DeepSeek prompts to chat.deepseek.com. <br>
Mitigation: Use an isolated browser profile when possible, review prompts before submission, and avoid exposing unrelated logged-in browser state. <br>
Risk: The security evidence flags handling of login QR codes and external messaging channels as too sensitive for the skill scope. <br>
Mitigation: Complete login manually in the browser and do not send login QR codes, screenshots, cookies, tokens, or phone numbers through messaging channels. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qidu/freechat-deepseek) <br>
- [DeepSeek Chat](https://chat.deepseek.com) <br>
- [OpenClaw Browser Relay extension](https://chromewebstore.google.com/detail/openclaw-browser-relay/nglingapjinhecnfejdcpihlpneeadjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript browser automation snippets, shell commands, and extracted chat response text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses browser automation against chat.deepseek.com and may interact with a user's local browser profile or legacy relay profile.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
