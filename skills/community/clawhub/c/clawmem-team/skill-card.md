## Description:

Single entry skill for ClawMem Team workflows. Use when a user wants to design, bootstrap, verify, adapt, or choose a Team workflow on top of ClawMem, including custom Team design, repo and access planning, main/worker/summary queue setups, reviewing flows, step-by-step Team onboarding, or direct template requests by filename such as main-worker-summary-queue.md and reviewing.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericzequan](https://clawhub.ai/user/ericzequan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team leads use this skill to design, bootstrap, and verify ClawMem-based multi-agent Team workflows, including queue-based worker routing and review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mutable shared ClawMem memory node can become the team's authoritative operating contract.

Mitigation: Limit who can edit the contract, review contract changes before workers use them, and keep critical rules in task bodies as defensive inline context.

Risk: Workers may act without explicitly fetching the canonical Team contract, or completed tasks may remain visible in the queue.

Mitigation: Verify an explicit memory_get or issue_get before worker action, require the terminal status label and state:closed in the same completion step, and use state:open polling filters.

Risk: Multi-agent readiness can be overstated if only configuration or orchestrator-authored proxy activity is observed.

Mitigation: Require a real worker handoff or repo-mediated pickup before reporting ready; otherwise report partial or blocked with repair steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericzequan/skills/clawmem-team)
- [Team Blueprint Reference](references/blueprint.md)
- [Bootstrap Reference](references/bootstrap.md)
- [Communication Reference](references/communication.md)
- [Verification Reference](references/verification.md)
- [Main Worker Summary Queue Template](references/templates/main-worker-summary-queue.md)
- [Reviewing Template](references/templates/reviewing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown responses with workflow blueprints, label schemas, bootstrap plans, verification results, and optional task templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ClawMem label schemas, contract references, and concrete next-step plans.]

## Skill Version(s):

0.3.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
