## Description:

Apply agent-led software development workflows for planning, implementation, TDD, verification, security review, code review, shipping, repository analysis, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunakkathuria](https://clawhub.ai/user/raunakkathuria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Buildwright to plan, implement, test, review, document, and ship software changes, or to analyze and clean up an existing repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated repository guidance or documentation may be inaccurate.

Mitigation: Review generated .buildwright files and documentation before relying on them.

Risk: The ship command can commit, push, and open a pull request.

Mitigation: Invoke /bw-ship only when outbound git actions are intended; review the changes before shipping.

## Reference(s):

- [Buildwright project homepage](https://github.com/raunakkathuria/buildwright)
- [Buildwright on ClawHub](https://clawhub.ai/raunakkathuria/skills/buildwright)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Text and Markdown, with repository files and code changes when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce plans, review findings, documentation, and pull requests depending on the selected command.]

## Skill Version(s):

0.0.22 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
