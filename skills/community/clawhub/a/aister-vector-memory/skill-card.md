## Description: <br>
Provides semantic vector search over Aister memory files using PostgreSQL, pgvector, and e5-large-v2 embeddings for Russian and English recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alekhm](https://clawhub.ai/user/alekhm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to index local Aister/OpenClaw memory files and retrieve related content by semantic meaning rather than exact keyword matching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may contain private information that would be copied into the vector database. <br>
Mitigation: Review memory files before indexing and exclude secrets, credentials, or other content that should not be stored for semantic recall. <br>
Risk: The embedding service and database add local services that could expose sensitive memory data if bound or configured too broadly. <br>
Mitigation: Keep the embedding service on localhost or another trusted endpoint and use a dedicated PostgreSQL user with minimal required permissions. <br>
Risk: Installation can require privileged package and PostgreSQL setup. <br>
Mitigation: Prefer the documented Docker setup or another isolated environment, and only enable shell autostart when automatic background operation is intended. <br>
Risk: The first embedding-service run downloads a large model from Hugging Face. <br>
Mitigation: Install only in environments where the initial network download and local model cache are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alekhm/aister-vector-memory) <br>
- [Artifact README](artifact/README.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [e5-large-v2 model](https://huggingface.co/intfloat/e5-large-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance, shell commands, Python scripts, environment configuration, and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes matched memory content, source metadata, timestamps, and similarity scores when JSON mode is used.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact README states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
