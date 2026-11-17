## Description:

Secure browser automation with Chrome profile support, vault integration, approval gates, and comprehensive audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riverho](https://clawhub.ai/user/riverho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Browser Secure to automate gated or authenticated browser workflows with approval gates, Chrome profile support, vault-backed credentials, and audit trails. It is intended for tasks such as site onboarding, content capture, extraction, screenshots, and exporting structured research notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access authenticated browser sessions and password-manager material, and the security summary notes weak scoping and approval controls that need review.

Mitigation: Use a dedicated automation Chrome profile, avoid personal or regulated accounts, keep human approval enabled for sensitive sites, and avoid auto-vault or manual credential entry until origin binding, approval, and password-input issues are resolved.

Risk: Auto-approval flags can reduce human review for sensitive browsing or destructive actions.

Mitigation: Do not use --yes or --skip-approval on sensitive sites; prefer interactive approval for login, extraction, purchases, deletion, and other high-impact actions.

Risk: Audit webhooks can send audit records outside the local machine when explicitly configured.

Mitigation: Keep audit logging in file mode unless the webhook destination is fully trusted and approved for the captured data.

## Reference(s):

- [Browser Secure on ClawHub](https://clawhub.ai/riverho/skills/browser-secure)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Bitwarden](https://bitwarden.com)
- [1Password](https://1password.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, YAML configuration, screenshots, raw HTML, and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save captures, screenshots, raw HTML, site profiles, audit logs, and scrapbook exports under the user's Browser Secure workspace.]

## Skill Version(s):

2.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
