## Description:

Document significant technical decisions with context, rationale, and consequences to maintain lightweight architectural records for future reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to decide when an ADR is warranted and to draft, review, and organize ADRs for important architecture and technology choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx installation command references a mutable GitHub path, which may change after review.

Mitigation: Review the install path before use and prefer a reviewed local copy or a pinned package version, repository commit, and checksum.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/architecture-decision-records)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with ADR templates and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ADR lifecycle guidance, template examples, directory and index conventions, tooling examples, and review checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
