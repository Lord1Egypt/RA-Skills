## Description:

Build and manage Apple-native container dev environments with ciderbox and orchard swarm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mentholmike](https://clawhub.ai/user/mentholmike)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Ciderbox to scaffold, run, test, and clean up Apple-native Linux container development environments from Apple Silicon Macs. The skill also guides local Orchard agent swarm setup, task execution, result collection, diagnostics, and teardown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may manage local Apple container VMs and alter or remove running Ciderbox environments.

Mitigation: Run Ciderbox commands only on intended Apple Silicon development machines, review VM lifecycle commands before execution, and treat chop commands as destructive.

Risk: Secret-push workflows can expose credentials to running Orchard trees or untrusted workloads.

Mitigation: Use short-lived, least-privilege credentials, avoid secrets push --all unless every running tree and workload is trusted, and rotate credentials after use.

Risk: Generated shell commands or configuration may not match the user's local container setup.

Mitigation: Run diagnostic checks such as ciderbox doctor or ciderbox orchard doctor and verify Apple container CLI prerequisites before executing build, test, or swarm commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review commands before execution, especially commands that destroy local Ciderbox environments or push secrets into running Orchard trees.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
