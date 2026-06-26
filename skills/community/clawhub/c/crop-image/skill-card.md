## Description: <br>
Crop Image helps an agent crop images through the deployed service using URL-based or file-upload API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Effimail](https://clawhub.ai/user/Effimail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to crop an image by URL or uploaded file and return the cropped image URL, original size, and face-detection flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected image URLs or uploaded local image files are sent to ImageClaw for processing. <br>
Mitigation: Avoid confidential, regulated, or private images unless the service's privacy and retention practices are approved for the use case. <br>
Risk: The skill depends on an external image-processing API that can return validation, decode, service, or network errors. <br>
Mitigation: Validate URL, width, and height before calling the service; return the original status code and detail; retry only transient 500 responses or network timeouts. <br>


## Reference(s): <br>
- [Crop Image on ClawHub](https://clawhub.ai/Effimail/crop-image) <br>
- [ImageClaw API documentation](https://api.imageclaw.net/docs) <br>
- [ImageClaw homepage](https://imageclaw.net) <br>
- [ImageClaw API base URL](https://api.imageclaw.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return cropped_url, original_size, face_detected, or HTTP status and detail on failure.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
