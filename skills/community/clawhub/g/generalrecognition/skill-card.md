## Description: <br>
图片通用文字 OCR，支持中英文及多语种。当用户说：这张图里的字提取成文本、截图 OCR 一下，或类似通用识图问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to extract text from user-provided screenshots or photos through JisuAPI's general OCR service, then format or analyze the recognized text for the user's workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are uploaded to JisuAPI for OCR processing. <br>
Mitigation: Use the skill only when external processing is acceptable, and avoid images containing passwords, IDs, medical, financial, or confidential business information. <br>
Risk: The skill requires a JisuAPI API key for external service access. <br>
Mitigation: Use a dedicated API key with appropriate limits and rotate it if exposure is suspected. <br>
Risk: Local image paths are accepted as input and the image contents are sent to the OCR service. <br>
Mitigation: Provide only intended workspace-relative image paths or vetted base64 payloads; the script blocks absolute paths and path traversal. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jisuapi/generalrecognition) <br>
- [Publisher profile](https://clawhub.ai/user/jisuapi) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI general text recognition documentation](https://www.jisuapi.com/api/generalrecognition/) <br>
- [JisuAPI OCR endpoint](https://api.jisuapi.com/generalrecognition/recognize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Shell commands, Configuration] <br>
**Output Format:** [JSON containing recognized text lines or structured error details; agents typically convert the result into concise text or Markdown for the user.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, a JISU_API_KEY environment variable, and either a workspace-relative image path or a base64 image payload.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
