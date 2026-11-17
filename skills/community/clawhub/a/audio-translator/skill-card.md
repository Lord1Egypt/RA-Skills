## Description:

多语种语音翻译技能，支持 URL 或本地音频输入，自动识别源语言、翻译为目标语言，并生成目标语言语音文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[okgptai](https://clawhub.ai/user/okgptai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to transcribe, translate, and synthesize speech from local audio files or audio URLs across supported languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio transcripts and translated text may be sent to external translation or speech services.

Mitigation: Do not use confidential, personal, regulated, or secret-containing audio unless the data-sharing behavior is acceptable for the use case.

Risk: The skill downloads remote audio URLs and performs broad dependency installation and network operations.

Mitigation: Run it in a contained environment, avoid untrusted audio URLs, and install dependencies through a reviewed virtual environment with pinned versions.

Risk: The security evidence flags Python interpolation bugs before attacker-supplied audio or remote translation responses are processed.

Mitigation: Fix the interpolation issues and review input handling before processing untrusted audio or API responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/okgptai/skills/audio-translator)
- [Publisher profile](https://clawhub.ai/user/okgptai)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command usage; generated MP3 audio and TXT translation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python 3.11, FFmpeg, curl, and network access for URL input, translation, and TTS synthesis.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
