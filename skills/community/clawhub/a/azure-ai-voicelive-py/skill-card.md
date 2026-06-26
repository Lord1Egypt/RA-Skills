## Description: <br>
Build real-time voice AI applications using Azure AI Voice Live SDK (azure-ai-voicelive). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build Python applications with real-time bidirectional audio communication through Azure AI Voice Live, including voice assistants, voice-enabled chatbots, transcription workflows, function calling, MCP tools, and avatar integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure credentials or API keys may be exposed if copied into source code or logs. <br>
Mitigation: Use least-privilege Azure credentials, prefer managed identity or DefaultAzureCredential for production, and keep secrets in environment or secret-management systems. <br>
Risk: Voice applications may capture or stream sensitive spoken data. <br>
Mitigation: Obtain consent before recording or streaming speech, minimize sensitive audio collection, and apply appropriate data handling controls for transcripts and audio. <br>
Risk: Function calling or MCP tools can let model-selected calls perform real actions. <br>
Mitigation: Review and constrain available tools before deployment, require approval for sensitive actions, and validate tool arguments server-side. <br>


## Reference(s): <br>
- [Azure AI Voice Live SDK - API Reference](references/api-reference.md) <br>
- [Azure AI Voice Live SDK - Examples](references/examples.md) <br>
- [Azure AI Voice Live SDK - Models Reference](references/models.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/thegovind/azure-ai-voicelive-py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance for Azure AI Voice Live SDK usage, including authentication, session configuration, event handling, audio streaming, and risk-aware deployment notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
