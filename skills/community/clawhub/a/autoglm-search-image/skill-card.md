## Description:

Searches for images with the AutoGLM image search API based on user-provided keywords and obtains its bearer token from a local token service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfujian](https://clawhub.ai/user/flyfujian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search for image results by keyword and present returned image URLs, captions, and sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image search terms are sent to the AutoGLM remote API.

Mitigation: Avoid entering confidential, regulated, or sensitive search terms unless that use is approved.

Risk: The skill automatically uses a bearer token from the local token service at 127.0.0.1:53699.

Mitigation: Install and run it only in environments where that local token broker is expected and trusted.

Risk: The bundled application signing key is exposed in the artifact.

Mitigation: Do not rely on the bundled signing key as a confidential secret.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyfujian/skills/autoglm-search-image)
- [AutoGLM image search API endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/search-image)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands]

**Output Format:** [Markdown image entries and command-line text; the bundled script emits formatted JSON from the API response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user search query, sends the query to AutoGLM, and uses a bearer token from the local token broker.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
