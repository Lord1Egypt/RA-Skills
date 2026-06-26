## Description: <br>
Use the Datris Platform as a long-term semantic memory layer through the Datris MCP server, with local markdown memory files as the canonical source and Datris as the retrieval index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datris](https://clawhub.ai/user/datris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to ingest, synchronize, and retrieve long-term memory from local markdown notes through Datris. It is intended for memory bootstrap, incremental sync, semantic search, and recall workflows where local files remain the source of truth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory notes may contain secrets or sensitive personal data before they are indexed for recall. <br>
Mitigation: Review MEMORY.md and memory/*.md before ingestion, remove sensitive content, and use the skill only with a trusted Datris MCP server and storage account. <br>
Risk: A memory pipeline bootstrapped from consolidated uploads can break per-file provenance and incremental sync behavior. <br>
Mitigation: Use one upload per canonical memory file, verify source filenames in retrieval results, and reset/re-ingest if consolidated corpus filenames appear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datris/datris-memory) <br>
- [Publisher profile](https://clawhub.ai/user/datris) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with operational steps and command-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Datris MCP operations for upload, polling, search, and sync workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
