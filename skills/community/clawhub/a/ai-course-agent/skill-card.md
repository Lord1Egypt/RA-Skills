## Description:

Generates Chinese-language AI education course links from natural-language grade, subject, and topic requests by charging SkillPay and calling the Edustem API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohano](https://clawhub.ai/user/ohano)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and education-app developers use this skill to convert Chinese course-generation requests into Edustem course links. It supports grade, subject, and topic extraction, then returns either a generated course link or a billing/payment response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable Edustem credentials and sends them to the configured Edustem endpoint.

Mitigation: Use only with a verified Edustem domain, provide credentials through secure environment configuration, and rotate credentials if endpoint trust changes.

Risk: The skill performs paid SkillPay billing and contains embedded SkillPay configuration tied to the publisher account.

Mitigation: Require explicit user confirmation before charges, validate configuration before billing, and rotate or remove embedded SkillPay keys before production use.

Risk: Local tests and live billing/API behavior can be confused during validation.

Mitigation: Separate mocked tests from live billing and Edustem API tests before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ohano/skills/ai-course-agent)
- [README](README.md)
- [API Requirements](API_REQUIREMENTS.md)
- [Main Session Integration Guide](src/main-session-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Chinese status text with a course URL or payment link, plus TypeScript integration examples and shell setup commands in documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May charge one SkillPay token per successful course-generation attempt and requires Edustem username/password environment variables.]

## Skill Version(s):

0.2.1 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
