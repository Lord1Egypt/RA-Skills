## Description: <br>
Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuangyinbot-boop](https://clawhub.ai/user/chuangyinbot-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw node-to-gateway connection routes, QR or setup-code pairing failures, and companion app authorization issues across local Wi-Fi, Tailscale, public URL, and remote gateway setups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup codes, bootstrap tokens, and similar pairing output may expose sensitive access details if shared publicly. <br>
Mitigation: Do not publish full setup-code or token-like output; redact sensitive values before sharing diagnostic logs. <br>
Risk: Approving an unexpected pending device could grant access to the wrong device. <br>
Mitigation: Run device approval only after confirming the pending device belongs to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chuangyinbot-boop/cool-node-connect) <br>
- [Publisher profile](https://clawhub.ai/user/chuangyinbot-boop) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Troubleshooting responses should identify one route and one concrete diagnosis when evidence is sufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
