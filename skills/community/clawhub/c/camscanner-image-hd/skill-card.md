## Description:

Uses CamScanner to enhance image clarity and quality with auto-crop, HD super filter processing, and optional moire-pattern removal when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to enhance photos or scanned documents through CamScanner's image HD workflow and to choose demoire mode only when moire removal is requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images or scanned documents are uploaded to CamScanner servers for processing.

Mitigation: Use the skill only for files where external processing by CamScanner is acceptable; avoid sensitive IDs, financial records, medical documents, or confidential business files unless approved.

Risk: Enhancement mode selection can produce unintended results if demoire processing is used when the user did not request moire removal.

Mitigation: Use the default HD enhancement path unless the user explicitly asks to remove moire patterns.

## Reference(s):

- [CamScanner Homepage](https://www.camscanner.com)
- [CamScanner Image HD API Base](https://ai-tools.camscanner.com)
- [ClawHub Skill Page](https://clawhub.ai/camscanner-ai/skills/camscanner-image-hd)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local image files after uploading selected inputs to CamScanner servers for processing.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata version: 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
