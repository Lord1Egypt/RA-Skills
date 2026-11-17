## Description:

ClawBB is a free macOS voice-to-text skill for installing and configuring XiaBB, a Globe-key dictation app powered by Google Gemini.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyz2102](https://clawhub.ai/user/dyz2102)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to install, configure, and operate a macOS voice-to-text app that transcribes speech into the active cursor location for coding and prompt-writing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional build-from-source path runs an unpinned remote install script.

Mitigation: Use the verified DMG path when possible; if building from source, pin and inspect a specific commit before running install commands.

Risk: The app requires Microphone and Accessibility permissions, allowing audio capture and text insertion at the active cursor.

Mitigation: Grant these macOS permissions only after reviewing whether voice capture and cursor-level text insertion are acceptable for the intended environment.

Risk: The downloaded DMG could be tampered with if the checksum is skipped.

Mitigation: Verify the documented SHA-256 checksum before opening the DMG.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dyz2102/skills/clawbb)
- [XiaBB Website](https://xiabb.lol)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
- [XiaBB GitHub Repository](https://github.com/dyz2102/xiabb)
- [XiaBB v1.1.3 Notarized DMG](https://github.com/dyz2102/xiabb/releases/download/v1.1.3/XiaBB-v1.1.3-macOS-arm64.dmg)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Gemini API key and macOS Microphone and Accessibility permissions.]

## Skill Version(s):

1.1.5 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
