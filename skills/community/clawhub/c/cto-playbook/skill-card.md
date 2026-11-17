## Description:

Provides CTO-level engineering guidance for architecture decisions, technology choices, DevOps, code quality, team planning, engineering document generation, and agent skill security review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chilu18](https://clawhub.ai/user/chilu18)

### License/Terms of Use:


## Use Case:

Developers, engineering leaders, and product teams use this skill to apply CTO-style engineering standards to architecture choices, delivery practices, engineering documents, code review, and agent skill security review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies broadly to coding tasks and may overreach by influencing work outside CTO-style planning, review, documentation, or security contexts.

Mitigation: Enable it deliberately for architecture, engineering process, review, documentation, and skill-security tasks rather than as a blanket default for all agent work.

Risk: The artifact recommends unpinned external scanner commands, including local, home-directory, and CI scans.

Mitigation: Pin and vet scanner versions, run with least privilege, and scope scans to intended files before adding commands to CI, hooks, or local workflows.

## Reference(s):

- [CTO & Engineering Excellence Playbook - Full Reference](references/full-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with templates and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ADRs, RFCs, postmortems, roadmaps, hiring plans, PRDs, reviews, CI guidance, and security scanning recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
