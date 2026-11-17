## Description:

Governed loop with roadmap, budget, ledger, and understanding debt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modeyapu](https://clawhub.ai/user/modeyapu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run bounded repository development rounds that leave durable state, verification results, and a single continuation decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commit-required, push-required, hook, or multi-agent split-write modes can expand the authority or write scope of a development round.

Mitigation: Review the repository policy before enabling those modes and require explicit human review when authority boundaries are unclear.

Risk: Continuity files written outside the intended repository can make later rounds follow stale or irrelevant state.

Mitigation: Keep continuity files inside the intended repository or a supervisor-owned state surface and reuse existing repo-native state when available.

Risk: Continuing after failed verification or unclear review gates can preserve an unsafe continuation decision.

Mitigation: Stop for human review when verification fails, review gates are due, or continuation evidence conflicts.

## Reference(s):

- [Continuous Dev Loop on ClawHub](https://clawhub.ai/modeyapu/skills/continuous-dev-loop)
- [Footer Contract](references/footer-contract.md)
- [Runtime Compatibility](references/runtime-compatibility.md)
- [Multi-Agent Governance](references/multi-agent-governance.md)
- [Stop Governance](references/stop-governance.md)
- [Precision Overview](references/precision-overview.md)
- [Repo Policy Profiles](references/repo-policy-profiles.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries, machine-readable footer text, and JSON or Markdown continuity files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write bounded repository state and review metadata such as loop state, ledgers, profile settings, metrics, and review reports.]

## Skill Version(s):

6.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
