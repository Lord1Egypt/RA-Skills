## Description:

Filament Vault helps agents manage a local 3D printing filament inventory by adding spools, logging usage, checking stock, searching records, and reporting stock and spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

3D printing users and shop operators use this skill to maintain a local filament spool inventory, track remaining material by brand, color, and material, and review low-stock or spending reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores filament inventory details, notes, storage locations, and purchase costs in a local JSON file.

Mitigation: Use it only for inventory data that is appropriate to store locally in the OpenClaw workspace and review file access before sharing the workspace.

Risk: Broad activation wording could cause the skill to be selected for general filament or 3D printing questions that are not inventory-management requests.

Mitigation: Tune triggers or invocation guidance when deployment requires activation only for explicit inventory tracking tasks.

## Reference(s):

- [Filament Materials Guide](references/materials.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inventory records are stored locally as JSON under the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
