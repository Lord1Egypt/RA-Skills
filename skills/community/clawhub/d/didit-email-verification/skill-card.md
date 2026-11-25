## Description:

Provides guidance and examples for sending and checking Didit email verification codes and scoring email risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Didit's email OTP verification and email-risk checks into backend services, including handling verification outcomes and optional risk signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email addresses and any supplied IP, device, user-agent, vendor, or metadata fields are sent to Didit, where verification and risk requests create API sessions.

Mitigation: Confirm you trust Didit to receive the data and have authorization to share it; send only optional identifying signals needed for your use case.

Risk: API requests require the DIDIT_API_KEY credential.

Mitigation: Store the key in a protected environment variable and avoid exposing it in source code or logs.

## Reference(s):

- [Email Verification Overview](https://docs.didit.me/core-technology/email-verification/overview)
- [Send Email Code API](https://docs.didit.me/standalone-apis/email-send)
- [Check Email Code API](https://docs.didit.me/standalone-apis/email-check)
- [Email Risk API](https://docs.didit.me/standalone-apis/email-risk)
- [Didit Pricing](https://docs.didit.me/getting-started/pricing)

## Skill Output:

**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python and TypeScript examples, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use the DIDIT_API_KEY environment variable; API requests and responses use JSON.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
