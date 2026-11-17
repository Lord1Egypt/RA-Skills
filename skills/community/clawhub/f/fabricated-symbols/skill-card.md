## Description:

Code calls functions, classes, or methods that don't exist - either on project types or on third-party library APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to avoid fabricated API calls by verifying third-party and project symbols before writing or refactoring code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may still propose a fabricated third-party or project symbol if it skips verification.

Mitigation: Check official documentation, source code, type definitions, or project search results before invoking a symbol.

Risk: A fabricated symbol can pass through weak typing and fail at runtime.

Mitigation: Run the relevant type checker or tests after meaningful code changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mvogt99/skills/fabricated-symbols)
- [Publisher profile](https://clawhub.ai/user/mvogt99)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown guidance with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to inspect documentation, source code, type definitions, and type-checker output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
