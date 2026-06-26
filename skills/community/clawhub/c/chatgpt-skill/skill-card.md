## Description: <br>
Automates ChatGPT Web conversations through a local browser session with persistent login state, one-shot prompts, reusable multi-turn sessions, and conversation metadata storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PlacidusaxAlarak](https://clawhub.ai/user/PlacidusaxAlarak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to route prompts through a logged-in ChatGPT Web browser session when they need web-UI behavior such as persisted conversations, model selection, extended thinking toggles, proof screenshots, or browser troubleshooting instead of OpenAI API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in ChatGPT Web browser session and can access account-authenticated browser state. <br>
Mitigation: Install only for workflows where that access is acceptable, avoid submitting private credentials or sensitive business data in prompts, and validate authentication state before use. <br>
Risk: Runtime browser_state, temporary chatgpt-profile directories, session metadata, and screenshots may contain account-access secrets or sensitive conversation content. <br>
Mitigation: Treat these files as secrets, restrict local file access, and clean up screenshots, sessions, temporary profile copies, and other runtime artifacts after use. <br>
Risk: ChatGPT Web selectors, login challenges, CAPTCHA, 2FA, risk-review pages, and network or proxy conditions can interrupt automation. <br>
Mitigation: Use visible-browser troubleshooting, inspect JSON error payloads and screenshots, and complete login or verification flows manually when required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PlacidusaxAlarak/chatgpt-skill) <br>
- [CLI Reference](references/api_reference.md) <br>
- [Usage Patterns](references/usage_patterns.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ChatGPT Web](https://chatgpt.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands; runtime scripts return JSON payloads containing ChatGPT responses and session metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist conversation and session metadata, browser auth state, temporary runtime files, and optional proof screenshots under data/ during local execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
