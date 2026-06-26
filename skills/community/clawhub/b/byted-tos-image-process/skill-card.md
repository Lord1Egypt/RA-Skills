## Description: <br>
Provides image processing capabilities for objects in Bytedance TOS using the official SDK, including image information retrieval, format conversion, resizing, visible watermarking, blind watermarking, and generic TOS image processing operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and transform images stored in Bytedance TOS without manually assembling each SDK call. It supports common image metadata, conversion, resize, watermark, blind-watermark, local-save, and save-back-to-TOS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires TOS credentials and can access or transform objects in configured buckets. <br>
Mitigation: Use short-lived, least-privilege STS credentials scoped to only the required buckets and object paths. <br>
Risk: Process strings, key-value options, output paths, and save-back targets can change what image operations run and where results are stored. <br>
Mitigation: Review --process, --kv, --output, --saveas-bucket, and --saveas-object values before execution. <br>
Risk: The release depends on the external tos Python SDK. <br>
Mitigation: Pin and review the tos SDK version used in production environments. <br>


## Reference(s): <br>
- [Volcengine TOS Image Processing Documentation](https://www.volcengine.com/docs/6349/153623) <br>
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/byted-tos-image-process) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus optional JSON or image files returned by the TOS SDK scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts can write processed images locally or save processed objects back to TOS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
