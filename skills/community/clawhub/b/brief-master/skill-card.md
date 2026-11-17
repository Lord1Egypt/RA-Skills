## Description:

Write precise execution briefs for agents, cron jobs, reviewers, researchers, and delegated coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leostehlik](https://clawhub.ai/user/leostehlik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, reviewers, and agent orchestrators use Brief Master to turn underspecified requests into focused execution briefs with clear inputs, constraints, testable acceptance criteria, and verification steps before delegating work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A drafted brief can direct another agent to change code, run commands, or schedule persistent work, so mistaken or unapproved instructions may cause unwanted actions.

Mitigation: The user or orchestrator should review the brief, especially commands, paths, access needs, and scheduled work, before execution; the brief should require explicit approval for elevated access or persistent automation.

Risk: The security review was partial because a local path-like reference could not be resolved, leaving the scanner evidence incomplete.

Mitigation: Resolve and inspect the referenced material before relying on the scanner assessment.

## Reference(s):

- [9 Dimensions of Intent](references/9-dimensions.md)
- [Brief Formats](references/brief-formats.md)
- [Messy Request to Clean Brief](examples/messy-to-clean-brief.md)
- [Brief Master project page](https://github.com/LeoStehlik/brief-master)
- [Proof Loop](https://github.com/LeoStehlik/proof-loop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown execution brief with task scope, inputs, constraints, acceptance criteria, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask up to three clarifying questions when critical information is missing; includes a token-efficiency review.]

## Skill Version(s):

0.2.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
