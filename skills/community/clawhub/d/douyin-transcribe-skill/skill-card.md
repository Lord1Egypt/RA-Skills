## Description:

Automatically transcribes Douyin links or local video files and helps an agent summarize, provide transcripts, archive notes, or support discussion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junweiren98-rgb](https://clawhub.ai/user/junweiren98-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Douyin videos or local video files into usable text, summaries, discussion analysis, and saved knowledge notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command execution can be abused with crafted URLs or filenames.

Mitigation: Run only after command execution is changed to non-shell argument arrays and URL or file inputs are strictly validated.

Risk: API keys may be exposed if users paste secrets into chat or store them casually.

Mitigation: Configure secrets out of band, avoid sharing keys in chat, and rotate any key that may already have been exposed.

Risk: Links and filenames are untrusted inputs.

Mitigation: Treat all user-provided links and paths as untrusted and avoid running the skill on crafted input until validation is hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junweiren98-rgb/skills/douyin-transcribe-skill)
- [OpenClaw](https://openclaw.ai)
- [Groq](https://groq.com)
- [FFmpeg](https://ffmpeg.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses and saved Markdown transcript or archive files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save transcripts under douyin-transcripts and archived notes under douyin-knowledge when requested.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
