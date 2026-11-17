## Description: <br>
Provides basic Azure VoiceLive SDK guidance for real-time voice conversations using WebSocket streaming, API key authentication, PCM16 audio input and output, and transcript handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prototype Azure VoiceLive voice assistants, stream microphone audio, receive PCM audio responses, and inspect transcripts from real-time sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad read, write, and command execution authority beyond the narrow Azure VoiceLive workflow. <br>
Mitigation: Install and run it only in constrained agent environments where file and command access can be limited to the documented SDK workflow. <br>
Risk: Audio and transcript content may be sent to Azure services during use. <br>
Mitigation: Use it only for explicit Azure VoiceLive audio or transcription tasks, and make sure users understand where audio and transcript data is processed. <br>
Risk: API keys can be exposed if copied into code, logs, or version control. <br>
Mitigation: Store Azure credentials in environment variables or a managed secret store, rotate them when needed, and avoid echoing them in command output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-ai-voicelive-py-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment-variable setup guidance and example JSON-shaped results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
