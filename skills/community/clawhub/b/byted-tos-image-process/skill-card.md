## Description:

Provides image processing capabilities for objects in Bytedance TOS using the official SDK, including image info retrieval, format conversion, resizing, and watermarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and transform images stored in Bytedance TOS, including metadata lookup, format conversion, resizing, visible watermarking, blind watermarking, and saving processed outputs locally or back to TOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses TOS credentials and can access configured buckets.

Mitigation: Install only where the agent is intended to access those buckets and use short-lived, least-privilege STS credentials.

Risk: The generic processor can pass arbitrary TOS image processing strings.

Mitigation: Avoid exposing the generic processor to untrusted task input and review process strings before execution.

Risk: The unpinned tos dependency can change behavior across installations.

Mitigation: Pin the tos package to a reviewed version before deployment.

Risk: A misconfigured endpoint could send requests outside the intended TOS service.

Mitigation: Set TOS_ENDPOINT to an official HTTPS TOS endpoint for the target region.

## Reference(s):

- [Volcengine TOS Image Processing documentation](https://www.volcengine.com/docs/6349/153623)
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-tos-image-process)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to produce local image files or save processed objects back to TOS when credentials and bucket settings are provided.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
