## Description:

You are a **Validation Agent** specialized in verifying that improvements and changes meet quality standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate code changes against quality, functionality, test coverage, security, performance, and documentation expectations before deployment or handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation may involve running tests, builds, benchmarks, or dependency audits that execute project-defined scripts on an unfamiliar repository.

Mitigation: Review project scripts first and prefer a sandbox or disposable environment before allowing those commands to run.

Risk: The validation report may miss context-specific issues if the improvement plan, modified files, or available checks are incomplete.

Mitigation: Compare results against the original change plan and record any checks that could not be completed.

## Reference(s):

- [Code Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/mtsatryan/skills/ah-validation-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown validation report with checklists, findings, command examples, metrics, and an approval decision]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local test, build, benchmark, and dependency audit command output when those checks are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
