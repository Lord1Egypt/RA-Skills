## Description: <br>
Account, access, and operations infrastructure for AI agents - phone verification, email inboxes, CAPTCHA solving, credential vault, and identity management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiyanhui](https://clawhub.ai/user/shiyanhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use Clawise to give agents account and access infrastructure, including email inboxes, phone verification, CAPTCHA solving, credential storage, and identity management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may use sensitive account infrastructure such as CAPTCHA solving, phone verification, inboxes, and credential vault access without clear safety limits. <br>
Mitigation: Use a dedicated, least-privileged API key and require human approval for CAPTCHA solving, phone verification, account creation, and credential access. <br>
Risk: Provider-side audit, revocation, retention, and lawful-use controls are not confirmed by the evidence. <br>
Mitigation: Confirm audit logs, key revocation, retention controls, and clear lawful-use boundaries before deployment. <br>


## Reference(s): <br>
- [Clawise homepage](https://clawise.dev) <br>
- [Clawise documentation](https://docs.clawise.dev) <br>
- [ClawHub release page](https://clawhub.ai/shiyanhui/clawise) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown guidance with environment variable setup details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWISE_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
