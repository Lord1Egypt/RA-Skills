## Description:

Search your Senso.ai knowledge base hands-free through Edith smart glasses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samdickson22](https://clawhub.ai/user/samdickson22)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Edith smart glasses use this skill to search their own Senso.ai knowledge base for documents, policies, or stored information and receive short spoken summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys and user questions in ways that could expose sensitive data.

Mitigation: Store Senso.ai API keys in a proper secret store, avoid pasting secrets into chat, and use the skill only when the user is comfortable sending questions and relevant document passages to Senso.ai.

Risk: The curl examples could allow unsafe shell execution if user questions are interpolated directly into shell commands.

Mitigation: Build requests with safely serialized JSON and avoid placing untrusted user text directly into shell command strings.

## Reference(s):

- [Senso.ai](https://senso.ai)
- [Senso.ai Search API](https://sdk.senso.ai/api/v1/search)
- [Senso.ai Generate API](https://sdk.senso.ai/api/v1/generate)
- [ClawHub skill page](https://clawhub.ai/samdickson22/skills/edith-senso-knowledge)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Text]

**Output Format:** [Concise spoken text with optional JSON API responses used as intermediate evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed to summarize the top one or two knowledge-base results without markdown, bullet points, or URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata and shipables.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
