## Description:

E2E automation engineer skill for route smoke checks, HTTP reachability, and lightweight UI confidence validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly confirm that changed routes, pages, or API surfaces are registered, reachable, and rendering at a basic level before deeper acceptance testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to run route refresh or HTTP request commands in a project environment.

Mitigation: Review proposed commands before execution, especially in production or shared environments.

Risk: A passing smoke check only proves basic reachability or rendering and may miss deeper business logic issues.

Mitigation: Use the result as quick confidence and run deeper scenario or acceptance tests when the change affects core behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/e2e-ui)
- [Publisher profile](https://clawhub.ai/user/aiweline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the checked route or UI path, command or browser path used, observed pass/fail result, and any follow-up required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
