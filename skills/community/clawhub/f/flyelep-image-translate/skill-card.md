## Description: <br>
This skill uses the Flyelep AI Tool API to identify and translate text in an image and return a URL for the translated image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyelepai](https://clawhub.ai/user/flyelepai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate text embedded in posters, product images, and other single-image assets by providing an image URL, target language, and Flyelep API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the submitted image URL and runtime API key to Flyelep. <br>
Mitigation: Use it only when Flyelep is trusted for the image content and key handling, avoid confidential images unless Flyelep's privacy and retention terms are acceptable, and provide the secretKey only at runtime. <br>
Risk: Storing the Flyelep secretKey in shared files or prompts could expose the API credential. <br>
Mitigation: Do not hard-code or persist the secretKey; pass it through the request header only for the active call. <br>


## Reference(s): <br>
- [Flyelep Image Translation API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/translate) <br>
- [Flyelep controlboard](https://www.flyelep.cn/controlboard) <br>
- [ClawHub skill page](https://clawhub.ai/flyelepai/flyelep-image-translate) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a translated image URL from the Flyelep API response.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
