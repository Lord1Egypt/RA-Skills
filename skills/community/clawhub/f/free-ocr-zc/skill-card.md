## Description: <br>
Extracts text from images through OpenRouter using the Baidu Qianfan OCR model, with support for image URLs, local files, and custom OCR prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run OCR on selected images and receive extracted text, optionally with an image description for additional context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, prompts, and image URLs are sent to OpenRouter or the configured OCR API endpoint. <br>
Mitigation: Use the skill only with data approved for third-party processing; avoid confidential documents, IDs, internal screenshots, internal URLs, and regulated data unless that processing is acceptable. <br>
Risk: The skill requires an OpenRouter API key read from a documented local secrets path or environment variable. <br>
Mitigation: Use a scoped API key you control, keep it out of version control, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/free-ocr-zc) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Console text with OCR results and optional image description] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenRouter API key and sends selected image content or image URLs to the configured OCR endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
