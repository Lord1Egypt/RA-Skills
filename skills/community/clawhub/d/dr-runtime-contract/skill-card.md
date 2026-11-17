## Description:

Runtime configuration changes: propagate, detect stale declarations, and prove capability across enabled execution paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to propagate session-persistent runtime configuration changes and verify that each enabled execution path resolves the intended source and passes a safe, read-only capability probe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manifests or receipts could expose credentials or secret-derived data.

Mitigation: Record only secret references, source identifiers, and non-secret revisions; omit values, tokens, request and response data, and secret-derived hashes.

Risk: Reloading or restarting a live service could interrupt operations.

Mitigation: Follow the owning service procedure and its approval gate; pause when interruption risk is unclear.

Risk: Verification could affect an unintended environment or execution path.

Mitigation: Limit checks to the intended environment and enabled paths, using safe authenticated read-only probes.

## Reference(s):

- [DR Runtime Contract on ClawHub](https://clawhub.ai/daniel-refahi-ikara/skills/dr-runtime-contract)
- [Publisher profile: daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Markdown]

**Output Format:** [Markdown checklists and a non-secret YAML runtime contract manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes path verification criteria and a redacted completion receipt; excludes secret values.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
