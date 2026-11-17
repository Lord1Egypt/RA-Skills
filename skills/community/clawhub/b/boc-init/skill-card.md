## Description:

Initializes a BOC container platform deployment host by checking the environment, verifying and unpacking the deployment package, running bocctl init, and validating key services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongruiji](https://clawhub.ai/user/hongruiji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and deployment engineers use this skill to initialize a BOC container platform deployment host from a local deployment package. It guides environment checks, SHA256 verification, package extraction, bocctl init execution, and post-initialization service checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root SSH and password-based access can expose privileged credentials or allow unintended host changes.

Mitigation: Use an approved SSH key or secret-manager workflow on a dedicated deployment host, and avoid root password authentication where possible.

Risk: Unverified deployment packages or password-tool downloads can introduce compromised binaries into the deployment process.

Mitigation: Verify deployment packages and tools with trusted checksums or signatures, and replace ad hoc sshpass installation guidance with managed tooling.

Risk: Deleting an existing deployment directory before unpacking can remove useful state or damage a deployment host.

Mitigation: Require operator confirmation and backups before removing any existing deployment directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongruiji/skills/boc-init)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports deployment-host initialization status and key component checks such as ansible, nerdctl containers, and containerd service state.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, artifact/_meta.json, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
