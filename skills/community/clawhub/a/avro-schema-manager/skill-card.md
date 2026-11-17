## Description:

Manage Apache Avro schemas by validating structure, checking schema compatibility, planning evolution, auditing namespace and registry conventions, and generating code guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to inspect Avro schemas, validate .avsc/.avdl/.avpr files, assess forward and backward compatibility, review schema registry settings, and plan safe schema evolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect schema files and related project code that the user points it at, including private project directories.

Mitigation: Scope use to relevant schema directories and specific old/new schema versions instead of broad private directories.

Risk: Compatibility and migration recommendations can be context-dependent and may be misleading if schema registry mode, consumers, or producer behavior are incomplete.

Mitigation: Review recommendations with the owning engineering team and verify changes with schema registry or CI compatibility checks before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/avro-schema-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include schema health scores, compatibility matrices, remediation plans, code-generation commands, and migration guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
