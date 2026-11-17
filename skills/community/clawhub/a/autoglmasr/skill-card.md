## Description:

AutoGLM ASR MCP transcribes long audio with concurrent chunking, configurable context modes, timestamped segments, and GLM-ASR-2512.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isabellazhangym](https://clawhub.ai/user/isabellazhangym)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to configure an MCP-based transcription service for long audio files, including chunking, concurrency controls, context-mode selection, and timestamped transcript output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server is installed through an unpinned npm command.

Mitigation: Pin autoglm-asr-mcp to a reviewed exact version before installation or deployment.

Risk: Local audio is sent to the external Zhipu/BigModel ASR service for transcription.

Mitigation: Use a dedicated API key and transcribe only audio that is approved for transfer to that external service.

Risk: Running the MCP server may expand the local agent's access to audio files and environment variables.

Mitigation: Run the server in a restricted environment with least-privilege file access and scoped credentials.

## Reference(s):

- [GLM-ASR-2512 documentation](https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-asr-2512)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [ClawHub skill page](https://clawhub.ai/isabellazhangym/skills/autoglmasr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described MCP tool returns full transcript text, timestamped segments, and run statistics.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
