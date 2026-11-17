## Description:

Inspect Linux hardware and live resource state, collect temperatures and sensor evidence, monitor bounded observation windows, validate workload requirements, and compare hosts using fitctl JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tznurmin](https://clawhub.ai/user/tznurmin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect a local Linux host, record current resource and sensor evidence, and assess whether it meets explicit workload requirements. It also helps compare hosts using saved JSON reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local hardware and resource reports may expose sensitive host details when shared.

Mitigation: Keep reports in a separate workspace and inspect or redact artifacts before sharing them.

Risk: Example scripts download pinned inputs from GitHub and keep a local cache.

Mitigation: Run examples only when GitHub access and workspace cache writes are acceptable; use an existing verified cache when offline.

Risk: Optional link probes write temporary files in inspected paths.

Mitigation: Explicitly authorize probe targets before enabling write-capable path probes.

## Reference(s):

- [Installation routes](references/installation.md)
- [Capabilities and public-version limits](references/capabilities.md)
- [Live state, sensors, and bounded monitoring](references/live-state-and-monitoring.md)
- [Decision flow details](references/decisions.md)
- [Public example inputs](references/public-inputs.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON reports, Guidance]

**Output Format:** [Markdown summaries with JSON field references; optional saved JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports distinguish missing or stale evidence from confirmed results and include collection context.]

## Skill Version(s):

0.3.5 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
