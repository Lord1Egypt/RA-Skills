## Description: <br>
File Translate helps agents translate text, images, and documents through the 360 AI Translation API while preserving document layout and image context where supported. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ray771](https://clawhub.ai/user/ray771) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to translate text, an image, or a document such as a PDF, Word file, spreadsheet, presentation, or ePub. It is intended for users who accept sending the selected content to 360's translation service for processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text, images, and documents selected for translation are sent to 360's API for processing. <br>
Mitigation: Use only when that transfer is acceptable, and avoid confidential or regulated files unless the user has approved the data handling risk. <br>
Risk: Translated image and document results may be returned through temporary, public-style URLs. <br>
Mitigation: Download results promptly, avoid sharing result URLs, and do not rely on temporary URLs as protected storage. <br>
Risk: The skill requires a 360 API key for requests. <br>
Mitigation: Use a dedicated API key with minimal billing scope when possible, and rotate or revoke it when the skill is no longer needed. <br>


## Reference(s): <br>
- [360 AI Platform](https://ai.360.com/platform/keys) <br>
- [360 AI Translation API Reference](artifact/references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ray771/360-translate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, translated text, output file paths, or temporary result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSLATE_360_API_KEY; document output is PDF; image output may be a saved file or result URL.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
