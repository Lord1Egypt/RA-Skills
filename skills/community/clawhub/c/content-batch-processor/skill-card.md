## Description: <br>
Batch content-processing skill for formatting text, generating summaries, extracting keywords, converting file formats, and organizing content workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[careytian-ai](https://clawhub.ai/user/careytian-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, researchers, and developers use this skill to process groups of documents for formatting, summarization, keyword extraction, format conversion, translation, analysis, and file organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad local file-processing and command-execution authority. <br>
Mitigation: Run it only in trusted workspaces, prefer copies or a dedicated output folder, and require explicit confirmation before overwrites, renames, batch edits, or command execution. <br>
Risk: Batch processing can affect many documents at once, including confidential content. <br>
Mitigation: Review file scopes before processing and avoid confidential documents unless the processing path and storage location are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/careytian-ai/content-batch-processor) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code examples and batch-processing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file reads, writes, conversions, renames, PDF/image processing, and batch execution patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog, released 2026-03-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
