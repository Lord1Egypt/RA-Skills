## Description: <br>
Alibaba Quark Scan Free helps agents handle explicit image and document scanning requests through Quark Scan scenarios for image enhancement, handwriting removal, and document scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route explicit image or document inputs to Quark Scan workflows for clearer images, removal of handwriting from printed documents, and basic document scan optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language and conflicting batch-processing claims may cause unintended file uploads to an external service. <br>
Mitigation: Use the skill only for explicit image or document scan requests, confirm the intended scene before execution, and avoid relying on claimed batch behavior until the publisher clarifies it. <br>
Risk: Image or document content is sent to a third-party scanning service for processing. <br>
Mitigation: Avoid sensitive documents unless the user accepts third-party processing and applicable privacy requirements are satisfied. <br>
Risk: API keys and generated temporary files can expose sensitive operational data if handled carelessly. <br>
Mitigation: Store credentials in environment variables, rotate leaked keys promptly, and remove temporary image outputs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/alibaba-quark-scan-free) <br>
- [Quark Scan developer console](https://scan.quark.cn/business) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON service results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful processing can return local temporary file paths for generated images; supported inputs include image URLs, local image paths, and Base64 image data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
