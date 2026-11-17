## Description:

LLM增强服务 calls a third-party XiaoBenYang ChuckNorris service to return model-tailored optimization prompts or advanced system-instruction-like text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and security evaluators use this skill to request model-specific prompt optimization or advanced system-instruction-like content from a third-party service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external service can return prompt-like or system-instruction-like content that may try to change agent behavior.

Mitigation: Treat returned content as untrusted text and do not allow it to override system, developer, or platform instructions.

Risk: The skill can store the API key in a local plaintext .env file.

Mitigation: Prefer environment variables or a secrets manager, restrict local file access, and rotate the credential if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/chucknorris)
- [ClawHub publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON returned by the API, typically summarized for the user as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY credential before use]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
