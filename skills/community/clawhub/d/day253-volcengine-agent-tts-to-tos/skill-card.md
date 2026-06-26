## Description: <br>
Combined agent that synthesizes speech via Volcengine TTS, uploads the audio to TOS, and returns a presigned temporary URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[day253](https://clawhub.ai/user/day253) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to convert text into speech, upload the generated audio to Volcengine TOS, and return a temporary shareable URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is sent to Volcengine TTS and generated audio is stored in TOS. <br>
Mitigation: Avoid secrets or regulated personal data unless the deployment is approved for that data. <br>
Risk: Broad storage credentials or long-lived presigned URLs can expose generated audio more widely than intended. <br>
Mitigation: Use least-privilege credentials limited to the intended bucket and keep URL expiry short. <br>
Risk: Using --keep-local retains a local copy of the generated audio. <br>
Mitigation: Use --keep-local only when a local audio copy is intentionally needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/day253/day253-volcengine-agent-tts-to-tos) <br>
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/196768) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local audio path when requested, a TOS object path, and a presigned temporary URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
