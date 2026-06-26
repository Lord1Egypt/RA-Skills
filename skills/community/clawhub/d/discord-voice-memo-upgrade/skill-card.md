## Description: <br>
Provides documentation and patch files for Clawdbot/Moltbot to make TTS auto-replies work for inbound Discord voice memos when block streaming is enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koto9x](https://clawhub.ai/user/koto9x) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and bot operators use this skill when Clawdbot or Moltbot text-to-speech works for text messages but does not trigger for inbound voice memos. It provides patch files, manual installation steps, testing guidance, and rollback instructions for the TTS auto-reply path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The patch overwrites core Clawdbot distribution files, which can break bot behavior or be lost on upgrades. <br>
Mitigation: Review the patch against the exact Clawdbot version, back up original files, test in a non-production bot first, and keep the documented rollback path ready. <br>
Risk: Verbose TTS debug logging can expose message text and fragments of credential state in logs. <br>
Mitigation: Remove or gate all TTS debug console logs before use with real users and restrict log access during testing. <br>
Risk: Remote TTS providers may receive sensitive conversation text. <br>
Mitigation: Use remote TTS only when sending the generated text to the configured provider is acceptable for the conversation context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/koto9x/discord-voice-memo-upgrade) <br>
- [README.md](artifact/README.md) <br>
- [PATCH.md](artifact/PATCH.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [Publisher profile](https://clawhub.ai/user/koto9x) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with JavaScript patch files, JSON configuration snippets, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes manual patch and rollback steps; patch files overwrite Clawdbot core distribution files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, CHANGELOG, plugin metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
