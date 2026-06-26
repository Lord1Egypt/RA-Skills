## Description: <br>
Generate AI music with Suno via AceDataCloud API for songs from prompts, generated lyrics, track extension, covers, vocal extraction, voice personas, custom styles, and multi-format output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and music creators use this skill to generate and transform music through AceDataCloud's Suno API, including prompt-based songs, custom lyrics and styles, song extensions, covers, format conversion, and vocal separation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music prompts, lyrics, uploaded audio, voice/persona material, and related metadata may be sent to AceDataCloud/Suno. <br>
Mitigation: Use a scoped, revocable API token and avoid submitting confidential, copyrighted, or sensitive voice/persona material unless the provider's terms and retention controls are acceptable. <br>
Risk: The optional MCP package or hosted endpoint introduces third-party tool-use and token-handling risk. <br>
Mitigation: Verify the MCP package or hosted endpoint before use, keep the API token in an environment variable, and review generated requests before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Germey/acedatacloud-suno-music) <br>
- [AceDataCloud Platform](https://platform.acedata.cloud) <br>
- [AceDataCloud Suno Audio API](https://api.acedata.cloud/suno/audios) <br>
- [AceDataCloud Suno MCP Endpoint](https://suno.mcp.acedata.cloud/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and JSON API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include asynchronous task-polling guidance and generated API request payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
