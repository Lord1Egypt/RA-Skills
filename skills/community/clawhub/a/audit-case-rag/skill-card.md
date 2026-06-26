## Description: <br>
Local-first RAG workflow for commercial real estate audit and investigation case folders that indexes PDF and Office evidence, applies case and stage filters, and returns cited query results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack4world](https://clawhub.ai/user/jack4world) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Audit, investigation, and compliance teams use this skill to organize a single case folder, build a local searchable index, and retrieve evidence with page-level citations for workpapers, rectification tracking, and investigation questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated manifests, converted PDFs, and saved indexes can contain sensitive audit or investigation text. <br>
Mitigation: Keep the case folder and output directory private, avoid committing generated files, and restrict access to users authorized for the case. <br>
Risk: Office document conversion uses a local LibreOffice executable on input documents. <br>
Mitigation: Use a trusted LibreOffice installation and sandbox conversion when processing documents from untrusted sources. <br>
Risk: Indexing unintended folders can expose unrelated case material in search results. <br>
Mitigation: Index only the specific case directory intended for processing and verify the generated manifest before querying. <br>


## Reference(s): <br>
- [Case Folder Template](references/case-folder-template.md) <br>
- [ClawHub release page](https://clawhub.ai/jack4world/audit-case-rag) <br>
- [Publisher profile](https://clawhub.ai/user/jack4world) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and text query output with citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local indexing creates manifest.jsonl and a joblib index; query output includes ranked evidence snippets and source citations when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
