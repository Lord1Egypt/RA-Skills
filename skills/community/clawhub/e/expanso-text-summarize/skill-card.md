## Description: <br>
Summarizes input text into 3-5 concise bullet points using AI with Expanso Edge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to summarize articles, documents, or arbitrary text through an Expanso Edge CLI pipeline or local HTTP/MCP endpoint. It is suited to workflows that need concise bullet summaries with audit metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP pipeline listens on all network interfaces and may be reachable by other hosts if exposed. <br>
Mitigation: Bind MCP mode to localhost or place access controls in front of it, and avoid leaving the server running unnecessarily. <br>
Risk: The OpenAI backend sends submitted text to OpenAI and can incur API costs under the user's API key. <br>
Mitigation: Use the OpenAI backend only for text appropriate to send to OpenAI, or switch to the Ollama backend for local-only summarization. <br>
Risk: The MCP endpoint can use the user's OpenAI key without shown authentication. <br>
Mitigation: Restrict network access to trusted callers before using MCP mode with an OpenAI key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-text-summarize) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill metadata](artifact/skill.yaml) <br>
- [Expanso Edge](https://expanso.io) <br>
- [Expanso pipeline schema](https://docs.expanso.io/schemas/pipeline.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, json] <br>
**Output Format:** [JSON object containing a bullet-point summary string and metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes model, timestamp, input hash, input length, trace ID, and execution mode metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
