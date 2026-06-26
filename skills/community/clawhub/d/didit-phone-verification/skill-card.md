## Description: <br>
Integrate Didit Phone Verification standalone API to send and check OTP codes for phone-number verification through SMS, WhatsApp, Telegram, or voice channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to add Didit phone-number verification flows, including sending OTP codes, checking user-supplied codes, and applying optional disposable or VoIP number policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Didit API key for live verification requests. <br>
Mitigation: Store DIDIT_API_KEY in a secret store or environment variable and do not commit it to source control. <br>
Risk: Phone numbers, OTP codes, IP addresses, device identifiers, and fraud-signal data may be sent to Didit. <br>
Mitigation: Send verification data only for users and numbers you are authorized to verify, and obtain appropriate user consent before using the API. <br>
Risk: Verification codes are subject to expiry, attempt limits, resend limits, and rate limits. <br>
Mitigation: Handle failed, expired, declined, undeliverable, blocked, retry, and rate-limited responses explicitly in the calling workflow. <br>


## Reference(s): <br>
- [Didit Documentation](https://docs.didit.me) <br>
- [Didit Phone Verification Overview](https://docs.didit.me/core-technology/phone-verification/overview) <br>
- [Didit Phone Send API](https://docs.didit.me/standalone-apis/phone-send) <br>
- [Didit Phone Check API](https://docs.didit.me/standalone-apis/phone-check) <br>
- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/didit-phone-verification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code examples, shell commands, and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIDIT_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
