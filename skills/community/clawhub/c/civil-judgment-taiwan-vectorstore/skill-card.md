## Description: <br>
Ingest Taiwan civil court judgments (HTML or PDF) — exclusively covering Taiwan civil cases — into Qdrant with Ollama embeddings, preserving traceability, deduplication, and incremental updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex02131926](https://clawhub.ai/user/alex02131926) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and legal-data engineers use this skill to ingest Taiwan civil judgment HTML or PDF files into Qdrant for semantic retrieval and RAG workflows. It is scoped to Taiwan civil court judgments and preserves traceability through local paths, document URLs, deterministic IDs, manifests, and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document text is sent to local or configured Ollama and Qdrant endpoints during ingestion. <br>
Mitigation: Keep Ollama and Qdrant on localhost or trusted infrastructure, and configure endpoints intentionally. <br>
Risk: If a run folder mixes FJUD and FINT files, metadata can be mislabeled because the system metadata field is hardcoded to FJUD. <br>
Mitigation: Avoid mixed FJUD/FINT folders when metadata accuracy matters. <br>
Risk: The reasoning collection rebuild helper can recreate a Qdrant collection. <br>
Mitigation: Use rebuild behavior only when collection recreation is intended and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alex02131926/civil-judgment-taiwan-vectorstore) <br>
- [Extraction Algorithm Design](references/extraction-design.md) <br>
- [Internals](references/internals.md) <br>
- [Judgment RAG Ingestion Plan](references/judgment-rag-ingestion-plan.md) <br>
- [Qdrant](https://qdrant.tech) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; runtime artifacts include Markdown reports and JSON Lines manifests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The ingestion scripts create or update Qdrant vector collections and write per-run manifest and report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
