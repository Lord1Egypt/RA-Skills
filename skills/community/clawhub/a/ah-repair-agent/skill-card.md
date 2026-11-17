## Description:

repair-agent helps an agent diagnose software defects, localize likely causes, propose patches, and validate fixes through test-driven repair workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to investigate failing tests or bug reports, identify likely root causes, generate candidate patches, and document validation results before accepting a repair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to edit code and run project tests.

Mitigation: Use version control, inspect proposed diffs, and review changes before accepting them.

Risk: Generated patches or diagnoses may be incomplete or incorrect.

Mitigation: Run the relevant test suite, add regression tests for the reported bug, and accept only changes with reviewed validation results.

## Reference(s):

- [RepairAgent examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/ah-repair-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with diagnostic summaries, ranked locations, patch suggestions, validation notes, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence scores, test outcomes, and final fix recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
