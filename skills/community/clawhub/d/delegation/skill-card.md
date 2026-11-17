## Description:

Architecture-first workflow for delegating complex projects to AI coding agents. Ensures code fits the system before it's written.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelmonetized](https://clawhub.ai/user/michaelmonetized)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to make AI coding agents analyze architecture, declare target files, identify dependencies and consumers, and check for conflicts before implementing code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make an agent follow a stricter architecture-check workflow before writing code, which may be misapplied if the architecture source is unclear.

Mitigation: Confirm the architecture document and repository conventions the agent should follow before using the skill.

Risk: Generated implementation guidance may appear production-ready even when project-specific tests, linting, or security review have not run.

Mitigation: Review the declared filepath, dependencies, consumers, tests, and checklist results before accepting generated code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michaelmonetized/skills/delegation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections and fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes architecture analysis, filepath declaration, implementation, testing requirements, architectural impact, and a compliance checklist.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
