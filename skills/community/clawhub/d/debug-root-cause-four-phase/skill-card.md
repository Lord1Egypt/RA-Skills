## Description:

4-phase root cause debugging: understand bugs before fixing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterliu-512](https://clawhub.ai/user/peterliu-512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents through a structured root-cause debugging workflow for test failures, production bugs, build failures, integrations, performance issues, and other technical defects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may spend extra time reproducing and investigating an issue before proposing a fix.

Mitigation: Use it when root-cause confidence matters, and narrow the requested scope when quick general coding help is preferred.

Risk: The skill may propose normal local investigation commands while debugging.

Mitigation: Review proposed commands and their scope before execution in sensitive workspaces.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Code, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill emphasizes reproducing the issue, forming falsifiable hypotheses, and validating fixes before implementation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
