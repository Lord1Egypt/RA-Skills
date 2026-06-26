## Description: <br>
Generate digital human talking avatar videos from images and audio using DreamAvatar 3.0 Fast API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hy-1990](https://clawhub.ai/user/Hy-1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create talking-avatar videos from a face image, audio clip, prompt, and selected resolution through the DreamAvatar/NewportAI API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, photos, voices, or audio clips are sent to an external DreamAvatar/NewportAI workflow. <br>
Mitigation: Use only media that is approved for the external service and avoid sensitive content unless the user accepts the service's data handling. <br>
Risk: The skill requires a DreamAPI key that could be misused if exposed. <br>
Mitigation: Store DREAM_API_KEY in the agent configuration, avoid sharing it in prompts or logs, and revoke or rotate the key when it is no longer needed. <br>
Risk: Local files may be uploaded and exposed through temporary externally reachable URLs. <br>
Mitigation: Use only files suitable for temporary external hosting and avoid private or regulated media unless that exposure is acceptable. <br>


## Reference(s): <br>
- [Dream Avatar on ClawHub](https://clawhub.ai/Hy-1990/dream-avatar) <br>
- [NewportAI API Getting Started](https://api.newportai.com/api-reference/get-started) <br>
- [Dreamface AI Tools](https://tools.dreamfaceapp.com/home) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown instructions with bash and JSON snippets; generated runs return an MP4 video URL when the external API task completes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAM_API_KEY. Inputs can be local image and audio files or public URLs; audio is limited to 3 minutes, API work is asynchronous, and uploaded file URLs are described as valid for 1 day.] <br>

## Skill Version(s): <br>
1.2.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
