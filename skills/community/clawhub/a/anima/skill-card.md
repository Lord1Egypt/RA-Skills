## Description: <br>
Anima generates 16:9 avatar videos with dynamic character sprites, Fish Audio speech, text overlays, and optional Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HMyaoyuan](https://clawhub.ai/user/HMyaoyuan) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and content creators use Anima to generate short avatar-led videos from scripted scenes, matching text to emotion-tagged sprites and synthesized speech. Agents can run it in preview mode for local video generation or provide Feishu credentials to upload and send the finished video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports suspicious command execution paths where user-controlled script text, recipient IDs, and file paths can reach shell commands. <br>
Mitigation: Use preview mode for sensitive content, avoid untrusted script text, recipient IDs, and file paths, and replace shell-string execution with argument-array process calls or direct HTTP-client calls before broad deployment. <br>
Risk: Feishu delivery uses supplied credentials and recipient identifiers to upload and send generated videos. <br>
Mitigation: Provide Feishu credentials only when upload and delivery are intended, scope credentials narrowly, and validate recipient IDs before sending. <br>
Risk: The published package does not include sprite PNG assets, so video frames may fall back to a blank white background until assets are prepared. <br>
Mitigation: Generate or install the expected sprite assets, verify the production plan and manifest, and run preview mode before sending videos externally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HMyaoyuan/anima) <br>
- [SKILL.md](SKILL.md) <br>
- [ASSETS_PLAN.md](ASSETS_PLAN.md) <br>
- [Sprite manifest](assets/manifest.json) <br>
- [Fish Audio API dashboard](https://fish.audio/dashboard/api) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown instructions with JSON scene scripts and generated MP4, PNG, WAV, and CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg, Node dependencies, Fish Audio credentials for speech, optional Gemini credentials for sprite generation, and optional Feishu credentials for delivery.] <br>

## Skill Version(s): <br>
3.3.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
