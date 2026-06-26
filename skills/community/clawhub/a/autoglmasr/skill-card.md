## Description: <br>
AutoGLM ASR MCP provides long-audio transcription with concurrent chunk processing, context modes, and timestamped segments using Zhipu GLM-ASR-2512. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsabellaZhangYM](https://clawhub.ai/user/IsabellaZhangYM) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users configure this MCP server to transcribe long audio files, inspect audio metadata, and return transcript text, timestamped segments, and run statistics to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to Zhipu/BigModel for cloud transcription. <br>
Mitigation: Use only approved audio, review provider terms, and avoid submitting sensitive or regulated recordings without organizational approval. <br>
Risk: The MCP server requires an API key and is commonly launched through npx. <br>
Mitigation: Use a dedicated API key, pin a known package version where possible, and review the npm package and linked source before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IsabellaZhangYM/autoglmasr) <br>
- [Zhipu GLM-ASR-2512 documentation](https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-asr-2512) <br>
- [Model Context Protocol specification](https://modelcontextprotocol.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples; MCP tool responses include transcript text, timestamped segments, and run statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and AUTOGLM_ASR_API_KEY; supports context mode, max concurrency, and audio chunking settings.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
