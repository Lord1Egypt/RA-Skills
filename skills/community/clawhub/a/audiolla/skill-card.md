## Description: <br>
Connects to a user-deployed audiolla server to perform audio processing, analysis, generation, metadata, MIDI, visualization, and workflow operations through REST or MCP calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyb0t](https://clawhub.ai/user/psyb0t) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and audio engineers use this skill when a user has named audiolla and provided access to a running audiolla server. It helps stage audio files, call server endpoints for stem separation, mastering, MIR analysis, DSP transforms, restoration, MIDI operations, visualization, and generation, and interpret the JSON responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An exposed audiolla server without authentication can let reachable users run resource-intensive audio processing and upload files to the staging area. <br>
Mitigation: Keep the server bound to localhost or protect it with a strong AUDIOLLA_AUTH_TOKEN before exposing it beyond the local machine. <br>
Risk: Remote file_url and output_url support can create URL-fetch and upload risk when enabled broadly. <br>
Mitigation: Leave AUDIOLLA_FETCH_MODE disabled unless needed; when enabling it, prefer allowlist mode with tightly scoped hosts and schemes. <br>
Risk: Staged audio files, generated outputs, and downloaded models can persist in the configured data volume. <br>
Mitigation: Operate only trusted servers, manage the AUDIOLLA_DATA_DIR volume intentionally, and remove staged sensitive audio when it is no longer needed. <br>


## Reference(s): <br>
- [audiolla setup](artifact/references/setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/psyb0t/audiolla) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-provided AUDIOLLA_URL and optional AUDIOLLA_TOKEN; audio-producing operations return JSON that points to staged paths or configured output URLs.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
