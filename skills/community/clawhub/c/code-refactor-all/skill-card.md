## Description:

Guides behavior-preserving code refactors, rewrites, and cross-language ports through staged changes, tests, and parity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkxzhou](https://clawhub.ai/user/linkxzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to restructure, rewrite, or port existing code while checking that observable behavior remains unchanged unless differences are approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code transformations can unintentionally change existing behavior.

Mitigation: Review proposed changes and run baseline tests and parity fixtures; approve intentional differences explicitly.

Risk: An unreviewed skill update could change the instructions followed during workspace edits.

Mitigation: Install a pinned version or reviewed commit where possible; permit code edits only for implementation requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkxzhou/skills/code-refactor-all)
- [Port playbook](references/port-playbook.md)
- [Safety net](references/safety-net.md)
- [Sources and further reading](references/sources.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown plans and reports, with code and tests for requested implementation work]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports verification results, approved differences, and follow-ups; plan-only requests make no file changes.]

## Skill Version(s):

1.0.2 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
