## Description: <br>
Guides agents through using the Azure AI Transcription Python client to submit batch speech-to-text jobs for Blob or SAS audio URLs, set the recognition locale, and retrieve transcription results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure Azure transcription credentials, submit batch transcription jobs for HTTPS-accessible audio, and turn completed results into transcript text or related summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure subscription keys, SAS tokens, audio URLs, and generated transcripts may expose sensitive access or content if mishandled. <br>
Mitigation: Store credentials in environment variables or a secrets manager, avoid logging tokens or transcripts, rotate exposed keys, and share audio URLs only with the minimum required access and lifetime. <br>
Risk: Audio is processed by Azure cloud transcription services, which may be inappropriate for private or regulated recordings without authorization. <br>
Mitigation: Confirm the user has rights to submit the recordings and understands applicable Azure retention, access control, and data handling requirements before transcription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-ai-transcription-py-free) <br>
- [Release artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets plus JSON result examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Azure environment variable names, batch transcription job examples, status handling notes, and transcript extraction guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
