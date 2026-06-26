## Description: <br>
Convert documents or text into PDF slide presentations via the Ruyi Converter API at nyoi.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lisiting01](https://clawhub.ai/user/lisiting01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn plain text, markdown, document URLs, or uploaded document content into PDF slide decks. It is suited for creating presentations, pitch decks, and visual summaries through the nyoi.io Ruyi Converter API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided notes, documents, URLs, and generated slide outputs are sent to nyoi.io and related storage infrastructure. <br>
Mitigation: Use the skill only for content that can be processed by that provider, and review privacy, retention, and access-control practices before sending regulated or highly confidential material. <br>
Risk: API keys, job IDs, webhook secrets, and pre-signed download links can grant access to jobs or generated files. <br>
Mitigation: Treat these values as private, avoid exposing them in public logs or chat transcripts, and resend or refresh download links only through trusted channels. <br>
Risk: Generated PDF download links are time-limited and may expire before delivery. <br>
Mitigation: Deliver the PDF as a file or media attachment when possible, and re-query the job endpoint for a fresh URL if the original link expires. <br>


## Reference(s): <br>
- [Ruyi Converter API Reference](references/api-reference.md) <br>
- [Ruyi Converter API](https://www.nyoi.io) <br>
- [ClawHub skill page](https://clawhub.ai/lisiting01/doc-to-slides) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples; final user-facing artifact is a PDF slide deck attachment.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, file URL, base64 file, title, language, upload, job polling, webhook, and PDF download workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
