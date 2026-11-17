## Description:

Bridge Evolver GEP prompts to OpenSpace MCP execute_task for automated execution. Handles path mapping, base64 encoding, timeout circuit breaker, and file readiness detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to send Evolver-generated GEP prompts to OpenSpace for automated execution, map Windows paths for WSL, and locate the resulting output files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automation may finalize generated results without substantive review.

Mitigation: Review generated output and proposed Evolver changes before finalization; make finalization opt-in or require explicit review where the surrounding workflow allows it.

Risk: A bridge path may wait indefinitely, and the security assessment has partial coverage.

Mitigation: Supervise runs with an external deadline, and review the skill's behavior before installation because the assessment is incomplete.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/147258xuan/skills/evolver-open-space-bridge)
- [Publisher profile: 147258xuan](https://clawhub.ai/user/147258xuan)

## Skill Output:

**Output Type(s):** [Files, Code, Text, Markdown]

**Output Format:** [Generated files in the configured output directory, with textual execution status and JSON-RPC response output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a supplied GEP prompt and supports a configurable output directory; defaults to memory/evolution/openspace_output/ for bridge output.]

## Skill Version(s):

0.1.0 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
