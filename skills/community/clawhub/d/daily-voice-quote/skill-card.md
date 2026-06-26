## Description: <br>
Creates a daily voice quote with generated audio, a cover-image static video, and an optional HeyGen avatar video for delivery to a recipient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation builders use this skill to prepare and send a daily motivational quote as cloned-voice audio, a static video, and optionally an avatar video. It is intended for scheduled personal or audience-facing messaging workflows where the voice and face subject has approved the media use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning and avatar generation can misuse a person's voice or likeness. <br>
Mitigation: Use the skill only after the voice and face subject has explicitly approved cloning, avatar training, hosting, and automated delivery. <br>
Risk: Public media URLs can expose generated audio or video beyond the intended recipient. <br>
Mitigation: Prefer short-lived or access-controlled URLs, and verify recipient IDs before automated messaging. <br>
Risk: API tokens for ElevenLabs, HeyGen, messaging, hosting, or image generation can grant access to paid services or private media. <br>
Mitigation: Use dedicated keys with the narrowest available access, keep them in environment configuration, and rotate them if exposed. <br>
Risk: Media providers and hosting services may retain uploaded samples, generated media, or delivery metadata. <br>
Mitigation: Confirm provider storage and deletion behavior before uploading voice samples, face media, or generated assets. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/daaab/daily-voice-quote) <br>
- [Publisher profile](https://clawhub.ai/user/daaab) <br>
- [Holiday reference list](references/holidays.md) <br>
- [Quote reference list](references/quotes.md) <br>
- [ElevenLabs voice API example](https://api.elevenlabs.io/v1/voices/add) <br>
- [HeyGen](https://www.heygen.com/?sid=rewardful&via=clawhub) <br>
- [LINE Messaging API push endpoint](https://api.line.me/v2/bot/message/push) <br>
- [Google AI Studio](https://aistudio.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated media workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and commands for audio, image, video, subtitle, scheduling, and message-delivery workflows; generated media files and API calls are created by the agent environment.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
