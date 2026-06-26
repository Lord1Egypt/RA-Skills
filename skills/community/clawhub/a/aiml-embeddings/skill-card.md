## Description: <br>
Generate text embeddings via AIMLAPI for semantic search, clustering, or high-dimensional text representations with text-embedding-3-large and other models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aimlapihello](https://clawhub.ai/user/aimlapihello) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to generate embedding vectors from text for semantic search, clustering, and other vector-based text workflows through AIMLAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is sent to AIMLAPI for embedding generation. <br>
Mitigation: Avoid embedding secrets, regulated data, or confidential documents unless approved for AIMLAPI processing. <br>
Risk: Generated embedding responses are saved locally. <br>
Mitigation: Use a safe output directory and handle saved JSON files according to the sensitivity of the source text. <br>
Risk: The skill requires an AIMLAPI credential. <br>
Mitigation: Use a dedicated AIMLAPI key where possible and keep AIMLAPI_API_KEY out of shared logs and files. <br>


## Reference(s): <br>
- [AIMLAPI Embeddings API Reference](references/endpoints.md) <br>
- [AIMLAPI Embeddings Endpoint](https://api.aimlapi.com/v1/embeddings) <br>
- [ClawHub Release Page](https://clawhub.ai/aimlapihello/aiml-embeddings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script writes JSON embedding responses to local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIMLAPI_API_KEY and sends input text to AIMLAPI before saving results in the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
