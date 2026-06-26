## Description: <br>
Chain of Verification (CoVe) fact-checks responses against the user's knowledge base, memory, and optional web search before they are presented. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bhawanakatiyar](https://clawhub.ai/user/bhawanakatiyar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to verify factual claims in OpenClaw responses against local workspace files, memory, optional vector stores, and web search before sending user-facing answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read broad OpenClaw workspace and memory content and may send verification context to configured LLM, search, embedding, vector-store, or sidecar services. <br>
Mitigation: Keep custom document paths empty or tightly scoped, disable web and vector features for sensitive work, and avoid use around secrets, regulated data, or private conversations unless clear data-handling controls are in place. <br>
Risk: Verification results and auto-corrections can still be wrong or unverifiable. <br>
Mitigation: Review reported inaccuracies and corrections before presenting final answers, and use strict mode when unverifiable claims should block output. <br>
Risk: The security verdict requires review before installation. <br>
Mitigation: Review the skill and its configured data sources before deployment, especially in environments with sensitive workspace or memory content. <br>


## Reference(s): <br>
- [ClawHub cove listing](https://clawhub.ai/bhawanakatiyar/cove-plugin) <br>
- [OpenClaw](https://openclaw.sh) <br>
- [Qdrant documentation](https://qdrant.tech/documentation/) <br>
- [Chroma documentation](https://docs.trychroma.com/) <br>
- [Weaviate documentation](https://weaviate.io/developers/weaviate) <br>
- [Milvus documentation](https://milvus.io/docs/) <br>
- [Redis vector search documentation](https://redis.io/docs/interact/search-and-query/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Plain text reports or JSON verification results, with optional corrected response text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish verified, inaccurate, and unverifiable claims; strict mode can fail on unverifiable claims.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
