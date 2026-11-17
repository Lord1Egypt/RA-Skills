## Description: <br>
Azure Transcription helps agents guide enterprise speech transcription workflows with Azure Speech/Cognitive Services, including real-time transcription, speaker diarization, batch queues, custom models, and transcript export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and business users use this skill to configure Azure-backed transcription workflows for meetings, customer calls, and subtitle generation. It provides guidance, code examples, shell commands, and configuration steps for handling streaming transcription, batch transcription, diarization, and transcript exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files, storage URLs, and transcript content may be sent to Azure Speech/Cognitive Services and can contain sensitive conversations. <br>
Mitigation: Use the skill only when Azure processing fits the organization's data handling rules, and send only approved audio or storage URLs. <br>
Risk: Azure credentials and generated transcripts may be exposed if stored or shared carelessly. <br>
Mitigation: Use restricted Azure keys, keep credentials in environment variables, avoid committing secrets, and write transcripts only to approved local or encrypted storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-transcription) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, shell, JSON, and table examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe generated transcript exports such as plain text, SRT, VTT, and JSON when the agent executes the referenced workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
