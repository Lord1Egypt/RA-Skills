## Description:

Provides documentation and patch files for Clawdbot/Moltbot so TTS auto-replies can run for inbound Discord voice memos when block streaming would otherwise suppress the final payload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koto9x](https://clawhub.ai/user/koto9x)

### License/Terms of Use:


## Use Case:

Developers and bot operators maintaining Clawdbot or Moltbot use this skill to review and apply a core patch that restores TTS audio replies for inbound Discord voice memos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overwrites Clawdbot runtime files and may not match the installed Clawdbot version.

Mitigation: Review the replacement files against the local Clawdbot version, apply the patch first in a non-production environment, and keep backups for rollback.

Risk: Verbose TTS debug logging may expose message text, media context, provider state, or API key status in logs.

Mitigation: Remove or gate the TTS debug console logs before real use and restrict access to retained logs.

Risk: Remote TTS providers receive the text being converted to speech.

Mitigation: Use only trusted and secured TTS providers or endpoints, and confirm their data handling is acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/koto9x/skills/discord-voice-memo-upgrade)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Patch details](artifact/PATCH.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and JavaScript patch files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides replacement runtime files and manual application and reversion guidance; it does not execute the patch itself.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
