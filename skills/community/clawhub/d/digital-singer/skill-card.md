## Description:

Digital Singer helps users run a NuwaAI avatar karaoke experience that lip-syncs avatar singing to vocal audio, plays accompaniment, supports duet battles, and returns playful scores and rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianglingling007](https://clawhub.ai/user/jianglingling007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up and run a browser-based NuwaAI digital avatar singer for karaoke-style duet battles with prepared song audio, microphone input, and an OpenAI-compatible LLM host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and local control endpoints may be exposed by the local server.

Mitigation: Review the server before installing, rotate or remove bundled API keys, protect or remove token and configuration endpoints, and store NuwaAI credentials outside web-served paths.

Risk: Audio conversion and song-file handling may allow unsafe local execution or file use.

Mitigation: Replace shell-form FFmpeg execution with argument-based execution and restrict conversion to an explicit allowlist of prepared song files.

Risk: Microphone audio and chat text are sent to external providers.

Mitigation: Inform users before use and only run the skill when sending microphone audio to NuwaAI and chat text to the configured LLM provider is acceptable.

## Reference(s):

- [Digital Singer ClawHub release page](https://clawhub.ai/jianglingling007/skills/digital-singer)
- [NuwaAI](https://nuwaai.com)
- [DashScope OpenAI-compatible chat completions endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operation guidance for a local browser-based singing avatar workflow.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
