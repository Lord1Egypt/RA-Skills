## Description:

Analyzes CIS Red Hat Enterprise Linux Benchmark rules against an OpenEuler security configuration baseline and reports which rules are fully covered, partially covered, or not covered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x008](https://clawhub.ai/user/0x008)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, compliance analysts, and platform maintainers use this skill to compare CIS RHEL Benchmark requirements with OpenEuler baseline content and generate rule-level coverage reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned dependency ranges can resolve to newer package versions with changed behavior.

Mitigation: Install dependencies in an isolated virtual environment and prefer pinned or locked versions for repeatable runs.

Risk: Input PDFs and Markdown baselines may contain malformed, misleading, or untrusted document text.

Mitigation: Process documents from trusted sources and review extracted JSON before relying on coverage conclusions.

Risk: Fuzzy matches and value-strictness comparisons can produce uncertain coverage classifications.

Mitigation: Manually review fuzzy matches, partial coverage results, and entries marked for confirmation before using the report for compliance decisions.

Risk: Generated CSV files can carry untrusted document text into spreadsheet software.

Mitigation: Treat CSV outputs as untrusted when opening them in spreadsheets; use JSON or text outputs for exact review when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0x008/skills/cis-rhel-openeuler-coverage)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, CSV files, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON intermediate files, and bilingual CSV/text coverage reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include exact, fuzzy, or no-match status and identify rules that need manual confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
