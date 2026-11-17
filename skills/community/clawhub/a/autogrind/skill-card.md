## Description:

Autogrind guides an agent to continue autonomous work through repeated overview, understanding, planning, execution, reflection, and pause cycles until the user explicitly stops it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttttonyhe](https://clawhub.ai/user/ttttonyhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, writers, and designers use Autogrind when they want an agent to keep improving a project across repeated work cycles until explicitly stopped.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Continuous autonomous work can continue beyond the user's intended scope and make repeated project changes.

Mitigation: Use only in disposable or version-controlled projects, set clear limits before starting, and monitor the session.

Risk: Weak stopping, approval, and persistence controls can increase the chance of unwanted changes during long-running sessions.

Mitigation: Avoid broad permissions, automatic commits, or exports unless they are intentionally enabled and supervised.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ttttonyhe/skills/autogrind)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Agent responses with task plans, edits, validation results, shell commands, and concise progress updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run repeated autonomous cycles and modify files inside the active project when permissions allow.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact metadata version 1.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
