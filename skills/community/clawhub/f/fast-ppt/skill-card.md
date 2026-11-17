## Description:

Converts PDFs and other documents into editable PPTX presentations through cloud processing and returns a ppt.siping.me download link after user consent for third-party upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Fast PPT to convert PDFs, DOCX, Markdown, TXT, and presentation files into editable PPTX outputs with either AI theme layout or PDF-only conversion. It is appropriate only when the user accepts third-party cloud processing of the uploaded file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Whole user documents are uploaded to siping.me/pingPPT for cloud processing, so confidential, regulated, personal, medical, financial, or contract-restricted content may leave the user's environment.

Mitigation: Warn users before upload, obtain explicit consent, and avoid or redact sensitive files; use local tooling when cloud upload is not acceptable.

Risk: The security evidence reports that whole documents are sent to a third-party service over plain HTTP.

Mitigation: Install and use the skill only when this transport risk is acceptable, and prefer a verified HTTPS API endpoint before uploading sensitive material.

Risk: AI theme mode may send document contents to an LLM for slide restructuring.

Mitigation: Use PDF-only conversion when LLM processing is not desired, while still treating the cloud upload itself as third-party data transfer.

## Reference(s):

- [Fast PPT homepage](https://ppt.siping.me)
- [ClawHub Fast PPT skill page](https://clawhub.ai/sipingme/skills/fast-ppt)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown response with a hosted PPTX download link and optional inline curl commands for agent execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PPTX files are delivered through siping.me download links and are described by the skill as temporary cloud-hosted outputs.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
