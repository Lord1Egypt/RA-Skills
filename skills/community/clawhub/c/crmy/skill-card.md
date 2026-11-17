## Description:

CRMy agent manages contacts, accounts, deals, and pipeline using the CRMy CRM, with guidance to search before creating, log meaningful interactions, and suggest next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codycharris](https://clawhub.ai/user/codycharris)

### License/Terms of Use:

Apache-2.0

## Use Case:

Sales and relationship teams use CRMy to search CRM records, create and update contacts, accounts, and opportunities, log meaningful interactions, summarize pipeline status, and identify next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform sensitive CRM write actions such as creating records, advancing opportunities, and logging activities.

Mitigation: Review agent-requested CRM writes before approval, especially bulk changes or updates to revenue-related records.

Risk: CRMy API keys and CRM data may be exposed if a non-local server URL uses insecure transport or an overly broad key.

Mitigation: Prefer HTTPS server URLs except for local development and configure a least-privilege CRMy API key.

Risk: Untrusted record IDs passed into update tools can target unintended CRM records until the plugin validates UUIDs.

Mitigation: Use search results to confirm record identity and avoid passing untrusted record IDs into update operations.

## Reference(s):

- [CRMy ClawHub skill page](https://clawhub.ai/codycharris/skills/crmy)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Concise natural-language responses, with tables or bullets for CRM summaries and tool-backed CRM updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured CRMy server URL and API key to read and write CRM records.]

## Skill Version(s):

0.5.11 (source: evidence release version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
