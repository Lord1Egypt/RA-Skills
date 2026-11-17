## Description:

E2E automation engineer skill for route smoke checks, HTTP reachability, and lightweight UI confidence validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly check whether changed Weline routes, pages, or API surfaces still load, render, and route correctly before deeper acceptance testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run focused route or browser smoke checks and may refresh route registration when routes changed.

Mitigation: Install and use it only in the intended Weline project context, and review the command or browser path before execution.

Risk: A passing smoke check does not prove deeper business logic or full end-to-end behavior is correct.

Mitigation: Treat the result as reachability and basic rendering confidence, then run deeper acceptance validation for critical flows.

Risk: Referenced shared Weline guidance may affect how the skill should be applied.

Mitigation: Review the referenced shared project documents when they exist in the target repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/e2e-route-ui-smoke)
- [Publisher profile](https://clawhub.ai/user/aiweline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with route paths, commands, observed results, and pass/failure/follow-up status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include focused HTTP request commands or minimal browser-smoke paths for the affected route or UI surface.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
