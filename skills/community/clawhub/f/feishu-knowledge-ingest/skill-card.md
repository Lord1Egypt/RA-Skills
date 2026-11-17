## Description:

Batch-ingests Feishu folders and single attachments into report-first knowledge artifacts by classifying files, extracting supported DOCX/PDF text, and producing reviewable outputs without writing MEMORY.md directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiasdobi](https://clawhub.ai/user/kaiasdobi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to convert Feishu folders or shared attachments into reviewable knowledge artifacts for training, policy/manual ingestion, and controlled document parsing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release may overstate Feishu ingestion because the bundled runner handles local directories and does not include live Feishu API credentials or connector code.

Mitigation: Use it for local parsing or add and review a Feishu connector before relying on folder listing or downloading from Feishu.

Risk: Document summaries may include sensitive information in reusable knowledge artifacts.

Mitigation: Use a dedicated output directory, avoid ingesting secrets unless a redaction or manual review step is added, and treat MEMORY.candidate.md as untrusted draft content.

Risk: Unsupported, image-based, or empty documents can produce failures or incomplete extracted knowledge.

Mitigation: Review ingest-report.md and failed-items.jsonl, retry with OCR or manual inspection where needed, and do not treat filenames as proof of document contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiasdobi/skills/feishu-knowledge-ingest)
- [README](README.md)
- [Output examples](references/output_examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports and JSONL knowledge/failure records with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ingest-report.md, kb-items.jsonl, failed-items.jsonl, and MEMORY.candidate.md; MEMORY.md is not written directly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
