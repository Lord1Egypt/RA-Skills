## Description: <br>
EvoMemory Core provides a local OpenClaw memory system with ChromaDB and LanceDB backends, hybrid retrieval, semantic deduplication, and offline operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lulan3954-a11y](https://clawhub.ai/user/lulan3954-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add or migrate local persistent memory for OpenClaw agents, including retrieval over stored memories without relying on external APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent agent memory can retain sensitive information. <br>
Mitigation: Avoid storing secrets or confidential data in memory and review stored content before relying on it. <br>
Risk: Installation can overwrite existing OpenClaw ChromaDB configuration. <br>
Mitigation: Back up ~/.openclaw/config/chromadb_config.yaml before installing or rerunning setup. <br>
Risk: A failed LanceDB migration may leave partially migrated data. <br>
Mitigation: Back up source data first and verify migrated document counts before switching backends. <br>
Risk: Remote ChromaDB settings can send memory data to a configured server. <br>
Mitigation: Use the local backend unless you intentionally operate and trust a remote ChromaDB server. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lulan3954-a11y/evomemory-core) <br>
- [Publisher profile](https://clawhub.ai/user/lulan3954-a11y) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and Python/configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory setup, migration, and usage guidance for OpenClaw agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
