## Description: <br>
Process video/audio files using FFHub.io cloud FFmpeg API. Use when the user wants to convert, compress, trim, resize, extract audio, generate thumbnails, or perform any FFmpeg operation on media files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangbo](https://clawhub.ai/user/gangbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn media-processing requests into FFmpeg commands submitted to FFHub's cloud API for conversion, compression, trimming, resizing, audio extraction, thumbnails, GIFs, and related operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's authentication instructions can expose the FFHUB_API_KEY if the agent prints the environment variable value. <br>
Mitigation: Check that FFHUB_API_KEY is present without echoing or logging the secret, and pass it only through the Authorization header. <br>
Risk: Local media may be uploaded to FFHub and made available through temporary public URLs. <br>
Mitigation: Use the skill only for media that is appropriate to send to FFHub and expose through temporary URLs; avoid sensitive, private, or regulated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gangbo/ffhub-ffmpeg) <br>
- [FFHub](https://ffhub.io) <br>
- [FFHub task API](https://api.ffhub.io/v1/tasks) <br>
- [FFHub upload API](https://files-api.ffhub.io/api/upload/file) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with curl commands, JSON snippets, status updates, result URLs, file details, and error guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FFHUB_API_KEY and may upload local media before submitting FFmpeg tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
