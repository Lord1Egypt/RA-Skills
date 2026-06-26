## Description: <br>
Provides expert guidance for designing, optimizing, evaluating, and debugging production-ready Retrieval-Augmented Generation systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan, build, troubleshoot, and operationalize RAG systems across ingestion, chunking, embeddings, retrieval, generation, evaluation, deployment, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may index secrets, unnecessary PII, or documents that should not be available to every requester. <br>
Mitigation: Define allowed document sources before ingestion, enforce document-level permissions during retrieval, and exclude secrets or unnecessary PII from indexes. <br>
Risk: Embeddings, metadata, logs, and cached responses can retain sensitive source information after deployment. <br>
Mitigation: Set retention rules for embeddings, metadata, logs, and cached responses, and align them with the sensitivity of the indexed corpus. <br>


## Reference(s): <br>
- [RAG Engineering release page](https://clawhub.ai/1kalin/afrexai-rag-engineering) <br>
- [Publisher profile: 1kalin](https://clawhub.ai/user/1kalin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with structured checklists, tables, YAML examples, pseudocode, and command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Methodology-only skill with no executable code or hidden access requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
