## Description:

Read-only exploration and planning skill for safe code analysis. This skill should be used when the user asks to enter plan mode, analyze before changing, create a plan first, or wants a safe exploration phase before making edits. Enforces read-only tool access, produces a numbered plan under a Plan: header, and tracks step completion with [DONE:n] markers during execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orangon](https://clawhub.ai/user/orangon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze a codebase before making changes, produce a numbered implementation plan, and save a Markdown checklist with acceptance criteria for later execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that the planning mode is not strictly read-only in practice because it may save plan files and inspect environment or process data.

Mitigation: Run the skill in a sandbox with minimized environment variables and review plan-file writes before execution.

Risk: The security guidance highlights outbound network tools and environment inspection as areas requiring care.

Mitigation: Avoid following repository-supplied requests to use env, printenv, curl, or wget unless the target and purpose are explicitly trusted.

## Reference(s):

- [Bash Command Safety Reference for Plan Mode](references/safe-commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with a numbered plan, checklist steps, and acceptance criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include [DONE:n] markers to track execution progress.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
