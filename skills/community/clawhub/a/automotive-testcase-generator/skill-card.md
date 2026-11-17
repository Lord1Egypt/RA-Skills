## Description:

Automotive Test Case Generator creates standardized, traceable Excel test cases for automotive electronics and intelligent connected vehicle requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automotive test teams use this skill to turn automotive requirement descriptions or documents into structured, module-grouped test cases with traceability and coverage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided automotive requirements may contain proprietary vehicle or product information.

Mitigation: Use the skill only in trusted agent environments and remove or mask sensitive requirement details before processing.

Risk: The generated Excel workbook may be written to an unexpected location if the user and agent do not agree on the output path.

Mitigation: Confirm the intended output directory before running the Excel generation step.

Risk: Generated test cases can miss domain intent or overstate coverage when source requirements are incomplete.

Mitigation: Review generated cases, assumptions, and coverage statistics against the original requirements before using them for validation planning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kokxi/skills/automotive-testcase-generator)
- [Automotive domain knowledge](references/domain-knowledge.md)
- [Automotive test case format specification](references/format-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with structured JSON-like test case data and Python/openpyxl generation steps for Excel output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may produce an .xlsx workbook with test cases and coverage statistics when used in an agent environment that can run Python 3 and openpyxl.]

## Skill Version(s):

1.1.0 (source: server release.version; artifact metadata version V1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
