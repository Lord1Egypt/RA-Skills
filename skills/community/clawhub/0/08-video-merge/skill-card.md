## Description: <br>
Merges video, audio, and optional subtitles into a 9:16 vertical short video ready for publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghwyever](https://clawhub.ai/user/ghwyever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video automation users use this skill to combine final video, dubbing audio, and optional subtitle assets into a publishable vertical short video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns a local output filename, so downstream agents may assume a hosted URL exists when it does not. <br>
Mitigation: Confirm the returned final_video_url is accessible in the current execution environment before publishing or passing it to another workflow. <br>
Risk: The security summary identifies powerful automation context around review, moderation, and deployment-adjacent workflows. <br>
Mitigation: Review the skill and its surrounding workflow before use in environments that affect public releases, user-facing content, or deployment processes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ghwyever/08-video-merge) <br>


## Skill Output: <br>
**Output Type(s):** [text, file reference] <br>
**Output Format:** [JSON object containing final_video_url and a completion message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a local merged video filename rather than uploading or hosting the result.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
