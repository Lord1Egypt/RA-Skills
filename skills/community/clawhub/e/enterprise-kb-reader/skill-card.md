## Description:

Retrieves and reads existing enterprise knowledge base content for business questions, policies, FAQs, procedures, product information, and project information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apanghu](https://clawhub.ai/user/apanghu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, support agents, and developers use this skill to query an already-initialized enterprise knowledge base, list available documents, view statistics, and retrieve read-only answers from existing content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query text can be sent to the configured external embedding provider even though the skill describes local-only knowledge base access.

Mitigation: Install only where external processing of query text is approved, review config.json before use, and avoid confidential questions unless the configured embedding provider is authorized for that data.

Risk: Unauthorized users may query enterprise knowledge base content if the skill is installed in a broadly accessible agent environment.

Mitigation: Restrict installation and execution to users who are allowed to query the enterprise KB, and use limited-scope API keys for the embedding provider.

Risk: Changing the embedding endpoint or related configuration can alter where query text is processed.

Mitigation: Limit who can modify configuration files and review the embedding provider, model, endpoint, and API key handling before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apanghu/skills/enterprise-kb-reader)
- [Configured DashScope-compatible embedding endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only query answers, detailed search results, document listings, and knowledge base statistics from an existing KB.]

## Skill Version(s):

1.1.0 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
