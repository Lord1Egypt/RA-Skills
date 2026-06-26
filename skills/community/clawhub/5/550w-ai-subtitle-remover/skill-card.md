## Description: <br>
Uploads a local video or accepts a video URL, calls the 550W AI subtitle-removal API, and returns a processed video link for hard subtitles, watermarks, station bugs, or logos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunshinehu](https://clawhub.ai/user/sunshinehu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to submit authorized MP4 or MOV videos to 550W AI for subtitle, watermark, station bug, or logo removal, then retrieve task status and the processed video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends video files or video URLs to the 550W AI service for processing. <br>
Mitigation: Use only videos you are authorized to upload or submit, and avoid sensitive or regulated media unless 550W's data handling terms meet your requirements. <br>
Risk: The skill requires a user number and API key for the 550W AI service. <br>
Mitigation: Store credentials in SUBTITLE_REMOVER_USER_NO and SUBTITLE_REMOVER_API_KEY environment variables, and avoid exposing them in prompts, logs, or shared files. <br>
Risk: Video processing can consume account credits, and repeated submissions of the same video URL are treated as separate tasks. <br>
Mitigation: Check account credits or estimate cost before submitting work, and avoid duplicate submissions unless separate processing is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunshinehu/550w-ai-subtitle-remover) <br>
- [550W AI service site](https://www.550wai.cn) <br>
- [550W credential application](https://qzm.550wai.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or JSON action responses containing task status, errors, credit estimates, and processed video URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include resultUrl, taskId, failReason, timedOut, credit balance, or credit estimates; the workflow may poll for up to 10 minutes before returning a taskId for later follow-up.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
