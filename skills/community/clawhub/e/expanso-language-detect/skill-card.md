## Description:

Detects the language of input text using AI through Expanso Edge CLI or MCP pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to detect the natural language of supplied text from a CLI pipeline or an HTTP-accessible MCP pipeline and receive a structured result with language, code, and confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send analyzed text to OpenAI when using the remote backend.

Mitigation: Use only with text that is approved for OpenAI processing, or configure a local backend where appropriate.

Risk: The MCP mode opens an unauthenticated network endpoint that can spend the operator's OpenAI quota.

Mitigation: Bind the service to localhost or a protected interface, add authentication, and enforce request size, rate, and quota limits before network exposure.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime pipeline returns JSON fields for language, ISO 639-1 code, confidence, and metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
