## Description:

Deploy acceleration services using Alibaba Cloud Global Accelerator (GA) for cross-border Web/API access, global gaming, audio/video transmission, and enterprise application acceleration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to plan, configure, deploy, and verify Alibaba Cloud Global Accelerator services for latency-sensitive cross-region applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Aliyun CLI or plugin installation can introduce executable supply-chain risk.

Mitigation: Use a trusted package manager or verified pinned release, audit the Aliyun CLI source and plugin installation path, and disable automatic plugin installation unless it is needed.

Risk: Alibaba Cloud credentials may be exposed if configured inside an agent conversation or passed as command-line arguments.

Mitigation: Configure credentials outside the agent session, avoid secrets in command-line arguments, and prefer temporary or least-privilege RAM credentials.

Risk: Overbroad cloud permissions can expand the impact of deployment mistakes or compromised credentials.

Mitigation: Use a least-privilege RAM role or user limited to the intended Global Accelerator resources.

## Reference(s):

- [Skill release page](https://clawhub.ai/sdk-team/skills/alibabacloud-network-ga-deploy-acceleration)
- [GA Operational Important Notes](references/important-notes.md)
- [API and CLI Command Reference](references/related-apis.md)
- [RAM Permission Policies for GA Deployment](references/ram-policies.md)
- [GA Acceleration Performance Verification Guide](references/acceleration-test-guide.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [Alibaba Cloud Global Accelerator Documentation](https://help.aliyun.com/zh/ga/)
- [Alibaba Cloud GA OpenAPI Explorer](https://api.aliyun.com/product/Ga)
- [Network dial test acceleration guide](https://help.aliyun.com/zh/ga/use-cases/use-the-network-dial-test-tool-to-test-the-acceleration)

## Skill Output:

**Output Type(s):** [text, guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with tables and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment plans, Aliyun CLI commands, configuration summaries, and verification guidance; execution requires explicit user confirmation.]

## Skill Version(s):

0.0.1-beta.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
