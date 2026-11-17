## Description:

Turn a backend change into verifiable success criteria and a minimum useful test set across unit, integration, contract, and migration tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ritual](https://clawhub.ai/user/ritual)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert backend changes into concrete success criteria, focused test coverage, fixtures or mocks, commands to run, and explicit coverage gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Ritual Cloud setup can involve a global, unpinned install of @ritualai/cli.

Mitigation: Review the package and prefer a pinned or otherwise approved install path before enabling the optional cloud workflow.

Risk: Optional knowledge-note capture can persist repository documentation.

Mitigation: Approve knowledge-note writes only when the information is durable and intended to be retained in the repository.

Risk: A backend test plan can be incomplete when affected callers, external boundaries, migrations, or prior incidents are outside the provided context.

Mitigation: Provide the relevant service context and review the remaining coverage gaps before relying on the plan.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ritual/skills/backend-test-plan)
- [Ritual Homepage](https://ritual.work)
- [Open Knowledge Format overview](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with concise prose and inline shell commands when commands are available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes success criteria, minimum useful tests, fixtures or mocks, commands to run, and remaining coverage gaps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
