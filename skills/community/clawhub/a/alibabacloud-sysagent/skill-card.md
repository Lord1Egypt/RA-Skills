## Description:

Guides Alibaba Cloud operators through Linux diagnostics, crash analysis, health checks, performance profiling, security assessment, OS customization, and Java runtime troubleshooting with SysAgent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and operations engineers use this skill to investigate Linux systems on Alibaba Cloud and manage SysAgent diagnostic tasks through the Alibaba Cloud CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guide includes running a downloaded shell script without verifying it.

Mitigation: Review installation steps and verify the downloaded script before running it.

Risk: Diagnostic requests could include credentials, secrets, or unnecessary sensitive details.

Mitigation: Keep credentials and secrets out of diagnostic requests, and share only details needed for the task.

Risk: The security scan had partial coverage, including one degraded static analysis, so its evidence is incomplete.

Mitigation: Review components not fully inspected before relying on the scan as a complete security assessment.

## Reference(s):

- [SysAgent Product Overview](https://help.aliyun.com/zh/alinux/sysagent-overview)
- [Start and Manage SysAgent Tasks](https://help.aliyun.com/zh/alinux/use-sysagent-to-start-and-manage-tasks)
- [SysAgent CLI Reference](artifact/references/sysagent-cli.md)
- [SysAgent CLI Setup](artifact/references/setup.md)
- [Aliyun CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [RAM Authorization Guidance](artifact/references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with diagnostic summaries and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize task progress, evidence, limitations, and artifact delivery status.]

## Skill Version(s):

0.0.1 (source: evidence.json release and artifact/references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
