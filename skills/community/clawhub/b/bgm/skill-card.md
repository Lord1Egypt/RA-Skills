## Description: <br>
Generate original background music for short videos from a natural language description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and content teams use this skill to generate three background-music variations for short videos from a scene, mood, style, and duration description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends video scene, style, mood, and duration descriptions to the third-party SenseAudio API. <br>
Mitigation: Avoid confidential or sensitive prompt details and use only a revocable SenseAudio API key. <br>
Risk: The default workflow creates three generation jobs for each request. <br>
Mitigation: Confirm the user wants three variations before execution when API usage, quota, or cost matters. <br>
Risk: The artifact claims generated music can be used for commercial short-video projects, but server security guidance says to verify licensing before relying on that claim. <br>
Mitigation: Confirm SenseAudio's current licensing and terms before commercial publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scikkk/bgm) <br>
- [SenseAudio homepage](https://senseaudio.cn) <br>
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with generated music version summaries, durations, audio links, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow creates three SenseAudio generation jobs per request and returns selectable audio links when the jobs complete.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
