## Description: <br>
Manages enterprise-level long-term memory by storing, retrieving, and filtering text data using vector similarity and confidence thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blackchen12](https://clawhub.ai/user/blackchen12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add durable semantic memory to agents, including storing high-confidence conversation facts and retrieving related memories as context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and reuse conversation-derived text as durable memory. <br>
Mitigation: Enable it only for deployments that intentionally need long-term memory, and add consent, retention limits, inspection, and deletion workflows before use. <br>
Risk: Stored memories may include sensitive information if upstream filtering is not added. <br>
Mitigation: Apply secret and PII filtering before memory writes, and protect the configured database path with access controls and encryption. <br>
Risk: The embedding model may be downloaded or loaded at runtime depending on the deployment environment. <br>
Mitigation: Confirm model download policy and model storage location before enabling the skill in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blackchen12/enterprise-memory-skill) <br>
- [Artifact README](artifact/README.md) <br>
- [Memory prompt instructions](artifact/prompts.md) <br>
- [Runtime configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [Plain text context snippets, JSON action results, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses confidence thresholds, retrieval top-k settings, and a configured vector database path.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
