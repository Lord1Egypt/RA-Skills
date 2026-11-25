## Description:

Helps developers integrate Didit's phone verification API to send and check one-time codes or assess phone-number risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to write backend integrations for Didit's standalone phone verification endpoints, including sending and checking one-time codes and assessing phone-number risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone verification can involve phone numbers and optional identifiers such as IP or device data being sent to Didit.

Mitigation: Send only the information needed for the verification flow, and account for that data in the application's privacy notices and handling practices.

Risk: Security review coverage is partial, and the evidence notes concerns about the skill's tool permission scope.

Mitigation: Review the skill's permissions and referenced material before use, and keep the DIDIT_API_KEY in a protected environment variable or secret store.

## Reference(s):

- [Didit Phone Verification overview](https://docs.didit.me/core-technology/phone-verification/overview)
- [Send phone verification code API](https://docs.didit.me/standalone-apis/phone-send)
- [Check phone verification code API](https://docs.didit.me/standalone-apis/phone-check)
- [Phone risk API](https://docs.didit.me/standalone-apis/phone-risk)
- [Didit phone verification pricing](https://docs.didit.me/getting-started/phone-verification-pricing)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Text and Markdown with Python or TypeScript examples, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.5.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
