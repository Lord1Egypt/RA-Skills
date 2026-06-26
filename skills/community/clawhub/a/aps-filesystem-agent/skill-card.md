## Description: <br>
Use this skill whenever an APS production scheduling agent needs to read, search, update, or maintain a local filesystem-based knowledge base for rules, client memory, problem schemas, vector indexing, and audit history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JasonDZS](https://clawhub.ai/user/JasonDZS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
APS developers and scheduling agents use this skill to operate a local knowledge base that stores domain rules, customer memory, problem schemas, solver configuration, decision logs, and pending knowledge proposals. It supports retrieval, human-reviewed knowledge updates, vector index maintenance, and Git-backed audit history for scheduling workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local APS knowledge base can contain sensitive customer, shop-floor, source-quote, and decision-history data. <br>
Mitigation: Keep aps_knowledge_base access-controlled and redact secrets or unnecessary personal data from source quotes, proposals, and decision logs. <br>
Risk: Incorrect proposed rules or memory updates could affect future scheduling decisions if accepted without review. <br>
Mitigation: Review pending proposals before confirmation and rely on the documented pending_review workflow before moving content into the active knowledge base. <br>
Risk: Vector index or dependency drift can affect semantic retrieval quality. <br>
Mitigation: Use backups or Git history for recovery, rebuild the vector index when knowledge changes, and pin or vet ChromaDB if vector indexing is used. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JasonDZS/aps-filesystem-agent) <br>
- [APS Knowledge Base JSON Schemas](references/schemas.md) <br>
- [APS Knowledge Base Utility Scripts](references/scripts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, bash, and JSON examples for local knowledge-base operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The documented write path creates pending JSON proposals and audit records locally, with human confirmation expected before live knowledge-base updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
