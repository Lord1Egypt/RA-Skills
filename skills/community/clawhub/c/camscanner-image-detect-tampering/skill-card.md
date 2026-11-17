## Description:

Detects whether an image appears to have been photoshopped, manipulated, retouched, or otherwise tampered with using CamScanner's manipulation-detection service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camscanner-ai](https://clawhub.ai/user/camscanner-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check a user-selected image or scanned document for signs of tampering and report the returned `is_tampered` and `result_text` fields in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-selected images to CamScanner's servers for analysis.

Mitigation: Use it only when third-party image processing is acceptable, and avoid highly sensitive, regulated, or confidential images unless policy permits that data flow.

## Reference(s):

- [CamScanner homepage](https://www.camscanner.com)
- [CamScanner AI tools API base](https://ai-tools.camscanner.com)
- [ClawHub skill page](https://clawhub.ai/camscanner-ai/skills/camscanner-image-detect-tampering)
- [ClawHub publisher profile](https://clawhub.ai/user/camscanner-ai)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain-language response with JSON result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports `is_tampered` and `result_text`; does not download an output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
