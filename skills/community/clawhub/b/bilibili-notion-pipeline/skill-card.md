## Description:

Downloads Bilibili or b23 videos, transcribes audio, uploads mp4 files, creates or updates Notion transcript pages, writes transcript blocks, and optionally appends Markdown summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiing](https://clawhub.ai/user/hiing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Bilibili or b23 video content into Notion transcript pages with optional structured summaries and download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload video files to a configured external destination.

Mitigation: Review the upload destination, require HTTPS, and use a narrowly scoped upload token before running the pipeline.

Risk: The skill can archive existing top-level Notion page blocks when replace-children behavior is enabled.

Mitigation: Use replace-children only when the target Notion page can safely have existing top-level blocks archived.

Risk: Cleanup modes can delete local transcript, audio, or video files.

Mitigation: Inspect generated metadata paths first and use cleanup-mode none until deletion behavior is confirmed.

## Reference(s):

- [Workflow Notes](references/workflow.md)
- [Summary Template](references/summary-template.md)
- [CloudFlare-ImgBed upload backend reference](https://github.com/MarSeventh/CloudFlare-ImgBed)
- [ClawHub skill page](https://clawhub.ai/hiing/skills/bilibili-notion-pipeline)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, shell commands, JSON metadata, transcript text, and Notion block content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Notion pages, upload mp4 files to a configured destination, and delete temporary files according to cleanup mode.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
