## Description:

Local CSV, TSV, and JSONL inspection and cleanup toolkit for profiling, validation, deduplication, diffing, previewing, filtering, sorting, concatenation, joins, pivots, transformations, and format conversion using Python 3 standard library tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers, data operators, and agents use this skill to inspect, clean, validate, reshape, compare, and convert local tabular datasets before sending safe rows, reports, or derived files downstream.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Data-writing commands can erase source files when an output path points to an input file.

Mitigation: Use separate approved output paths, keep backups, and avoid reusing any input path as an output path until the aliasing issue is fixed.

Risk: CSV previews or reports may expose PII or secrets from local datasets.

Mitigation: Use the skill only on approved local datasets and avoid printing or saving previews and reports that contain sensitive data.

## Reference(s):

- [Clean CSV Toolkit ClawHub Skill Page](https://clawhub.ai/gopendrasharma89-tech/skills/clean-csv-toolkit)
- [Clean CSV Toolkit Homepage](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples; script outputs include CSV, TSV, JSON, JSONL, Markdown tables, and aligned text tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file-processing outputs depend on the selected command and caller-provided input and output paths; no remote calls are used.]

## Skill Version(s):

0.5.0 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
