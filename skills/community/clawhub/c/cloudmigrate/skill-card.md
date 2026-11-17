## Description:

Cloudmigrate helps agents plan multi-cloud migrations and generate infrastructure-as-code, deployment workflows, and provisioning guidance across AWS, Azure, and GCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to plan cloud migrations, generate IaC and deployment automation, and prepare validation or rollback guidance for AWS, Azure, GCP, and hybrid environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cloud credentials and high-impact infrastructure actions can affect live resources when used without tight scoping.

Mitigation: Use separate, least-privilege, short-lived credentials for only the active cloud provider and review commands before applying changes.

Risk: Generated Terraform, deployment commands, and network rules may be incorrect or too permissive.

Mitigation: Treat generated infrastructure and deployment artifacts as drafts that require security review, especially for network egress rules and resource-modifying commands.

Risk: Prompts or generated files may expose sensitive cloud secrets if real credentials are pasted into the agent workflow.

Mitigation: Avoid entering real secrets into prompts or generated files; use secret managers, environment isolation, and credential rotation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/cloudmigrate)
- [Skill homepage from artifact metadata](https://github.com/ncreighton/empire-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, configuration snippets, and structured JSON, YAML, or HCL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include migration plans, IaC drafts, deployment commands, cost analysis, risk notes, validation checks, and rollback procedures.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
