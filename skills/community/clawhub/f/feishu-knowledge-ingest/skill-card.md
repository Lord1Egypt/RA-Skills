## Description: <br>
Batch-ingests Feishu folder or attachment inputs into report-first knowledge artifacts by classifying files, extracting supported DOCX/PDF text, and writing reviewable reports without directly updating memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiasdobi](https://clawhub.ai/user/kaiasdobi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base maintainers use this skill to process Feishu folders or shared attachments into structured, reviewable knowledge-ingestion outputs. It is suited for controlled document ingestion workflows where extracted content, failures, confidence, and memory candidates must be reviewed before adoption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This release is mainly a local parsing skeleton, not a complete Feishu connector. <br>
Mitigation: Confirm any Feishu listing, download, or native-document reader path before relying on full Feishu workspace coverage. <br>
Risk: Generated reports and memory candidates may contain sensitive extracted document content. <br>
Mitigation: Scope input directories narrowly and review ingest-report.md and MEMORY.candidate.md before importing, storing, or sharing outputs. <br>
Risk: Processing untrusted DOCX or PDF files depends on python-docx and pypdf behavior. <br>
Mitigation: Use vetted pinned dependency versions and apply file-size and runtime limits for untrusted documents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaiasdobi/feishu-knowledge-ingest) <br>
- [Output examples](artifact/references/output_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSONL files, Guidance] <br>
**Output Format:** [Markdown reports and JSON Lines records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report-first outputs include ingest-report.md, kb-items.jsonl, failed-items.jsonl, and MEMORY.candidate.md; the skill does not directly write MEMORY.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
