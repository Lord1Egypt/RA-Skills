## Description: <br>
Parses PDF documents and image files, including long screenshots and scans, through Bytedance LAS-AI and returns structured Markdown with extracted text, tables, and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit PDFs, scanned documents, screenshots, local image files, URLs, or TOS paths for OCR and document parsing, then receive editable Markdown plus saved result artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local PDFs, screenshots, scans, extracted text, and images may be uploaded to Bytedance LAS or TOS services during parsing. <br>
Mitigation: Use the skill only for documents approved for external processing, and have the agent confirm before processing local files or creating download links. <br>
Risk: TOS credentials and buckets are required for local file upload and optional result archiving. <br>
Mitigation: Use scoped TOS credentials, a dedicated bucket, and environment variables rather than embedding secrets in prompts or files shared with others. <br>
Risk: Generated ZIP download links are presigned and time-limited, but anyone with the full URL may be able to access the archive while it is valid. <br>
Mitigation: Share download links only with intended recipients and rely on the generated download_url.txt file when the full signed URL must be preserved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-las-document-parse) <br>
- [Configuration](artifact/references/configuration.md) <br>
- [Commands](artifact/references/commands.md) <br>
- [Usage Examples](artifact/references/usage-examples.md) <br>
- [API Reference](artifact/references/api.md) <br>
- [FAQ](artifact/references/faq.md) <br>
- [Volcengine LAS API key documentation](https://www.volcengine.com/docs/6492/2191994?lang=zh) <br>
- [Volcengine TOS credential documentation](https://www.volcengine.com/docs/6291/65568?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown responses with local result files, complete JSON responses, downloaded images, and optional ZIP download links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include result.md, result.full.json, images/, images.json, and download_url.txt under a task-specific output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
