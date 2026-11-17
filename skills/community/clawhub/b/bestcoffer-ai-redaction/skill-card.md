## Description:

Bestcoffer Ai Redaction helps an agent guide personal users through uploading a document, collecting redaction instructions, and returning a task link for AI-assisted file redaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marsxh](https://clawhub.ai/user/marsxh)

### License/Terms of Use:

MIT-0

## Use Case:

Personal users and agents use this skill to redact sensitive information from PDFs, Word files, images, spreadsheets, and text files using natural-language instructions or user-provided redaction rules. The workflow requires an API key, user confirmation before processing, and returns a link for status and result download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files and redaction instructions are sent to BestCoffer's external service.

Mitigation: Use only when that external processing is acceptable for the document's sensitivity and applicable policy requirements.

Risk: API keys can be exposed if pasted into chat or handled outside the platform secret mechanism.

Mitigation: Configure the API key through the platform's secret or environment-variable mechanism.

Risk: Returned task URLs may grant access to processing status or redacted results.

Mitigation: Treat task URLs as sensitive and share them only with authorized users.

Risk: Local debug logs may retain filenames, file paths, redaction instructions, and result links.

Mitigation: Review log retention and access controls before use with sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marsxh/skills/bestcoffer-ai-redaction)
- [Publisher profile](https://clawhub.ai/user/marsxh)
- [BestCoffer API console](https://apiconsole.bestcoffer.com.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with a runtime command and JSON result containing taskUrl and errorMessage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, and a configured API key; processes one file up to 10MB and returns a task URL for status and download.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
