## Description:

Local JSON / JSONL inspection and manipulation toolkit for inspecting nested structures, querying with a jq-style path language, flattening and unflattening data, merging, patching, and validating JSON using Python 3 standard library tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect, query, transform, merge, patch, and validate local JSON or JSONL files without external JSON tooling or network calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inspection and query output can expose sample values from sensitive local JSON or JSONL files in terminal output or logs.

Mitigation: Avoid running inspection on secrets or redact inputs first; reduce sampling when representative values are not needed.

Risk: Patch, merge, flatten, and unflatten workflows can write changed JSON files that may be difficult to recover if applied to important data.

Mitigation: Use --dry-run where available, write to a separate output path, and keep backups or version control for important files.

Risk: Untrusted validation schemas with complex regular expressions can cause excessive processing or misleading validation results.

Mitigation: Use trusted schemas, avoid complex regex patterns from untrusted sources, and review validation errors before acting on them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gopendrasharma89-tech/clean-json-toolkit)
- [ClawHub skill page](https://clawhub.ai/gopendrasharma89-tech/skills/clean-json-toolkit)
- [clean-csv-toolkit](https://clawhub.ai/gopendrasharma89-tech/clean-csv-toolkit)
- [clean-text-toolkit](https://clawhub.ai/gopendrasharma89-tech/clean-text-toolkit)
- [clean-log-toolkit](https://clawhub.ai/gopendrasharma89-tech/clean-log-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include file paths, JSON summaries, transformed JSON files, validation reports, or patch results depending on the selected script.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
