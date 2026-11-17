## Description:

CI/CD pipeline requirements and deployment standards for gate sequencing, merge policy, staging deployment, production approval, and build-failure handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to configure CI/CD expectations, diagnose CI failures, and apply merge, staging, and production approval policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged artifact references a detailed pipeline requirements file that is not included in this release.

Mitigation: Review the referenced file if the publisher later includes it, and rely on repository-specific CI policies for exact gate definitions.

Risk: Staging auto-deploy guidance could be misread as permission to bypass existing release controls.

Mitigation: Keep production deployment tied to the repository's normal tag and approval controls.

## Reference(s):

- [CI/CD Compliance on ClawHub](https://clawhub.ai/urbantech/skills/ci-cd-compliance)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown prose with checklists and optional inline shell commands or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory CI/CD policy guidance; no autonomous deployment or credential handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
