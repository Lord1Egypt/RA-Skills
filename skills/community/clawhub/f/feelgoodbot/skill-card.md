## Description: <br>
Set up feelgoodbot file integrity monitoring and TOTP step-up authentication for macOS agents that need tamper detection, security alerts, or OTP checks before sensitive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kris-hansen](https://clawhub.ai/user/kris-hansen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up macOS file integrity monitoring, Clawdbot alerting, and TOTP checks for sensitive agent actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup installs an unpinned Go binary, creates a baseline, enables webhooks, stores a local webhook secret, restarts the gateway, and starts a persistent daemon. <br>
Mitigation: Install only after reviewing the setup behavior and trusting the upstream feelgoodbot project; run it on the intended macOS host with appropriate local privileges. <br>
Risk: TOTP step-up protection is documented but may not be active until initialization and protected-action configuration are completed. <br>
Mitigation: Run the documented TOTP initialization and configure protected actions separately before relying on OTP checks for sensitive agent actions. <br>
Risk: Webhook alerting depends on a locally stored secret and Clawdbot gateway configuration. <br>
Mitigation: Review the generated configuration, protect the local secret, and rotate the webhook token if setup output or local files are exposed. <br>


## Reference(s): <br>
- [Feelgoodbot ClawHub page](https://clawhub.ai/kris-hansen/feelgoodbot) <br>
- [feelgoodbot GitHub repository](https://github.com/kris-hansen/feelgoodbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
