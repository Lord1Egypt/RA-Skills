## Description:

流体网络求解与分析工具，输入 TOML 格式的网络描述，计算压力流量分布，并分析负载状态和连通性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redflag666](https://clawhub.ai/user/redflag666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate steady-state hydraulic, environmental-control, and chemical-process fluid networks from TOML descriptions, including scenario changes, load thresholds, and connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled virtual-environment contents and unpinned dependencies can make dependency review and updates harder.

Mitigation: Remove the bundled venv from distribution and install pinned, reviewed dependencies in the target environment.

Risk: Very large or untrusted TOML network inputs may consume excessive local resources because input-size limits are not documented.

Mitigation: Run with resource limits and accept only trusted or size-bounded TOML inputs until explicit input limits are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redflag666/skills/fluid-network-solver)
- [TOML schema](artifact/SCHEMA.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [JSON object with pressures, flows, and load/connectivity analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from local TOML input and an optional scenario name.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
