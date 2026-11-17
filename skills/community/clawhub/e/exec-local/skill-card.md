## Description:

Exec Local executes system-level shell commands inside the thundarr-gpu container for monitoring and remote orchestration tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrslu01](https://clawhub.ai/user/zrslu01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run shell commands inside a local container for health checks, process inspection, network diagnostics, and remote host orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted shell access can perform high-impact actions in the container environment.

Mitigation: Install only in a hardened, disposable, least-privileged container with no unnecessary secrets, mounts, SSH keys, or broad network reach.

Risk: Remote-host or state-changing operations can affect systems beyond the container.

Mitigation: Use explicit human approval and command allowlists for remote-host or state-changing operations.

Risk: Automated workflows may pass unsafe command input to the execution interface.

Mitigation: Sanitize command inputs before automation and review commands before execution.

## Reference(s):

- [Exec Local ClawHub listing](https://clawhub.ai/zrslu01/skills/exec-local)
- [Publisher profile](https://clawhub.ai/user/zrslu01)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text stdout and stderr from command execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the container user permissions and available local or remote tools.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact manifests)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
