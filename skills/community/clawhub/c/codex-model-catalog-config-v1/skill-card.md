## Description:

Manage models in an existing Codex model-catalogs/default.json catalog on Windows or macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hasakyi](https://clawhub.ai/user/hasakyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add, modify, remove, or list entries in their existing local Codex model catalog while preserving unrelated catalog content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent model catalog edits can affect future Codex model selection and behavior.

Mitigation: Review the exact model slug and requested fields before approving any catalog change.

Risk: Bundled catalog entries contain large inactive model-instruction strings that could expose unnecessary detail if printed.

Mitigation: Use compact probes and avoid echoing base_instructions or model_messages.

Risk: The workflow does not create backups or reconstruct missing catalogs.

Mitigation: Use it only for an existing model-catalogs/default.json and stop when the target file is absent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hasakyi/skills/codex-model-catalog-config-v1)
- [ClawHub publisher profile](https://clawhub.ai/user/hasakyi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [JSON file edits with concise Markdown or text status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the target default.json path, changed model slugs and fields, and JSON parse validation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
