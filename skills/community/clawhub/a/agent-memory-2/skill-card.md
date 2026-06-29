## Description: <br>
Persistent SQLite memory for Hermes and OpenClaw that stores facts, snippets, lessons, entities, relations, and provenance with authority lanes, conflict detection, bounded retrieval, and plugin-based recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmannixx](https://clawhub.ai/user/xmannixx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local persistent memory to Hermes or OpenClaw agents. It is intended for storing and retrieving bounded memory context across sessions while separating identity, preference, evidence, authorization, and procedural information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can store privacy-relevant or sensitive information across sessions. <br>
Mitigation: Review the SQLite database location, avoid storing secrets or sensitive personal data, and periodically run cleanup or purge stale memory. <br>
Risk: The scanned artifact only included documentation, so referenced implementation files were not artifact-verified. <br>
Mitigation: Verify the referenced source files and tests from the server-resolved provenance before installing or executing the skill. <br>
Risk: Automatically recalled memory can affect future agent responses if low-trust content is stored as authoritative context. <br>
Mitigation: Use the documented authority lanes and source restrictions, keep tool and external inputs quarantined to evidence, and require human approval for procedural rules. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/xMannixx/agent-memory-skill/tree/main/memory/agent-memory) <br>
- [ClawHub release page](https://clawhub.ai/xmannixx/skills/agent-memory-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, shell, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes local SQLite memory setup, CLI/API usage, plugin configuration, recall behavior, and operational safeguards.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
