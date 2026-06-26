## Description: <br>
AI Face Swap - Swap face in video using verging.ai API. Supports local video files, YouTube/Bilibili URLs, local and remote face images. Auto-download, trimming, real-time progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alouhaou](https://clawhub.ai/user/alouhaou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare local or URL-based video and face image inputs, call the verging.ai face-swap API, monitor job progress, and optionally download the generated result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos, face images, and fetched remote URLs are sent to verging.ai for processing. <br>
Mitigation: Use only authorized, non-sensitive media and review remote URLs before running the skill. <br>
Risk: The skill requires a sensitive VERGING_API_KEY credential. <br>
Mitigation: Use a dedicated API key, pass it through the environment, and avoid exposing it in prompts, logs, or repositories. <br>
Risk: Temporary media files may remain under /tmp/verging-faceswap/ after use. <br>
Mitigation: Clean up the temporary directory after each run, especially on shared systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alouhaou/face-swap) <br>
- [verging.ai Website](https://verging.ai) <br>
- [verging.ai API Docs](https://verging.ai/docs/api) <br>
- [Face Swap Demo Video](https://youtu.be/xvlZe4uqvY4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VERGING_API_KEY plus yt-dlp, ffmpeg, ffprobe, and curl; may create temporary media under /tmp/verging-faceswap/ and optionally download result files.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
