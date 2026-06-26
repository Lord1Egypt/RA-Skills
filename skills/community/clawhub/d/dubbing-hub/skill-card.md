## Description: <br>
DubbingHub translates user-provided videos or video URLs through an external video translation service and returns a preview URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[papawaigo](https://clawhub.ai/user/papawaigo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit a video file or URL, choose a supported target language, and retrieve the translated video's preview URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Videos or video URLs may be sent to a third-party processing service without clear disclosure or confirmation. <br>
Mitigation: Before submitting a job, explicitly confirm the video source, target language, and external upload, and use only videos suitable for third-party processing. <br>
Risk: The skill requires a service credential for VIDEO_TRANSLATE_SERVICE_API_KEY. <br>
Mitigation: Provide the credential through the configured environment variable and avoid exposing it in prompts, logs, command history, or shared outputs. <br>


## Reference(s): <br>
- [API Contract](references/api-contract.md) <br>
- [DubbingHub ClawHub listing](https://clawhub.ai/papawaigo/dubbing-hub) <br>
- [Luoji video translation service](https://audiox-api-global.luoji.cn) <br>
- [Luoji support and privacy site](https://luoji.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text or Markdown guidance with optional shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns job status, preview_url on success, or API error text on failure; requires VIDEO_TRANSLATE_SERVICE_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
