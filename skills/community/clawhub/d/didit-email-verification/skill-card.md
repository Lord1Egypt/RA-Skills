## Description:

Integrate Didit Email Verification's standalone API to send and check email OTP codes, detect breached, disposable, or undeliverable emails, and support fraud-signal policy decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and product teams use this skill to add email OTP verification and optional email risk checks to identity, signup, or account-security flows through Didit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email verification sends personal data and optional fraud signals to Didit.

Mitigation: Use this skill only when Didit processing is intended, get appropriate consent, and avoid optional IP, device, and user-agent signals unless needed.

Risk: The helper script depends on a Didit API key and the external requests package.

Mitigation: Use a dedicated, least-privilege API key and install dependencies in a pinned or isolated Python environment.

## Reference(s):

- [Didit Documentation](https://docs.didit.me)
- [Didit Email Send API Reference](https://docs.didit.me/standalone-apis/email-send)
- [Didit Email Check API Reference](https://docs.didit.me/standalone-apis/email-check)
- [Didit Email Verification Feature Guide](https://docs.didit.me/core-technology/email-verification/overview)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, TypeScript, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIDIT_API_KEY and network access to Didit APIs.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
