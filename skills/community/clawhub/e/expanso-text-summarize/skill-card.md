## Description:

Summarizes input text into 3-5 concise bullet points using AI with Expanso Edge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to summarize supplied text into 3-5 bullet points from CLI or local MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP mode can expose an unauthenticated summarization endpoint on all network interfaces.

Mitigation: Bind the service to 127.0.0.1 and add authentication before exposing it beyond the local machine.

Risk: Remote OpenAI mode may send submitted text and authentication material outside the local environment.

Mitigation: Use the local Ollama backend for sensitive text, or ensure users understand what is sent before use.

Risk: OpenAI-backed usage can create unexpected API costs.

Mitigation: Monitor API usage and configure spending limits when using the OpenAI backend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-text-summarize)
- [Publisher profile](https://clawhub.ai/user/aronchick)
- [Expanso Edge](https://expanso.io)
- [Expanso pipeline schema](https://docs.expanso.io/schemas/pipeline.schema.json)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object with a bulleted summary string and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes model, mode, input hash, trace ID, timestamp, and input length metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
