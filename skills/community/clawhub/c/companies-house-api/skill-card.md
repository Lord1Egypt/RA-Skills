## Description:

Search the UK Companies House register by name, then pull a company's full register entry, its officers, and its filing history as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and compliance teams use this skill to look up UK companies, retrieve official register details, review officers, and inspect filing history for KYB, due diligence, and company-monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company lookup queries and the Scavio API key are sent to a third-party API provider.

Mitigation: Confirm third-party API use is acceptable for the workflow and store SCAVIO_API_KEY only in environment variables or a secret manager.

Risk: Each endpoint call consumes paid API credits, and pagination can multiply usage.

Mitigation: Monitor credit balance, set sensible page limits, and narrow broad searches before walking many result pages.

Risk: Optional SDK installation introduces normal dependency-review considerations.

Mitigation: Install SDKs in a constrained environment and apply standard dependency review before production use.

Risk: Officer records may include public personal data such as correspondence addresses and partial dates of birth.

Mitigation: Use officer data only for the user's stated company-register task and avoid compiling unnecessary profiles of individuals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/companies-house-api)
- [Scavio Companies House documentation](https://scavio.dev/docs/companies-house-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=companies-house-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=companies-house-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API response descriptions and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured JSON responses from Scavio API endpoints; requires SCAVIO_API_KEY.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
