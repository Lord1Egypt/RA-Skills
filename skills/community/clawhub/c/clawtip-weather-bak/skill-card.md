## Description: <br>
Clawtip Weather.Bak provides Chinese-language daily weather reports for a user-specified location after a Clawtip payment verification flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liulian822](https://clawhub.ai/user/liulian822) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request paid weather reports for a specific location. The agent creates an order, coordinates Clawtip payment verification, and returns the weather report after payment succeeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke a payment flow before delivering the weather report. <br>
Mitigation: Review the payment amount and recipient before proceeding, and install only when a paid weather service is expected. <br>
Risk: Payment tokens, orders, and payment credential files may be stored locally, including plaintext token storage in the bundled payment helper. <br>
Mitigation: Avoid shared machines, restrict local file permissions, and remove local order or token files when they are no longer needed. <br>
Risk: The security review marked the release suspicious because it bundles a high-impact payment/wallet helper with background polling and broad local file access. <br>
Mitigation: Review the skill before deployment and prefer a version that pins and verifies the payment dependency, validates local file paths, and uses protected secret storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liulian822/clawtip-weather-bak) <br>
- [Clawtip wallet](https://clawtip.jd.com/qrcode?bizUrl=https://jpay.jd.com/ecnya2a/claw/index) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and key-value payment/status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user location and a verified order number/payment credential before report generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
