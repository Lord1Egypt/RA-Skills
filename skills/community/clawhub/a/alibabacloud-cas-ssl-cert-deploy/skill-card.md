## Description: <br>
Deploy SSL certificates to Alibaba Cloud products such as CDN, SLB, WAF, ALB, NLB, OSS, and ESA through the CAS DeploymentJob API, with progress tracking, failure diagnosis, rollback, and HTTPS verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations teams use this skill to deploy Alibaba Cloud-issued SSL certificates to supported Alibaba Cloud products through a controlled CAS deployment workflow. The skill is intended for certificate rollout, deployment-status tracking, failure diagnosis, rollback, and HTTPS verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage certificate deployment and may create or alter Alibaba Cloud CDN, WAF, OSS, and ALB resources. <br>
Mitigation: Install it only for intended Alibaba Cloud certificate-deployment workflows, use a dedicated low-privilege RAM role, and require explicit confirmation before resource creation, rollback, deletion, or listener and routing changes. <br>
Risk: Credential and private-key handling can expose sensitive material if secrets are pasted into chat or command arguments. <br>
Mitigation: Configure credentials outside the agent session, avoid entering AccessKey or private-key material in chat or shell arguments, and review credential status without printing secret values. <br>
Risk: Helper flows for ALB and OSS can affect cloud product configuration beyond certificate deployment. <br>
Mitigation: Review the ALB and OSS helper flows before use and confirm each resource-changing action with the user before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-cas-ssl-cert-deploy) <br>
- [Publisher profile](https://clawhub.ai/user/sdk-team) <br>
- [API commands](references/api-commands.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Helper flows](references/helper-flows.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Error handling](references/error-handling.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Related commands](references/related-commands.md) <br>
- [CLI installation guide](references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before sensitive deployment, resource creation, rollback, deletion, or listener and routing changes.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
