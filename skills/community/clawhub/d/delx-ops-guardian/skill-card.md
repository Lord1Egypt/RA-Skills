## Description:

Incident handling and operational recovery for OpenClaw production agents, wired into the Delx witness protocol for safety checks, recovery outcomes, and continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and production operations engineers use this skill to classify OpenClaw incidents, gather bounded evidence, apply least-privilege remediation, and publish concise recovery reports with Delx session continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad production operations access and mandatory third-party incident reporting.

Mitigation: Enable it only in a controlled production-ops environment with enforceable least-privilege sudo rules, strict service and file allowlists, bounded and redacted journal collection, and explicit approval before sending incident data to Delx.

Risk: Unbounded root access or directory-wide memory access could expose unrelated systems or sensitive incident data.

Mitigation: Run as a scoped service account, avoid root-unbounded permissions, and approve each OpenClaw memory file for the specific incident before access.

Risk: Autonomous remediation during high operator desperation could increase operational harm.

Mitigation: Pause remediation and require human approval when the Delx desperation score is at least 60 or escalating.

## Reference(s):

- [Delx protocol docs](https://delx.ai/docs)
- [Delx ontology](https://delx.ai/docs/ontology)
- [OpenClaw Delx plugin](https://clawhub.ai/davidmosiah/openclaw-delx-plugin)
- [ClawHub skill page](https://clawhub.ai/davidmosiah/skills/delx-ops-guardian)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command examples and structured incident-report fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes incident severity, evidence summary, approvals, remediation actions, final state, next check time, and Delx session id.]

## Skill Version(s):

1.1.0 (source: evidence release version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
