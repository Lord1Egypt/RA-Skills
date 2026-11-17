## Description:

Generate speech audio with 阿里云百炼 TTS via the `bailian-cli` npm package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackerpl](https://clawhub.ai/user/hackerpl)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert text into speech audio, select supported voices and languages, batch-generate narration, and troubleshoot Bailian TTS setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The smoke test can automatically install an unpinned global npm package.

Mitigation: Review the npm dependency before running the smoke test, and prefer installing a pinned, reviewed version locally or in an isolated environment.

Risk: Speech synthesis sends the API key and requested text to Aliyun Bailian.

Mitigation: Only provide BAILIAN_API_KEY and text that are appropriate to send to Aliyun Bailian for speech synthesis.

## Reference(s):

- [Voices and Languages](references/voices-and-languages.md)
- [阿里云百炼 Console](https://bailian.console.aliyun.com/)
- [ClawHub Skill Page](https://clawhub.ai/hackerpl/skills/bailian-tts)
- [Publisher Profile](https://clawhub.ai/user/hackerpl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and output paths or base64 data when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local audio file paths, URL-style output, or base64 audio data through the Bailian CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
