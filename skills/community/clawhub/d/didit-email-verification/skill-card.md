## Description: <br>
Integrate Didit Email Verification standalone API to verify email addresses via OTP, including sending and checking codes, detecting risky email attributes, and configuring fraud signals and policy-based declines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add Didit email OTP verification to applications, including send/check flows, command-line testing, and policy decisions for breached, disposable, duplicated, or undeliverable emails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends email addresses and optional IP, device, or user-agent signals to Didit for verification and risk scoring. <br>
Mitigation: Use the skill only for intended Didit email verification flows, provide appropriate user notice, and send optional fraud signals only when there is a valid privacy basis. <br>
Risk: DIDIT_API_KEY is required for API access and could enable unauthorized verification requests if exposed. <br>
Mitigation: Store DIDIT_API_KEY in an environment variable or secret manager, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: Sending OTP emails can consume Didit credits or create unintended user-facing messages. <br>
Mitigation: Confirm before sending OTP emails and monitor Didit usage or credit balance. <br>


## Reference(s): <br>
- [Didit Documentation](https://docs.didit.me) <br>
- [Didit Email Send API Reference](https://docs.didit.me/standalone-apis/email-send) <br>
- [Didit Email Check API Reference](https://docs.didit.me/standalone-apis/email-check) <br>
- [Didit Email Verification Feature Guide](https://docs.didit.me/core-technology/email-verification/overview) <br>
- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/didit-email-verification) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce command-line instructions and API request examples that require DIDIT_API_KEY.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
