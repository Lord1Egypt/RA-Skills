## Description: <br>
Auto-speak every message using edge-tts, converting responses to speech asynchronously in the background after installing the package if needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StefanoChiodino](https://clawhub.ai/user/StefanoChiodino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to have assistant responses spoken aloud through Microsoft Edge TTS while the text conversation continues. It supports automatic speech for every reply and manual speech commands for specific text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assistant replies may be sent to Microsoft Edge TTS for speech generation. <br>
Mitigation: Use only when users intentionally want spoken replies and are comfortable with generated text being processed by that external TTS service. <br>
Risk: The skill encourages automatic speech for every assistant message without clear consent or control. <br>
Mitigation: Add an explicit off switch or confirmation step before enabling the mandatory SOUL.md rule, especially in shared or sensitive environments. <br>
Risk: The evidence guidance notes that the auto-speak wrapper should be verified before relying on the package. <br>
Mitigation: Confirm the wrapper exists and behaves as expected before deployment, and test with non-sensitive sample text first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/StefanoChiodino/auto-talk-tts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger background text-to-speech playback through node-edge-tts and local audio playback when the described wrapper is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
