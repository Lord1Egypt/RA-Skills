## Description:

Manage multiple SaaS startups simultaneously with CEO-driven orchestration, product agents, ChatDev code generation, and a 3-Gate BUILD, TEST, JUDGE pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[csbenson001](https://clawhub.ai/user/csbenson001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and startup operators use this skill to coordinate multiple product agents, route work through CEO-style prioritization, and enforce BUILD, TEST, and JUDGE gates for SaaS product development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path depends on unpinned external code and a setup script that is unavailable in the submitted artifact.

Mitigation: Review setup files and external dependencies before installation, and pin the ClawHub installer version and ChatDev commit where possible.

Risk: The workflow may require access to product repositories and API keys.

Mitigation: Run setup from a low-privilege environment and avoid exposing unnecessary repositories or credentials until installed files and scripts have been inspected.

## Reference(s):

- [Dark Factory Skill on ClawHub](https://clawhub.ai/csbenson001/skills/dark-factory-skill)
- [ChatDev](https://github.com/OpenBMB/ChatDev)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with setup steps, workflow guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through multi-agent startup orchestration, product configuration, and gated validation workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
