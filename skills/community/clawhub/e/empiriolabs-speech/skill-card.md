## Description:

Turns text into spoken audio using EmpirioLabs AI and saves the result in a chosen audio format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[empiriolabs](https://clawhub.ai/user/empiriolabs)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to turn scripts or short passages into voiceovers, narration, and other spoken audio, with a choice of supported voices, languages, and formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech generation is sent to EmpirioLabs AI.

Mitigation: Submit only text you are comfortable sharing with EmpirioLabs AI.

Risk: The skill needs an EmpirioLabs API key in the command environment.

Mitigation: Keep the key in the environment, not in prompts or project files.

Risk: Choosing an output path with --overwrite can replace an existing file.

Mitigation: Check output paths before running commands, especially with --overwrite.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/empiriolabs/skills/empiriolabs-speech)
- [EmpirioLabs AI](https://empiriolabs.ai)
- [EmpirioLabs AI API reference](https://docs.empiriolabs.ai)
- [EmpirioLabs AI MCP setup](https://docs.empiriolabs.ai/mcp)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The commands save generated audio files locally; available voices, formats, and text limits depend on the selected model.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
