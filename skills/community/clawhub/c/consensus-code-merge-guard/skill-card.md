## Description:

Persona-weighted merge governance for AI-assisted engineering. Evaluates PR risk (tests, security markers, reliability signals), returns MERGE/BLOCK/REVISE decisions, and records board-native audit artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill before merge automation to evaluate pull request and release-branch risk, including test status, security signals, rollback readiness, and reviewer or policy gates. It returns a policy-backed decision and records an auditable decision artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can approve and persist merge decisions without the existing persona governance that its documentation says is required.

Mitigation: Use the decision as advisory until missing persona sets fail closed before automated merges.

Risk: External votes and constraints can affect merge decisions if they are not strictly validated.

Mitigation: Validate external votes and constraints at the integration boundary and keep independent CI and security gates in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaicianflone/skills/consensus-code-merge-guard)
- [consensus-guard-core npm package](https://www.npmjs.com/package/consensus-guard-core)
- [consensus-guard-core repository](https://github.com/kaicianflone/consensus-guard-core)
- [consensus-tools repository](https://github.com/kaicianflone/consensus-tools)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [JSON decision response with an auditable decision artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records merge decisions under the configured consensus state path; no outbound network calls are described for the shipped guard decision path.]

## Skill Version(s):

1.1.15 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
