## Description:

Analyze text and return a sentiment score from -1 for negative sentiment to +1 for positive sentiment using Expanso Edge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to score the sentiment of supplied text and return a structured score, label, and confidence value. It supports CLI execution and an HTTP/MCP-style server pipeline through Expanso Edge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server mode listens on all network interfaces without authentication.

Mitigation: Run the server only on trusted local networks or add authentication, ingress restrictions, and request limits before exposing it.

Risk: Remote sentiment analysis can send analyzed text to OpenAI or another configured backend and consume the operator's quota.

Mitigation: Avoid sending sensitive text to remote backends unless approved, and configure budget controls or use the local Ollama backend where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-sentiment-score)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Skill metadata](artifact/skill.yaml)
- [CLI pipeline](artifact/pipeline-cli.yaml)
- [MCP pipeline](artifact/pipeline-mcp.yaml)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing score, label, confidence, and metadata fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores range from -1 to +1; labels are positive, negative, or neutral.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
