## Description:

Generate, validate, and tighten Content Security Policy (CSP) headers for web applications by analyzing pages, discovering resource origins, building least-privilege policies, testing violations, and planning report-only to enforcement migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to generate, validate, and harden Content Security Policy headers for web applications before moving from report-only monitoring to enforcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to make web requests to user-specified sites during CSP analysis.

Mitigation: Use it only on domains you own or are authorized to test, and avoid localhost, private network addresses, admin panels, and sensitive internal services.

Risk: Generated CSP policies may miss dynamically loaded resources or allow overly broad sources if analysis inputs are incomplete.

Mitigation: Deploy report-only first, monitor CSP reports, fix observed violations, and review any unsafe-inline, unsafe-eval, wildcard, or data: allowances before enforcement.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with CSP headers, shell commands, JavaScript middleware examples, and security recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include report-only and enforcement CSP variants, migration steps, warnings, and nonce or hash implementation examples.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
