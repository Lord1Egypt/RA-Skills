## Description:

File Translate helps agents translate text, images, and common document formats with layout-preserving outputs through the 360 AI Translation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ray771](https://clawhub.ai/user/ray771)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate PDFs, Word files, slide decks, spreadsheets, images, and free-form text while preserving layout when supported. It is best suited for content that can be sent to a third-party translation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text, images, and whole documents are sent to 360's external translation service.

Mitigation: Avoid confidential, regulated, or classified content unless that transfer is acceptable, and test first with non-sensitive samples.

Risk: Credential and billing exposure can occur if a broad or long-lived API key is used.

Mitigation: Use a dedicated low-limit TRANSLATE_360_API_KEY and rotate or revoke it when no longer needed.

Risk: Returned result URLs may be accessible to anyone with the link during their validity window.

Mitigation: Download results promptly, avoid sharing result URLs, and prefer a patched version that validates downloaded result URLs before routine use.

## Reference(s):

- [360 AI Translation API Reference](artifact/references/api-reference.md)
- [360 AI Platform API Keys](https://ai.360.com/platform/keys)
- [File Translate on ClawHub](https://clawhub.ai/ray771/skills/360-translate)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands, translated strings, result URLs, and saved PDF or image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRANSLATE_360_API_KEY; sends requested text, images, or documents to 360's external translation service.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
