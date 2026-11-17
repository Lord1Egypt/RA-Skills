## Description:

Guides agents through Baijimu Bundle lifecycle work with the baijimu CLI, including developing, freezing, reviewing, publishing, installing, upgrading, and uninstalling Bundles and resources within them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[momoplan](https://clawhub.ai/user/momoplan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Bundle-first public product lifecycle tasks in Baijimu, including Bundle and resource changes, immutable versioning, review submission, marketplace distribution, runtime installation, and end-to-end verification. It is not intended for Hosted Service backend construction, database migrations, or platform-internal releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the baijimu CLI and the @baijimu/cli npm package source.

Mitigation: Install it only for intended Baijimu Bundle workflows, verify the CLI package source and version, and compare behavior with the current Baijimu documentation before acting.

Risk: Publishing, installation, upgrade, and uninstall guidance can affect marketplace and runtime state.

Mitigation: Use a scoped Baijimu account and workspace, review proposed publish/install/uninstall actions, and verify target Bundle, Runtime, and service status after execution.

## Reference(s):

- [Baijimu Bundle Development Documentation](https://docs.baijimu.com/development/bundle-development/)
- [Baijimu Bundle Change and Release Workflow](https://docs.baijimu.com/development/bundle-development/change-and-release/)
- [Baijimu Platform Skill Homepage](https://github.com/momoplan/baijimu-platform-skill)
- [百积木 Bundle 开发 on ClawHub](https://clawhub.ai/momoplan/skills/baijimu-bundle-development)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Baijimu object IDs, statuses, error codes, and verification results from user-directed workflows.]

## Skill Version(s):

1.6.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
