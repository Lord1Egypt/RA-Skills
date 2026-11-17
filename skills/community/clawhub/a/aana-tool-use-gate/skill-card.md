## Description:

Controls and reviews external tool use for necessary, scoped, authorized, data-minimized, and safe operations that may affect state or reveal private data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this instruction-only skill to review planned tool calls before private-data, external, state-changing, or high-impact operations. It helps agents decide whether to proceed, narrow scope, ask for approval, retrieve limited evidence, defer, or refuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause agents to ask for confirmation more often before private-data access, external sends, destructive changes, financial actions, deployments, or privileged operations.

Mitigation: Apply the gate to tool-sensitive workflows and allow no-tool or low-risk read-only responses when they already satisfy the user request.

Risk: Review payloads could expose secrets, credentials, logs, private records, or unrelated private data if copied directly into a checker or message.

Mitigation: Use redacted summaries, exact IDs only when necessary, narrow date ranges, and limited fields; exclude secrets, auth headers, full logs, full records, and unrelated data.

Risk: Ambiguous target scope or authorization can make external, destructive, financial, privileged, or production actions unsafe.

Mitigation: Require exact tool, operation, target scope, and explicit approval or human review before high-impact or irreversible tool use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindbomber/skills/aana-tool-use-gate)
- [README](artifact/README.md)
- [Tool use review schema](artifact/schemas/tool-use-review.schema.json)
- [Redacted tool use review example](artifact/examples/redacted-tool-use-review.json)

## Skill Output:

**Output Type(s):** [guidance, text, JSON]

**Output Format:** [Markdown and plain-text instructions with optional JSON review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; no bundled code, dependencies, command execution, file writes, remote service calls, or persistent memory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
