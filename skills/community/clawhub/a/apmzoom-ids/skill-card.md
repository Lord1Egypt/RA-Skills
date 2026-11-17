## Description:

APM Authentication Center API documents 19 APM authentication endpoints for account, email, phone, administrator, supplier, user login, token refresh, verification code, captcha, and token validation flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apmzoom](https://clawhub.ai/user/apmzoom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to understand and prepare calls to APM authentication endpoints, including login, token refresh, verification-code delivery, captcha retrieval, and token validation. It is intended for authorized APM accounts and workflows that can safely handle credentials and tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers administrator, user, supplier, and seller authentication flows that can expose passwords, verification codes, access tokens, and refresh tokens.

Mitigation: Use only authorized accounts, avoid logging or persisting secrets, and keep tokens out of long-lived exported environment variables.

Risk: The documented signing pattern uses MD5 with static salts, which the security evidence identifies as weak for security-sensitive workflows.

Mitigation: Review the signing design with the APM service owner before relying on it for sensitive production automation.

Risk: Agents following the documentation may prepare calls that send verification codes or refresh reusable tokens.

Mitigation: Require explicit user approval before sending codes, refreshing tokens, or using privileged administrator credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apmzoom/skills/apmzoom-ids)
- [Publisher profile](https://clawhub.ai/user/apmzoom)
- [Homepage](https://github.com/apmzoom-ai/apm-skills)
- [APM API base URL](https://44k2t5n59e.execute-api.ap-northeast-2.amazonaws.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with request details, signing rules, headers, and example command or code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; does not execute API calls by itself.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
