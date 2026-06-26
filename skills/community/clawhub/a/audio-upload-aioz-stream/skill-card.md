## Description: <br>
Quick upload audio to AIOZ Stream API. Create audio objects with default or custom encoding configurations, upload the file, complete the upload, then return the audio link to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinhbui3004](https://clawhub.ai/user/vinhbui3004) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create audio objects, upload audio files, complete processing, and retrieve HLS streaming links from AIOZ Stream. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided stream public and secret keys as HTTP headers to the disclosed AIOZ/W3Stream endpoint. <br>
Mitigation: Treat the stream-secret-key as sensitive, use scoped or revocable keys when possible, and avoid exposing secrets in logs or shared transcripts. <br>
Risk: The skill uploads the selected local audio file to an external API. <br>
Mitigation: Confirm the exact file path, destination account, and upload intent before running the upload workflow. <br>


## Reference(s): <br>
- [W3Stream Audio API Reference](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/vinhbui3004/audio-upload-aioz-stream) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON request examples, and returned streaming links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and md5sum; sends user-provided stream public and secret keys to the disclosed AIOZ/W3Stream API endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
