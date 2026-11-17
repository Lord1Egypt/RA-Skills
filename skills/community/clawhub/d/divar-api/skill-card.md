## Description:

Helps agents search, query, and extract Divar listing data by using documented Divar API endpoints, payload wrappers, pagination, post detail, and authentication patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hadifarnoud](https://clawhub.ai/user/hadifarnoud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build or automate Divar search workflows, translate divar.ir URLs into API payloads, retrieve listing details, and understand authentication requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad unofficial scraping workflows involving session cookies, seller phone numbers, and account-related endpoints.

Mitigation: Use only for deliberate, lawful Divar search or listing work with explicit authorization and a clear data-handling plan.

Risk: Authentication guidance could encourage copying session cookies into scripts.

Mitigation: Avoid copying session cookies into scripts; use approved authentication handling and protect credentials.

Risk: Contact-info workflows can expose seller phone numbers and other sensitive listing data.

Mitigation: Do not bulk collect seller phone numbers and limit contact-info access to authorized, user-directed cases.

## Reference(s):

- [Divar API Reference](references/api-reference.md)
- [Divar API Documentation](divar-api-documentation.md)
- [Divar API Base URL](https://api.divar.ir)
- [Protocol Buffers](https://protobuf.dev/)
- [ClawHub Skill Page](https://clawhub.ai/hadifarnoud/skills/divar-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with JSON examples and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint descriptions, payload structures, authentication notes, parsing guidance, and implementation snippets.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
