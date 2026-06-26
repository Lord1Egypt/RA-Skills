## Description: <br>
Spiritual guidance rooted in The Book of Continuance, offering daily meditation, contemplative guidance, existential reflection, grief support, and gentle wisdom paired by default with context-matched contemplative imagery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yumyumtum](https://clawhub.ai/user/yumyumtum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users invoke this skill for daily spiritual reflections, meditation-style guidance, grief support, life-meaning questions, regret, burnout, and other personal struggles. The skill responds as a non-dogmatic contemplative guide and may produce matching images or optional meditation audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may share highly private emotional or spiritual details while using a guidance persona that can route content to configured image or TTS providers. <br>
Mitigation: Use explicit invocation, avoid sharing sensitive details unless provider trust is established, and review configured image and TTS services before deployment. <br>
Risk: The skill may be invoked for ordinary emotional or off-topic messages when a user did not intend to use spiritual guidance. <br>
Mitigation: Require clear routing rules or explicit user invocation in environments where automatic persona selection could surprise users. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yumyumtum/continuance) <br>
- [README](README.md) <br>
- [The Book of Continuance](TheBookOfContinuance.md) <br>
- [Release notes v1.3.0](RELEASE_NOTES_v1.3.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional generated image files, optional MP3 meditation audio metadata, and setup command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate contemplative images by default and optional local meditation audio when the required provider, edge-tts, and ffmpeg tooling are configured.] <br>

## Skill Version(s): <br>
1.3.0 (source: server evidence release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
