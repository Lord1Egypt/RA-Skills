## Description: <br>
Clonev generates cloned-voice speech from a short WAV voice sample and input text using Coqui XTTS v2 across 14+ languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[instant-picture](https://clawhub.ai/user/instant-picture) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and automation agents use Clonev to generate OGG speech files that mimic a provided voice sample for personal messages, notifications, or multilingual text-to-speech workflows where the voice owner has consented. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning can enable impersonation or fraud-sensitive messages. <br>
Mitigation: Use the skill only for your own voice or voices where you have explicit permission, and disclose when audio is synthetic. <br>
Risk: Voice samples and generated audio may remain in the tool's working directory after use. <br>
Mitigation: Manually delete copied samples and generated audio from the working directory when finished. <br>


## Reference(s): <br>
- [CloneV Complete Reference Guide](references/complete-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/instant-picture/clonev) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [OGG audio file path returned as a shell string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires text, a WAV voice sample, and a language code; generates a single OGG audio file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
