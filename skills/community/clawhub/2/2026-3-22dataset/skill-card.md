## Description: <br>
Use for RAGFlow dataset tasks: create, list, inspect, update, or delete datasets; upload, list, update, or delete documents; start or stop parsing; check parse status; retrieve chunks with `search.py`; and list configured models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redredrrred](https://clawhub.ai/user/redredrrred) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage RAGFlow datasets and documents, run parsing workflows, inspect parse status, list available models, and retrieve chunks from configured datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete remote RAGFlow datasets and documents. <br>
Mitigation: Use a least-privilege RAGFlow API key and require exact dataset or document IDs plus explicit confirmation before delete or bulk update operations. <br>
Risk: The skill uploads local files to the configured RAGFlow server. <br>
Mitigation: Set RAGFLOW_API_URL only to the intended server and upload sensitive files only after user approval. <br>
Risk: Parsing operations may run asynchronously and return before processing completes. <br>
Mitigation: Use parse status checks and surface returned progress or failure messages exactly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/redredrrred/2026-3-22dataset) <br>
- [Publisher profile](https://clawhub.ai/user/redredrrred) <br>
- [Output Format Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON returned from bundled command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers --json for exact API fields; requires RAGFLOW_API_URL and RAGFLOW_API_KEY.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
