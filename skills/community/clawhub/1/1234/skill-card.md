## Description: <br>
Use for RAGFlow dataset and retrieval tasks: create, list, inspect, update, or delete datasets; list, upload, update, or delete documents in a dataset; start or stop parsing uploaded documents; check parser status through `parse_status.py`; and retrieve relevant chunks from RAGFlow datasets with `search.py`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caesergattuso](https://clawhub.ai/user/caesergattuso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage RAGFlow datasets, documents, parsing jobs, model listings, and retrieval queries through bundled scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete remote RAGFlow datasets and documents. <br>
Mitigation: Review exact dataset and document IDs before confirming destructive operations. <br>
Risk: The skill can optionally save a RAGFlow API key locally for repeated use. <br>
Mitigation: Use a minimally scoped API key and avoid saving credentials on shared or backed-up machines. <br>
Risk: Document bytes and metadata are sent to the configured RAGFlow server. <br>
Mitigation: Install and use the skill only with a trusted RAGFlow server. <br>


## Reference(s): <br>
- [Output Format Reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, tables, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script results may include RAGFlow API responses, document status snapshots, search chunks, and error objects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
