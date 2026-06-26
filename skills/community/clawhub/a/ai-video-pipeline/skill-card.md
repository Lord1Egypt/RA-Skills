## Description: <br>
Ai Video Pipeline is a conversational AI short-video creation skill that guides a user from an idea through script design, human confirmation, and automated MP4 production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mydearzsy](https://clawhub.ai/user/mydearzsy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and agents use this skill to turn a short-video idea or manuscript into a confirmed script and a generated MP4 with narration, subtitles, BGM, and optional AI video clips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scripts, prompts, generated audio/video, and API-authenticated requests are sent to named third-party AI services. <br>
Mitigation: Use only non-sensitive content unless the providers' data-handling terms are acceptable, and configure API credentials with least privilege and cost controls. <br>
Risk: The default work directory can reuse prior cached media without confirming it matches the current script. <br>
Mitigation: Use a fresh work directory per job or clear /tmp/video-poc before running a new production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mydearzsy/ai-video-pipeline) <br>
- [Volcengine visual intelligence documentation](https://www.volcengine.com/docs/85621) <br>
- [MiniMax music generation API](https://api.minimaxi.com/v1/music_generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown production plans, bash commands, Python configuration guidance, and generated MP4/audio/subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before production; generated media may depend on third-party API credentials and cached work-directory files.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
