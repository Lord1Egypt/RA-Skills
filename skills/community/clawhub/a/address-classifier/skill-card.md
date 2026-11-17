## Description:

Classifies China address records into local city, in-province other city, out-of-province, or incomplete categories, with configurable Guizhou and Guiyang mappings and limited search completion for partial addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhh8896416](https://clawhub.ai/user/zhh8896416)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data-processing agents use this skill to classify tabular China address datasets for administrative-region cleanup, regional statistics, routing, and data management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Address datasets, output files, and debug logs may contain sensitive personal or location information.

Mitigation: Process only datasets the user is authorized to handle, limit retention of generated files and logs, and avoid sharing raw records beyond the intended workflow.

Risk: Untrusted CSV or TSV outputs can be unsafe when opened in spreadsheet software if cells contain formula-like content.

Mitigation: Neutralize formula-like cells before spreadsheet use or review outputs in plain-text tooling.

Risk: The dependency list includes PyYAML without a strict pin, while the core artifact does not require it for the shown classifier flow.

Mitigation: Remove the unused dependency or pin it to an approved version before installation in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhh8896416/skills/address-classifier)
- [README](artifact/README.md)
- [Skill document](artifact/SKILL.md)
- [Configuration](artifact/config/config.yaml)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python code examples, shell commands, configuration files, and TXT/CSV/JSON address-classification outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes UTF-8 tab-separated input files containing an ID column and address column; default output is tab-separated text with configurable CSV or JSON output.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-03-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
