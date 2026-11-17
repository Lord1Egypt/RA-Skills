## Description:

Design, prototype, build, QA, and ship Chrome extensions across separate plugin, template, and product repos with explicit publish lanes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and extension teams use this skill to design, prototype, validate, package, and prepare Chrome extensions while keeping plugin, template, and product repositories separated by publish lane.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may run unaudited Python scripts from relative paths outside the packaged skill.

Mitigation: Confirm the repository layout and exact script paths, inspect those scripts, and run the workflow from a controlled working directory with only required files and credentials available.

Risk: Chrome extension release steps can use the wrong publish lane or broaden extension permissions if release metadata is changed carelessly.

Mitigation: Keep permissions, host matches, and store metadata narrow in extension.release.json; validate the release profile and lane before recommending ship steps.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and repository file recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on relative workflow scripts that should be inspected before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
