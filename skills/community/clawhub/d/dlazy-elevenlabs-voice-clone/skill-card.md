## Description: <br>
ElevenLabs Instant Voice Cloning (IVC). Upload a clean voice sample to clone a custom voice usable with ElevenLabs TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to invoke dLazy's ElevenLabs voice-cloning CLI workflow, upload an authorized voice sample, and create a custom voice for ElevenLabs text-to-speech use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice samples and request parameters may be uploaded to dLazy or ElevenLabs-related services. <br>
Mitigation: Use only audio the user owns or is authorized to process, and avoid submitting sensitive or private voice samples without appropriate consent. <br>
Risk: A dLazy API key may be stored locally for CLI authentication. <br>
Mitigation: Store credentials with OS-user-only permissions, prefer per-invocation environment variables when appropriate, and rotate or revoke keys when access changes. <br>
Risk: The skill installs @dlazy/cli@latest, which may change behavior over time. <br>
Mitigation: Review the package or source before installation and verify current CLI help before relying on examples. <br>
Risk: Voice cloning can be used for deceptive impersonation. <br>
Mitigation: Use the skill only for authorized voice cloning and disclose synthetic voice use where required by policy or law. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dlazyai/dlazy-elevenlabs-voice-clone) <br>
- [dLazy CLI Source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm Package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy Homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return asynchronous task identifiers and hosted output URLs from the dLazy service.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
