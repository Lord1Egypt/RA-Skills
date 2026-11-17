## Description:

Generate text embeddings via AIMLAPI for semantic search, clustering, or high-dimensional text representations with text-embedding-3-large and other models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aimlapihello](https://clawhub.ai/user/aimlapihello)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to generate text embeddings for semantic search, clustering, and other vector-based text representation workflows through AIMLAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text and the AIMLAPI API key are sent to AIMLAPI.

Mitigation: Avoid embedding secrets, regulated data, or proprietary text unless the AIMLAPI account and data-handling terms are acceptable for that content.

Risk: Embedding responses are saved locally and may contain sensitive derived representations of the input text.

Mitigation: Write outputs only to approved storage locations and avoid committing generated embedding files that derive from sensitive content.

## Reference(s):

- [AIMLAPI Embeddings API Reference](references/endpoints.md)
- [AIMLAPI Embeddings Endpoint](https://api.aimlapi.com/v1/embeddings)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON files, Guidance]

**Output Format:** [Markdown guidance with bash commands; embedding responses are saved as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIMLAPI_API_KEY; supports model, dimensions, encoding format, timeout, retry, and output directory options.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
