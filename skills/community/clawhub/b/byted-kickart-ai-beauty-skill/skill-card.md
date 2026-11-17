## Description:

Analyzes user-provided JPG or PNG images, applies AI beauty enhancement to detected people, and returns enhanced image links or batch ZIP output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to apply automated portrait beautification to a single image, multiple image URLs, or an archive of images through the Volcengine/Kickart service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are sent to the remote Volcengine/Kickart service for processing.

Mitigation: Use the skill only with images approved for that service and avoid sensitive or regulated images unless the deployment has appropriate data-handling controls.

Risk: Credential handling guidance in the artifact asks users to expose AK/SK values and echo credential-related environment variables.

Mitigation: Provide tightly scoped, disposable credentials through a safe secret mechanism; do not paste long-lived AK/SK secrets into chat or run the credential-echo preflight as written.

Risk: The skill accepts remote image URLs and image archives, which can increase input-handling risk.

Mitigation: Avoid untrusted URLs or archives until URL allowlisting, size limits, log redaction, and safe archive extraction controls are in place.

Risk: The authoritative security verdict is suspicious.

Mitigation: Review the skill, its credential flow, and its input-processing behavior before installation or deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/skills/byted-kickart-ai-beauty-skill)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown text with image URLs or local ZIP paths; the helper scripts write JSON result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-image processing returns a signed image URL; batch URL and archive processing can return per-image results and a ZIP path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
