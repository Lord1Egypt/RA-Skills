## Description:

Cohesivity helps agents provision backend infrastructure for app projects through one HTTP API, including databases, hosting, auth, realtime, storage, email inbox, Redis, cron, and AI model APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anshuagrawal01](https://clawhub.ai/user/anshuagrawal01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent bootstrap, provision, and connect Cohesivity backend services for application projects when Cohesivity is already configured or no other backend provider is selected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates project credentials and makes external service calls to Cohesivity.

Mitigation: Use it only when Cohesivity is an acceptable external backend provider for the project, and keep the .cohesivity secrets file out of client code and version control.

Risk: Claiming tenants, provisioning paid resources, upgrades, and managed agents can create durable state or spending commitments.

Mitigation: Require explicit user approval before crossing those consent gates.

## Reference(s):

- [ClawHub Cohesivity Skill](https://clawhub.ai/anshuagrawal01/skills/cohesivity)
- [Cohesivity live docs index](https://cohesivity.ai/llms.txt)
- [Cohesivity latest skill](https://cohesivity.ai/skill.md)
- [Cohesivity pricing](https://cohesivity.ai/pricing)
- [Cohesivity managed agents](https://cohesivity.ai/offerings/managed-agents)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands, code changes, configuration details, and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read a project-root .cohesivity credential file and direct server-side calls to Cohesivity services.]

## Skill Version(s):

1.0.0 (source: server release metadata; skill frontmatter content version: 01f65efd7816)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
