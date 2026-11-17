## Description:

Integrates Didit Phone Verification standalone APIs to send and check phone OTP codes across SMS, WhatsApp, Telegram, and voice channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add Didit phone-based identity verification to applications, including sending OTPs, checking user-provided codes, and applying optional fraud policies for disposable or VoIP numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles phone numbers, OTPs, optional device telemetry, and API keys.

Mitigation: Review the skill before use with real users, provide Didit API keys only in controlled environments, avoid passing real OTPs directly on the command line, and minimize optional device or IP signals unless needed for fraud prevention.

Risk: The skill includes billing and credit top-up guidance.

Mitigation: Require explicit user confirmation before any billing or credit top-up action.

## Reference(s):

- [Didit Documentation](https://docs.didit.me)
- [Send Phone Code API](https://docs.didit.me/standalone-apis/phone-send)
- [Check Phone Code API](https://docs.didit.me/standalone-apis/phone-check)
- [Phone Verification Feature Guide](https://docs.didit.me/core-technology/phone-verification/overview)
- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/skills/didit-phone-verification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Didit API request examples and guidance that reference DIDIT_API_KEY, phone numbers, OTP codes, optional device/IP signals, and billing-related setup.]

## Skill Version(s):

1.3.0 (source: server release evidence; artifact frontmatter lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
