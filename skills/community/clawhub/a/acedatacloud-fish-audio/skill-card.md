## Description: <br>
Generate AI audio and synthesize voices with Fish Audio via the AceDataCloud API for text-to-speech, voice synthesis, and audio content generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to call AceDataCloud's Fish Audio API for text-to-speech, custom voice synthesis, voice cloning, and task polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning may be used without authorization from the speaker. <br>
Mitigation: Clone voices only with clear permission from the speaker and in compliance with applicable laws. <br>
Risk: The skill sends text and reference-audio URLs to AceDataCloud and uses an API token. <br>
Mitigation: Use scoped or revocable credentials, monitor usage costs, and share only data appropriate for that provider. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Germey/acedatacloud-fish-audio) <br>
- [AceDataCloud Fish Audio API endpoint](https://api.acedata.cloud/fish/audios) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACEDATACLOUD_API_TOKEN; generated audio is delivered by the external Fish Audio/AceDataCloud API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
