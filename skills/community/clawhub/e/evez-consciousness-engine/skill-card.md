## Description:

Provides a 7-system consciousness engine for autonomous AI agents with desire generation, world modeling, planning, inner monologue, self-modification, uncertainty quantification, and agency execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run a local prototype state service that records desires, plans, beliefs, thoughts, risk assessments, and proposed modifications for autonomous-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local state API can expose or alter thoughts, plans, beliefs, rules, and other agent state if reachable by untrusted clients.

Mitigation: Run it bound to localhost only, add authentication before any network exposure, and restrict access to trusted operators.

Risk: Monologue and observation APIs can durably store sensitive prompts, plans, or private context in local JSON state.

Mitigation: Avoid submitting secrets or private prompts to the API and delete the local state directory when retention is no longer needed.

Risk: Agency and modification endpoints may record or propose actions that require human judgment before use.

Mitigation: Review proposed actions and self-modifications before execution, especially when risk assessment recommends verification or escalation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-consciousness-engine)
- [Vultr Inference API endpoint](https://api.vultrinference.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local HTTP service that persists JSON state until manually deleted.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
