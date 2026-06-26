## Description: <br>
Controls and reviews external tool use for necessary, scoped, authorized, data-minimized, and safe operations that may affect state or reveal private data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this instruction-only skill to gate risky tool calls before an agent reads private data, changes external state, sends information, performs financial actions, or uses privileged systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause agents to request more confirmations around private data, external sends, destructive actions, production systems, and payments. <br>
Mitigation: Use the gate for explicit approval and human review when actions are risky, ambiguous, high impact, irreversible, privileged, financial, or externally visible. <br>
Risk: Review payloads may expose sensitive data if copied from raw tool inputs or outputs. <br>
Mitigation: Use redacted summaries and omit secrets, credentials, full private records, full logs, full transcripts, full directory dumps, and unrelated private data. <br>
Risk: An external checker could introduce trust or disclosure concerns if misconfigured. <br>
Mitigation: Use only a trusted checker configured by the user or administrator, or fall back to manual review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-tool-use-gate) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Tool use review schema](artifact/schemas/tool-use-review.schema.json) <br>
- [Redacted tool use review example](artifact/examples/redacted-tool-use-review.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Configuration] <br>
**Output Format:** [Markdown instructions with optional JSON review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute commands, install dependencies, call services, write files, or persist memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
