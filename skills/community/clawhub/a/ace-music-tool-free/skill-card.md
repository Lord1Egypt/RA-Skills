## Description:

ACE音乐生成-免费版 helps agents generate short AI songs with vocals, lyrics, instrumental mode, multiple languages, and basic style controls through the ACE Music API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to prompt an agent to generate short AI music demos, background tracks, or instrumental clips through ACE Music API commands. It is intended for ACE music generation workflows, not broad media conversion or unrelated agent automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution while its activation text and stated capabilities are broader than its ACE music generation purpose.

Mitigation: Restrict use to ACE music generation, review proposed commands before execution, and avoid using it for unrelated video, media conversion, generic agent, or file-processing tasks.

Risk: The workflow requires an ACE Music API key.

Mitigation: Provide the API key through a controlled environment variable and do not hard-code or echo credentials in generated commands or output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ace-music-tool-free)
- [ACE Music API key page](https://acemusic.ai/playground/api-key)
- [ACE Music API endpoint](https://api.acemusic.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash command examples and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the external ACE Music API and may produce MP3 outputs; the free-version guidance describes a 60-second single-song limit.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
