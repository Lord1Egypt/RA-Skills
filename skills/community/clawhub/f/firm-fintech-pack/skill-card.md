## Description:

Curated skill bundle for fintech startups, neobanks, payment processors, and wealth-management platforms that activates Finance, Legal, Engineering, and Compliance agents for AML/KYC, financial modelling, regulatory reporting, and payment infrastructure workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and fintech teams use this skill to configure a multi-department agent firm for financial services workflows, including AML/KYC review, pricing analysis, regulatory reporting, payment infrastructure, audit, and incident-response planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad multi-session authority in a sensitive financial context.

Mitigation: Only grant session history, session sending, and session spawning with explicit approval, tenant isolation, redaction of customer and financial data, and audit logging.

Risk: The companion install commands use mutable latest-version package resolution.

Mitigation: Use pinned, reviewed versions or an internal approved registry before production deployment.

Risk: Financial and regulatory review workflows may expose tier-1 sensitive data.

Mitigation: Run regulatory reviews in read-only mode with production security controls, immutable audit trails, and sandboxed non-main sessions.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands, JSON configuration, and workflow prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes department activation guidance, companion skill install commands, configuration overlay examples, and structured workflow prompts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
