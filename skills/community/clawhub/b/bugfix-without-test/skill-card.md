## Description:

A fix is applied without a reproduction test, leaving no proof the bug is fixed and no regression coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when fixing bugs to require a reproduction test, verify the fix, and preserve regression coverage. It also guides explicit manual verification notes when automated tests are impractical.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause the agent to spend extra effort adding or requesting regression tests when fixing bugs.

Mitigation: Plan for the extra test-writing or review effort; this behavior matches the scanner guidance and the skill's coding-quality purpose.

Risk: If a bug is hard to test, the fix may still lack automated regression coverage.

Mitigation: Record the manual verification performed and explain why automated coverage was impractical, as directed by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mvogt99/skills/bugfix-without-test)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, credentials, tools, or external services are requested by the skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
