## Description:

Configures HTTP-to-HTTPS redirects on Alibaba Cloud ALB by inspecting listener and rule state, creating missing HTTP or HTTPS listeners, and adding redirect rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to audit an Alibaba Cloud ALB configuration and enforce HTTPS by guiding listener, rule, certificate, and server group changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote installers and plugin updates can change what runs between executions.

Mitigation: Review and control Aliyun CLI and plugin installation yourself; prefer verified, pinned CLI and plugin versions and avoid unverified latest downloads.

Risk: TLS private key material may be handled by the certificate helper workflow.

Mitigation: Do not use the bundled certificate helpers with production private keys unless the key-handling issues are fixed or otherwise mitigated.

Risk: The workflow performs cloud read-write actions against ALB and Certificate Management Service resources.

Mitigation: Use least-privilege RAM permissions and grant only the documented ALB and CAS actions needed for the run.

## Reference(s):

- [RAM Permissions](references/ram-policies.md)
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-network-alb-http-to-https)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single response stream; some workflows may create or update ALB listeners, rules, server groups, or uploaded certificates.]

## Skill Version(s):

0.0.1-beta.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
