## Description:

CareMax OCR helps agents upload medical report files to the CareMax Health API, run OCR, review structured results, and save confirmed reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kittenyang](https://clawhub.ai/user/kittenyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and care workflows use this skill to upload PDF, JPG, PNG, or HEIC medical reports, extract structured OCR results, review them, and save confirmed reports. Agents can also resume interrupted OCR sessions and help manage pending sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can upload sensitive health files and extracted health data to an external API.

Mitigation: Require explicit user consent before upload or OCR, and use the skill only when the user trusts CareMax Health and the configured endpoint.

Risk: Broad activation terms may cause the agent to start upload or OCR when the user's intent is ambiguous.

Mitigation: Use explicit invocation or confirmation before processing medical files, especially in conversations that only mention upload, scan, or extraction generally.

Risk: The skill depends on the external caremax-auth sibling package for API calls, upload, OCR streaming, and authentication.

Mitigation: Pin or verify the caremax-auth source before installation and review how it handles credentials and medical data.

Risk: Delete operations can remove individual records or entire sessions.

Mitigation: Require a strong confirmation step before any record or session deletion.

## Reference(s):

- [CareMax OCR ClawHub listing](https://clawhub.ai/kittenyang/skills/caremax-ocr)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and JSON progress/result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the caremax-auth sibling dependency; streams OCR progress and waits for user approval before saving extracted reports.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
