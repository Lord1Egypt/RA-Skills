## Description:

Discover and send tasks to A2A agents through an A2A API Gateway, including finding agents or providers, delegating tasks, checking task status, and routing work to a specific agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thearchitectit](https://clawhub.ai/user/thearchitectit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover available A2A agents or LLM providers, delegate work through an A2A API Gateway, and retrieve task status or results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal task actions use administrator-level gateway tokens.

Mitigation: Use only in a trusted test environment or change the scripts to use scoped credentials instead of admin bootstrap before broader deployment.

Risk: Unsafe input handling can expose task routing to unintended targets or data handling.

Mitigation: Validate agent slugs, require HTTPS for non-local gateways, and avoid sending secrets or confidential work through external agents or providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thearchitectit/skills/a2a-client)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3 on linux or darwin, plus an A2A gateway URL and optional API key.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
