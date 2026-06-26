## Description: <br>
Ingest documents into your Senso.ai knowledge base through Edith smart glasses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samdickson22](https://clawhub.ai/user/samdickson22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to upload substantial text or file contents into a Senso.ai knowledge base so the content can later be searched through Edith smart glasses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected user text or file contents to Senso.ai. <br>
Mitigation: Confirm the exact text or file before ingestion and avoid uploading secrets or regulated/private documents. <br>
Risk: The skill relies on a Senso.ai API key. <br>
Mitigation: Use a scoped Senso API key where possible and store it only in the agent's intended memory or configuration mechanism. <br>


## Reference(s): <br>
- [Senso.ai](https://senso.ai) <br>
- [Senso.ai raw content ingestion endpoint](https://sdk.senso.ai/api/v1/content/raw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and brief voice-ready confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SENSO_API_KEY and may upload selected text or file contents to Senso.ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: shipables.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
