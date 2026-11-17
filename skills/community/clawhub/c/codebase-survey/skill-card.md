## Description:

Codebase Survey guides an agent through repository reconnaissance so it can summarize structure, architecture, code quality, deployment context, and maintainability before planning or implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelvillar1](https://clawhub.ai/user/adelvillar1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to onboard to unfamiliar or long-neglected codebases, run full surveys or targeted domain deep dives, and produce concise Markdown reports that support planning, handoffs, and maintenance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository surveys can expose sensitive architecture, timeline, customer, velocity, or operating-context details in the generated report.

Mitigation: Narrow the requested report before use and omit maturity, velocity, or future-reader context sections when those details are sensitive.

Risk: The workflow asks the agent to inspect repository structure, recent git history, documentation, schemas, and representative source files.

Mitigation: Run it only in repositories where that level of code and documentation access is appropriate, and keep secret-bearing files out of scope.

## Reference(s):

- [Codebase Survey ClawHub Skill Page](https://clawhub.ai/adelvillar1/skills/codebase-survey)
- [Codebase Survey Checklist](references/codebase-survey-checklist.md)
- [Targeted Domain Deep Dive Checklist](references/targeted-deep-dive-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with concise prose, tables, checklists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Synthesizes representative repository evidence and avoids raw file dumps except for brief quoted patterns.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
