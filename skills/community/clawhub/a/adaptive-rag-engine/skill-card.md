## Description: <br>
Adaptive RAG Engine helps agents decide when and how to retrieve memory using capsule pre-filtering, vector search, reranking, CRAG evaluation, and final consistency checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luaqnyin](https://clawhub.ai/user/luaqnyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a protocol layer for memory retrieval, query routing, relevance evaluation, and retrieval quality checks in OpenClaw memory workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local capsule index can contain metadata and short summaries derived from memory notes, which may expose sensitive personal, medical, financial, or business information if those notes contain it. <br>
Mitigation: Review memory topics before running the index script, avoid indexing secrets or highly sensitive notes, and keep the generated local index access-controlled. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luaqnyin/adaptive-rag-engine) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, text] <br>
**Output Format:** [Markdown guidance with optional shell commands plus JSON or text reports from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; the index script writes a local .capsule-index.json file for OpenClaw memory topics.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
