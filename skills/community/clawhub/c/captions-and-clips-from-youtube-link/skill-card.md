## Description: <br>
Turn YouTube videos into short-form vertical clips with captions and hook titles through the MakeAIClips API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nosselil](https://clawhub.ai/user/nosselil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content-creation teams use this skill to ask an agent to submit YouTube links or uploaded videos to MakeAIClips, monitor processing, present generated clips and hook titles, and download selected MP4 outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube URLs and uploaded videos are sent to MakeAIClips for remote processing. <br>
Mitigation: Use the skill only with media that may be shared with MakeAIClips under the user's privacy, contractual, and authorization requirements. <br>
Risk: The skill requires an API key that can affect account quota or billing. <br>
Mitigation: Keep MAKEAICLIPS_API_KEY secret, avoid printing it in logs, and monitor usage limits before running large batches. <br>
Risk: Generated clips and titles may misrepresent source content if used without review. <br>
Mitigation: Review clip boundaries, captions, and hook titles before publishing or distributing the generated videos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nosselil/captions-and-clips-from-youtube-link) <br>
- [MakeAIClips API documentation](https://makeaiclips.live/docs) <br>
- [MakeAIClips web app](https://makeaiclips.live) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON request examples, curl commands, status summaries, and downloaded MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAKEAICLIPS_API_KEY and remote MakeAIClips processing; generated clips are returned as MP4 downloads.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
