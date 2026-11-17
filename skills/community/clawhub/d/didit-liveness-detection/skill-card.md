## Description:

Detects liveness from a single selfie image via the Didit standalone API, returning liveness score, face quality, and luminance metrics for passive anti-spoofing checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and identity verification teams use this skill to add passive liveness and anti-spoofing checks to workflows that accept a single selfie image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive face images through a third-party liveness API.

Mitigation: Use it only with clear consent from the person in the image and confirm that the deployment meets applicable biometric, privacy, and retention requirements.

Risk: API requests may be saved by the provider by default.

Mitigation: Set save_api_request=false unless retention is explicitly required and approved.

Risk: vendor_data can carry identifying information if callers pass personal data.

Mitigation: Avoid personal or directly identifying values in vendor_data; use scoped opaque identifiers when session tracking is needed.

Risk: The Didit API key grants access to account capabilities and request history.

Mitigation: Restrict access to DIDIT_API_KEY, store it in a secret manager, rotate it when exposed, and limit account permissions where available.

## Reference(s):

- [Didit Documentation](https://docs.didit.me)
- [Didit Passive Liveness API](https://docs.didit.me/standalone-apis/passive-liveness)
- [Didit Liveness Overview](https://docs.didit.me/core-technology/liveness/overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python, TypeScript, shell command, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIDIT_API_KEY and a supported single-face image file.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
