## Description:

Azure Ai Voicelive P provides Markdown guidance and examples for using Azure VoiceLive with bidirectional audio/text streaming, transcription, microphone input, credentials, session configuration, audio streaming, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as reference material for building Azure VoiceLive applications that stream audio and text, configure authentication, manage sessions, handle events, and troubleshoot common errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executed examples may connect to Azure VoiceLive and handle privacy-sensitive microphone audio, uploaded audio, transcripts, or function-call data.

Mitigation: Confirm the Azure account and endpoint, obtain clear user consent before capture or upload, and review function-call integrations before running examples.

Risk: Credential examples can lead to exposed or hard-coded API keys if copied without adjustment.

Mitigation: Use environment variables or DefaultAzureCredential, avoid committing secrets, and rotate any key that may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-voicelive-2)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; examples may require Azure credentials, network access, microphone access, and user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
