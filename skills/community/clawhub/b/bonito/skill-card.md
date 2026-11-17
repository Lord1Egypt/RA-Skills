## Description:

Onboard users to the Bonito AI platform for multi-provider AI routing, managed inference, agent deployment, and multi-agent orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shabarirepo](https://clawhub.ai/user/shabarirepo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get started with Bonito, create gateway keys, choose managed inference or provider keys, test gateway calls, and optionally deploy Bonito agents or the Atlas multi-agent demo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and run unpinned external code, including bonito-cli and the Atlas repository.

Mitigation: Pin and inspect bonito-cli and the Atlas repository before running installation, deployment, or test commands.

Risk: The skill can lead users to run Docker Compose services and deployment commands with Bonito or provider credentials.

Mitigation: Use disposable or least-privilege Bonito and provider credentials, review Docker Compose and shell scripts first, and prefer dry-run deployment before account changes.

Risk: The security scan verdict is suspicious because the onboarding flow includes external code execution and credentialed deployment actions.

Mitigation: Review this skill before installing or using it, and avoid production accounts until the workflow has been inspected.

## Reference(s):

- [Atlas Guide](references/atlas-guide.md)
- [Bonito Documentation](https://getbonito.com/docs)
- [Bonito Gateway Documentation](https://getbonito.com/docs#gateway)
- [Bonito Managed Inference Documentation](https://getbonito.com/docs#managed-inference)
- [BonBon Agent Documentation](https://getbonito.com/docs#bonbon)
- [Bonobot Orchestration Documentation](https://getbonito.com/docs#bonobot)
- [Bonito MCP Documentation](https://getbonito.com/docs#mcp)
- [Atlas Repository](https://github.com/ShabariRepo/atlas)
- [Bonito Skill Page](https://clawhub.ai/shabarirepo/skills/bonito)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands, curl examples, Python snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend external CLI, Docker, deployment, and API test commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
