## Description:

Runs existing project validation checks, diagnoses failures, makes focused fixes, and reports the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to run existing lint, type-check, test, and build commands, repair failures without masking regressions, and document remaining issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project validation scripts may perform actions beyond checking code.

Mitigation: Review commands from unfamiliar repositories before allowing the agent to run them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bovinphang/skills/fec-validation-fix)
- [Verification report template](references/report-template.md)
- [Frontend Craft project](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Markdown, Guidance]

**Output Format:** [Code changes and a Markdown verification report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports command results, fixes, and unresolved failures in reports/validation-fix-YYYY-MM-DD-HHmmss.md.]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
