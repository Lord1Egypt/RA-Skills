## Description: <br>
Search your Senso.ai knowledge base hands-free through Edith smart glasses. Triggers on knowledge/document queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samdickson22](https://clawhub.ai/user/samdickson22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users wearing Edith smart glasses use this skill to search their own Senso.ai knowledge base for documents, policies, and stored information, then receive concise spoken answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow may expose a raw Senso API key in a voice-first smart-glasses workflow. <br>
Mitigation: Configure the key through a protected secret or settings flow when available, use a limited Senso key, and rotate the key if it was spoken or pasted into chat history. <br>
Risk: Knowledge-base queries and possible document excerpts may be sent through OpenClaw and Senso. <br>
Mitigation: Use the skill only when those services are trusted for the relevant knowledge-base content and review organizational data-handling requirements before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samdickson22/edith-senso-knowledge) <br>
- [Senso.ai](https://senso.ai) <br>
- [Senso search endpoint](https://sdk.senso.ai/api/v1/search) <br>
- [Senso generate endpoint](https://sdk.senso.ai/api/v1/generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain spoken text with optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are intended to be concise for voice output; SENSO_API_KEY must be configured before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: shipables.json and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
