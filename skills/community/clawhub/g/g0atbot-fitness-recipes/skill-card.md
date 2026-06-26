## Description: <br>
AI tool that creates fitness recipe videos with generated food images, voiceovers, rendered MP4 output, and optional TikTok posting support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G0atfac3](https://clawhub.ai/user/G0atfac3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fitness influencers, nutrition coaches, and health content creators use this skill to generate short-form recipe video assets and batch production workflows for social publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a hard-coded ElevenLabs API key in the artifact. <br>
Mitigation: Remove and rotate the embedded key before use, then configure only user-owned scoped provider keys with spending limits. <br>
Risk: The skill can use paid media-generation and rendering services. <br>
Mitigation: Set provider budgets and review batch counts, quality settings, and automation schedules before running production jobs. <br>
Risk: Optional TikTok/Postiz publishing can make generated content public. <br>
Mitigation: Do not configure posting credentials until the posting path and generated media have been reviewed and approved. <br>
Risk: Prompts, scripts, images, and audio may be sent to third-party services. <br>
Mitigation: Avoid private, sensitive, or regulated content in prompts and media inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/G0atfac3/g0atbot-fitness-recipes) <br>
- [Publisher profile](https://clawhub.ai/user/G0atfac3) <br>
- [fal.ai](https://fal.ai) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [Shotstack](https://shotstack.io) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown documentation, Python scripts, environment variable configuration, and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create image, audio, and MP4 video files through paid third-party services when configured with API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
