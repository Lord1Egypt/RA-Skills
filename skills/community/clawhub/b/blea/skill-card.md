## Description:

BLEA helps agents diagnose, capture, compare, and replay local Bluetooth Low Energy device behavior using BLEA MCP tools or the `ble` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitmi](https://clawhub.ai/user/nitmi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use BLEA to inspect BLE adapters and nearby devices, collect read-only evidence, compare captures, replay behavior offline, and prepare guarded write or exchange workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live BLE operations require native Bluetooth access on the agent host and can be mistaken for operations on the user's own workstation when run in a hosted environment.

Mitigation: Verify BLEA runtime, operating-system Bluetooth permission, and adapter availability before live work; otherwise analyze uploaded `.blea.jsonl` evidence or prepare local commands clearly labeled as not executed.

Risk: State-changing BLE writes can affect nearby devices if the target, characteristic, payload, or expected effect is wrong.

Mitigation: Require explicit authorization, exact resolved device confirmation, write guards, and read-back or notification verification before any write or exchange operation.

Risk: BLE captures may expose device identifiers, raw advertising data, GATT details, read values, notifications, errors, or cleanup evidence.

Mitigation: Use read-only capture mode, choose explicit output paths, redact identifiers before sharing captures off the workstation, and report only recorded structured evidence.

## Reference(s):

- [BLEA ClawHub skill page](https://clawhub.ai/nitmi/skills/blea)
- [BLEA workflow YAML](references/workflows.md)
- [BLE safety policy](references/safety.md)
- [Evidence Format v1](https://github.com/Nitmi/blea/blob/v0.6.1/docs/evidence-format-v1.md)
- [Diff Format v1](https://github.com/Nitmi/blea/blob/v0.6.1/docs/diff-format-v1.md)
- [Replay Format v1](https://github.com/Nitmi/blea/blob/v0.6.1/docs/replay-format-v1.md)
- [Platform Acceptance](https://github.com/Nitmi/blea/blob/v0.6.1/docs/platform-acceptance.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON or JSONL evidence descriptions, and YAML workflow snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local-execution caveats, exact-device identifiers, characteristic UUIDs, byte encodings, capture file paths, and structured failure summaries.]

## Skill Version(s):

0.6.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
