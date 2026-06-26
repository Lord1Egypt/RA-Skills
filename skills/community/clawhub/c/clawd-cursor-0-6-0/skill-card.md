## Description: <br>
Clawd Cursor lets an OpenClaw agent control Windows or macOS desktop apps through natural-language tasks, including opening apps, clicking, typing, navigating browsers, filling forms, and visually checking UI state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external OpenClaw users use this skill to let an agent operate desktop and browser UIs when direct APIs or CLI tools are unavailable. It is intended for user-requested, supervised desktop tasks, form interactions, cross-app workflows, and visual verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad visibility into the user's screen and control over desktop applications. <br>
Mitigation: Use it only for user-requested tasks, supervise sensitive workflows, and prefer direct APIs, file access, browser tools, or CLI commands when they can complete the task. <br>
Risk: The local controller may be started hidden and can operate apps through the local desktop session. <br>
Mitigation: Confirm how the controller starts and stops, verify it is bound to localhost, and abort or stop it when desktop automation is no longer needed. <br>
Risk: Screenshots and UI text may be sent to a configured cloud AI provider when not using a local provider. <br>
Mitigation: Prefer local Ollama mode for sensitive work and choose any cloud provider intentionally before allowing screen or app data to be processed. <br>
Risk: Sensitive or destructive actions such as sending messages, purchases, deletion, or financial workflows can affect real user accounts. <br>
Mitigation: Require explicit user confirmation for safety-gated actions and do not self-approve confirmations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sieyer/clawd-cursor-0-6-0) <br>
- [Publisher profile](https://clawhub.ai/user/Sieyer) <br>
- [Clawd Cursor homepage](https://clawdcursor.com) <br>
- [Clawd Cursor source repository](https://github.com/AmrDab/clawd-cursor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with REST API examples, shell commands, and configuration steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local REST API calls and confirmation prompts for safety-gated desktop actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version 0.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
