## Description: <br>
Attaches the OpenClaw Browser Relay Chrome extension to a live macOS Chrome tab so browser automation can use the chrome profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[i-am-rad](https://clawhub.ai/user/i-am-rad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users working with OpenClaw browser automation use this skill to attach the Chrome extension relay on macOS before workflows that call browser(profile="chrome"). <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can abruptly close Chrome and change Chrome startup or session state. <br>
Mitigation: Save browser work before running it and use a separate Chrome profile when possible. <br>
Risk: The helper enables automation in a live Chrome session that may already be logged in. <br>
Mitigation: Use a Chrome profile with limited logins and review sensitive browser actions before allowing automation. <br>
Risk: Failure screenshots may be written to disk and could contain sensitive browser content. <br>
Mitigation: Review and delete ~/.openclaw/media/relay-attach-fail.png when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/i-am-rad/chrome-extension-relay-helper-mac) <br>
- [Publisher profile](https://clawhub.ai/user/i-am-rad) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, JSON, and Python code blocks; the attach script returns status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script reports ALREADY_ATTACHED, ATTACHED, or FAILED with a reason.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
