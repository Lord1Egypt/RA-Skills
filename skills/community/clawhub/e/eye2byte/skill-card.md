## Description: <br>
Give your agent eyes - capture screenshots, voice, and annotations from any screen, monitor, or device via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wolverin0](https://clawhub.ai/user/wolverin0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to give an agent user-directed screen, audio, and recent context capture when visual or spoken context is needed for debugging, UI review, or workflow analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can access sensitive screen content, screen recordings, microphone audio, and recent captured context. <br>
Mitigation: Use it only for explicit user-directed capture, confirm before audio recording, multi-monitor capture, or monitoring over time, and avoid sending captures to external vision models unless the user has configured and approved that use. <br>
Risk: Captured files may contain private information and are stored locally for later retrieval. <br>
Mitigation: Review local retention settings, rely on the default cleanup behavior where appropriate, and delete captured files when they are no longer needed. <br>
Risk: Remote MCP transport uses a bearer token that grants access to capture tools. <br>
Mitigation: Treat the token as a secret, store it only in the intended agent configuration, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wolverin0/eye2byte) <br>
- [Eye2byte homepage](https://github.com/wolverin0/Eye2byte) <br>
- [Eye2byte PyPI package](https://pypi.org/project/eye2byte/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured context summaries and transcriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include screenshot analysis, voice transcription, screen clip summaries, and recent captured context.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
