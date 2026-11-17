## Description:

Runs project checks before and after code changes and reports a tool-determined verification verdict, including regressions or checks that could not be verified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[return054](https://clawhub.ai/user/return054)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI coding agents use this skill to run project syntax, lint, type, and test checks around code changes and identify failures or regressions before reporting completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-defined test and lint commands may execute untrusted code with access to the user's local environment.

Mitigation: Review the commands before running them in unfamiliar repositories, or use a sandboxed workspace without sensitive credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/return054/skills/ai-code-verification-guard)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown verdict block with check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports PASS, PASS_WITH_UNVERIFIED, FAIL, REGRESSION, or UNVERIFIED; missing tools and unsupported projects may leave checks unverified.]

## Skill Version(s):

1.0.1 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
