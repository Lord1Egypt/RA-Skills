## Description: <br>
Generate images, videos, and process media using the GenVR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genvrlabs](https://clawhub.ai/user/genvrlabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to list GenVR models, start media-generation jobs, check task status, and download generated outputs from the GenVR API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, and task details are sent to GenVR. <br>
Mitigation: Avoid submitting private or regulated prompts or media unless GenVR handling is acceptable for the intended use case. <br>
Risk: The skill requires sensitive GenVR credentials. <br>
Mitigation: Use a dedicated GenVR API key and provide credentials through GENVR_API_KEY and GENVR_UID. <br>
Risk: The CLI automatically loads a local .env file from the current working directory. <br>
Mitigation: Check the local .env before running so unintended credentials or identifiers are not used. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/genvrlabs/genvr-skills) <br>
- [GenVR API](https://api.genvrresearch.com) <br>
- [GenVR API Credentials](https://api.genvrresearch.com/obtain-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance, files] <br>
**Output Format:** [CLI text and JSON responses, with downloaded generated media files when tasks complete] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GENVR_API_KEY and GENVR_UID; generation jobs may poll asynchronously unless --no-wait is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
