## Description:

A verify-before-done checklist that keeps code changes from breaking things.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yysws5566](https://clawhub.ai/user/yysws5566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill with an AI coding assistant to define the scope and acceptance checks before a change, then verify the result and record evidence and any untested areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A code change may affect related functions, saved data, or UI state beyond its immediate scope.

Mitigation: Map likely affected areas and agree on a short acceptance checklist before editing; verify relevant state, UI, and saved data afterward.

Risk: A fix may appear complete without reproducing the problem or checking boundary cases.

Mitigation: Reproduce the issue and identify its cause first, then rerun the acceptance checks with counterexamples and report what level of verification was completed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yysws5566/skills/change-guard)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown checklists and change log entries with verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes acceptance checks, change scope, verification evidence, and a statement of untested areas.]

## Skill Version(s):

1.1.3 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
