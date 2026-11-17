## Description:

Ingests Taiwan civil court judgment HTML or PDF files into Qdrant with Ollama embeddings while preserving traceability, deduplication, and incremental updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex02131926](https://clawhub.ai/user/alex02131926)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and legal-technology operators use this skill to ingest archived Taiwan civil court judgments into Qdrant collections for semantic retrieval and RAG workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full judgment text and identifying metadata can be sent to configurable Ollama and Qdrant HTTP endpoints.

Mitigation: Use only controlled endpoints, preferably localhost or authenticated HTTPS, and check OLLAMA_URL and QDRANT_URL before running ingestion.

Risk: Out-of-scope or mixed FJUD/FINT inputs may be ingested or mislabeled because the documented v1 limitation hardcodes the system metadata to FJUD.

Mitigation: Use a dedicated run folder containing Taiwan civil judgment inputs only, and avoid mixed FJUD/FINT inputs unless the metadata limitation is acceptable.

Risk: Running the scripts creates persistent Qdrant collections and local ingest_report.md, ingest_manifest.jsonl, and possibly issues.jsonl files.

Mitigation: Run in an environment where persistent vector collections and local report artifacts are expected and review generated reports after ingestion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex02131926/skills/civil-judgment-taiwan-vectorstore)
- [Internals Reference](references/internals.md)
- [Extraction Algorithm Design](references/extraction-design.md)
- [Taiwan Civil Judgment Vector DB Plan](references/judgment-rag-ingestion-plan.md)
- [Qdrant](https://qdrant.tech)
- [Ollama](https://ollama.com)
- [OpenClaw](https://openclaw.dev)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command blocks and ingestion status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent Qdrant collections and local ingest reports or manifests when the ingestion scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence and changelog, released 2026-03-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
