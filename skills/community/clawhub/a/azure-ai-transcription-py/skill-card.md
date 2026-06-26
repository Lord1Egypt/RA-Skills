## Description: <br>
Azure AI Transcription SDK for Python for real-time and batch speech-to-text transcription with timestamps and diarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install and configure the Azure AI transcription Python package, authenticate with an Azure subscription key, and use batch or real-time speech-to-text workflows with timestamps and speaker diarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure subscription keys could be exposed in shared logs, files, or prompts during setup. <br>
Mitigation: Keep the transcription key in environment variables or a secret manager and avoid pasting it into shared transcripts or generated files. <br>
Risk: Audio may contain sensitive or unauthorized content before it is sent to Azure for transcription. <br>
Mitigation: Only transcribe audio that the user is authorized to process and review data handling requirements before sending audio to Azure. <br>
Risk: The referenced Python package source is not independently verified by the skill card evidence. <br>
Mitigation: Verify the package source before installation and pin trusted package versions for production use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment variable names, authentication setup, and usage examples for batch and streaming transcription.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
