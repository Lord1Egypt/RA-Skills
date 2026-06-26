## Description: <br>
Sends a user-provided image to Synerunify's appearance prediction API and reports face appearance scores, including multiple faces sorted left to right. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiushosens](https://clawhub.ai/user/qiushosens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user asks in English or Chinese for face appearance or attractiveness scores from an image. It guides the agent to upload the image, parse the JSON response, and surface scores or API errors clearly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided photos, including face images, are sent to Synerunify for processing. <br>
Mitigation: Use only images the user has permission to submit and avoid sensitive photos unless the user accepts the service privacy and retention uncertainty. <br>
Risk: The skill depends on an external API response and may receive failures or incomplete face data. <br>
Mitigation: Surface the HTTP status and response message first, and treat empty or missing face results as an API outcome rather than inventing scores. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qiushosens/appearance-score) <br>
- [Synerunify appearance predict API](https://synerunify.com/api/process/appearance/predict) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON response fields, curl and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses multipart/form-data image uploads, reports HTTP or API errors first, and sorts multi-face scores left to right.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
