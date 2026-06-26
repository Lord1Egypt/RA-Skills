## Description: <br>
Uses Agnes AI models to generate and edit images with Agnes-Image-2.0-Flash and generate videos with Agnes-Video-V2.0, including text-to-image, image-to-image, text-to-video, image-to-video, and multi-image composition workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jefsky](https://clawhub.ai/user/jefsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Agnes AI image and video generation endpoints, prepare request parameters, poll asynchronous video jobs, and optionally save returned media locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, referenced image URLs, and account-linked API usage are sent to Agnes AI. <br>
Mitigation: Avoid sensitive prompts or private images unless they are intended to be shared with the provider, and review Agnes account and API usage controls before use. <br>
Risk: The helper script requires an Agnes API key. <br>
Mitigation: Provide the key through the AGNES_API_KEY environment variable or an approved secret store, and do not hard-code it in skill files, prompts, or shared logs. <br>
Risk: The helper script downloads provider-returned media URLs and saves generated files locally. <br>
Mitigation: Run the script in an appropriate workspace, inspect saved outputs before reuse, and apply normal controls for files downloaded from external URLs. <br>


## Reference(s): <br>
- [Agnes API Platform](https://platform.agnes-ai.com/) <br>
- [Agnes API Base URL](https://apihub.agnes-ai.com/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/jefsky/agnes-image-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request payloads, local file paths for downloaded media, and generated media URLs returned by Agnes AI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
