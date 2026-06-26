## Description: <br>
Converts short drama dialogue into natural, emotional text-to-speech audio suited to scene pacing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghwyever](https://clawhub.ai/user/ghwyever) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and agent workflows use this skill to turn short drama lines, short-video narration, or batch dialogue text into generated voice audio through a configured TTS provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dialogue text is sent to the configured TTS provider. <br>
Mitigation: Use only a trusted API_BASE provider and avoid submitting secrets, private personal data, or sensitive unpublished dialogue unless that provider is acceptable for the use case. <br>
Risk: The skill requires provider credentials to call the TTS API. <br>
Mitigation: Use a limited API key that can be rotated or revoked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ghwyever/06-tts-voice) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON object containing an audio_url string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a provider-generated audio URL; audio bytes are not embedded in the skill output.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
