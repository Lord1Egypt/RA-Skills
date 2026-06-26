## Description: <br>
Converts DOCX files into compact Markdown or JSON for review, applies structured edit JSON back to DOCX with tracked revisions and comments, and finalizes documents by accepting revisions and removing comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanweiliang323868-del](https://clawhub.ai/user/yanweiliang323868-del) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
Developers and document-review agents use this skill to extract DOCX content into token-efficient Markdown or structured JSON, produce targeted edit JSON, write those edits back with Word tracked changes and comments, and create a clean final DOCX after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts read DOCX contents and write derived files, so an incorrect path or output choice can expose or overwrite sensitive document data. <br>
Mitigation: Run the workflow on document copies, choose explicit output paths, and review generated DOCX files before replacing originals. <br>
Risk: The finalize step removes tracked changes and comments from the output. <br>
Mitigation: Finalize only after human approval and retain the reviewed DOCX with tracked revisions/comments as an audit copy. <br>
Risk: Runtime dependencies are version ranges rather than exact pins. <br>
Mitigation: Pin and review Python dependency versions in sensitive or regulated environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanweiliang323868-del/docx-md) <br>
- [LLM-oriented DOCX pipeline](references/llm-pipeline.md) <br>
- [OOXML reference for DOCX](references/ooxml.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON edit structures; supporting scripts produce Markdown, JSON, and DOCX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read output uses blockIndex markers for edit targeting; finalize output removes tracked changes and comments.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and LICENSE.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
