## Description: <br>
Requires agents to classify memory operations and get explicit approval before storing, reusing, editing, importing, exporting, or deleting user memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a review gate around agent memory so memory use is relevant, minimized, sensitivity-aware, and explicitly approved when required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace capability tags include crypto and purchase-related capabilities that are unrelated to this instruction-only memory skill. <br>
Mitigation: Before enabling platform permissions, verify that those tags do not grant real crypto or purchase authority. <br>
Risk: A configured external AANA checker could receive sensitive memory context if payloads are not minimized. <br>
Mitigation: Use only trusted checker interfaces and send redacted review payloads instead of raw secrets, private records, full logs, or unrelated private data. <br>
Risk: Agents may store, reuse, edit, delete, import, or export memory without clear user consent. <br>
Mitigation: Require explicit approval for persistent memory changes, import/export, and sensitive reuse; do not treat silence as approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-agent-memory-gate) <br>
- [Publisher profile](https://clawhub.ai/user/mindbomber) <br>
- [schemas/agent-memory-gate.schema.json](artifact/schemas/agent-memory-gate.schema.json) <br>
- [examples/redacted-agent-memory-gate.json](artifact/examples/redacted-agent-memory-gate.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown instructions with optional JSON review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; no bundled code, dependencies, command execution, file writes, service calls, or memory persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
