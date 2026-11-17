## Description:

Diagnoses GPU device status, driver installation issues, and hardware failures on Alibaba Cloud ECS GPU instances using Console Diagnosis and Cloud Assistant diagnosis modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to diagnose single-instance, batch, or scheduled GPU health checks for Linux Alibaba Cloud ECS GPU instances and interpret Console Diagnosis and Cloud Assistant results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents high-impact Alibaba Cloud command authority for ECS diagnostic and Cloud Assistant operations.

Mitigation: Use a tightly scoped RAM identity with only the documented permissions and review commands before execution.

Risk: Untrusted instance lists, tag values, or region inputs could direct diagnosis commands at unintended resources.

Mitigation: Use explicit instance lists when possible, validate region and instance IDs, and avoid untrusted tag or region inputs.

Risk: CLI installation and plugin update steps depend on mutable external sources.

Mitigation: Verify Alibaba Cloud CLI and plugin sources independently before installation or update.

Risk: Scheduled diagnosis creates persistent cloud automation.

Mitigation: Track scheduled invocations, use stop-invocation only when explicitly requested, and clean up scheduled resources manually in the console.

## Reference(s):

- [Alibaba Cloud CLI Installation Guide](references/cli-installation.md)
- [RAM Permission List](references/ram-policies.md)
- [Alibaba Cloud CLI official installation documentation](https://help.aliyun.com/zh/cli/install-cli)
- [Alibaba Cloud GPU driver installation guide](https://help.aliyun.com/zh/egs/install-a-gpu-driver-on-a-gpu-accelerated-compute-optimized-linux-instance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and diagnosis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streams diagnosis results as each method or instance completes; findings are grouped by diagnosis method.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
