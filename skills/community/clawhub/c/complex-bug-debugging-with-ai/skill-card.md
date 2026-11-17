## Description:

Guides agents and human operators through a disciplined seven-stage workflow for investigating complex, intermittent, multi-system bugs with structured evidence, decision gates, validation, and knowledge capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when a bug is hard to reproduce, spans multiple services or systems, has contradictory symptoms, or has resisted ordinary debugging. It structures collaboration between the agent and operator so each conclusion is evidence-backed, production-impacting choices stay with the human operator, and fixes are verified before being documented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may require operational access to production-adjacent systems during debugging.

Mitigation: Approve production changes explicitly and limit DB, SSH, Kubernetes, log, and network access to the incident scope.

Risk: Generated debugging notes or BUGxx.md files may contain sensitive logs, infrastructure details, or customer data.

Mitigation: Review generated documentation for sensitive data before retaining or sharing it.

Risk: The artifact includes strong model and tooling recommendations that may be too prescriptive for some environments.

Mitigation: Treat the model requirement as advice and require each conclusion to be supported by current evidence.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with structured questions, decision tables, command plans, validation tables, and optional BUGxx.md documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces workflow guidance and operator-facing templates; it does not contain hidden execution or exfiltration behavior according to the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
