## Description:

Guides Alibaba Cloud AgentLoop onboarding, instrumentation, runtime diagnostics, dataset and pipeline management, and evaluations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to onboard and instrument applications, diagnose runtime issues, and manage AgentLoop datasets, pipelines, and evaluations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud and Kubernetes operations can change or delete production resources.

Mitigation: Use a least-privilege RAM role and a temporary scoped kubeconfig; confirm exact targets and rollback plans before destructive actions.

Risk: Unverified HTTP Java-agent and curl-to-bash installation paths may introduce unsafe code.

Mitigation: Avoid these installation paths unless independently verified.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-agentloop-management)
- [AgentLoop onboarding](references/onboarding.md)
- [Live-Debug runtime diagnostics](references/live-debug-runtime.md)
- [High-code instrumentation](references/instrumentation/instrumentation.md)
- [Dataset management](references/dataset/dataset.md)
- [Pipeline management](references/pipeline/pipeline.md)
- [Evaluation](references/evaluation/evaluation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review proposed cloud operations before execution.]

## Skill Version(s):

0.1.6 (source: ClawHub release and skill manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
