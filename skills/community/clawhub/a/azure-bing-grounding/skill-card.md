## Description:

Azure Bing Grounding lets agents search the web through Azure AI Foundry and the Bing Grounding Search Tool, returning synthesized answers with URL citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bowang306](https://clawhub.ai/user/bowang306)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer time-sensitive factual questions by sending configured queries to Azure AI Foundry with Bing grounding and returning cited results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Azure and Bing services as part of normal grounded-search operation.

Mitigation: Install only for workflows where Azure/Bing processing is permitted and handle query contents according to the user's data policy.

Risk: Azure credentials can be exposed if long-lived secrets are stored loosely in local environment files.

Mitigation: Prefer Azure CLI authentication, managed identity, or tightly scoped short-lived credentials; keep ~/.openclaw/.env private when it is used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bowang306/skills/azure-bing-grounding)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Raw JSON or Markdown with URL citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured Azure AI Foundry endpoint, Bing connection ID, model deployment, and Azure credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
