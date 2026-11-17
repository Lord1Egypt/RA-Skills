## Description:

Ingests documents into a user's Senso.ai knowledge base for retrieval through Edith smart glasses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samdickson22](https://clawhub.ai/user/samdickson22)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Edith smart glasses use this skill to add document-scale content or file contents to a Senso.ai knowledge base so it can be searched later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Senso API keys could be exposed if users paste them into chat or store them in agent memory.

Mitigation: Use a platform secret store for SENSO_API_KEY and avoid entering API keys directly into conversation history.

Risk: Shell command templates that upload arbitrary text or file contents can create command-execution or serialization risks.

Mitigation: Review commands before execution and prefer safe JSON serialization or a structured HTTP client for uploads.

Risk: The skill can upload user-provided content to Senso.ai.

Mitigation: Use it only for content the user intentionally wants added to the Senso.ai knowledge base.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samdickson22/skills/edith-senso-ingest)
- [Senso.ai](https://senso.ai)
- [Senso raw content endpoint](https://sdk.senso.ai/api/v1/content/raw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with concise voice-response text and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides content upload to Senso.ai and brief Edith voice confirmations.]

## Skill Version(s):

1.0.0 (source: shipables.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
