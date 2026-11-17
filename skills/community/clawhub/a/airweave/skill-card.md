## Description:

Airweave lets agents search and retrieve context from Airweave collections that index user applications such as Slack, GitHub, Notion, Jira, Confluence, Google Drive, Salesforce, Linear, SharePoint, and Stripe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lennertjansen](https://clawhub.ai/user/lennertjansen)

### License/Terms of Use:


## Use Case:

Employees, external users, developers, and agents use this skill to answer questions and complete tasks with context retrieved from connected workplace applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the Airweave API key may be sent to a custom endpoint if AIRWEAVE_BASE_URL is set.

Mitigation: Keep AIRWEAVE_BASE_URL unset or set it only to a trusted HTTPS Airweave endpoint before use.

Risk: Broad searches can expose sensitive company data from connected applications.

Mitigation: Use a least-privilege read-only key where possible and limit searches to the user's explicit scope.

## Reference(s):

- [Airweave Search Parameters](artifact/references/PARAMETERS.md)
- [Airweave Search Examples](artifact/references/EXAMPLES.md)
- [Airweave API endpoint](https://api.airweave.ai)
- [ClawHub Airweave skill page](https://clawhub.ai/lennertjansen/skills/airweave)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional source listings and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, AIRWEAVE_API_KEY, and AIRWEAVE_COLLECTION_ID; AIRWEAVE_BASE_URL optionally changes the API endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
