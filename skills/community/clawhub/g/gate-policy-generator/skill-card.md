## Description:

Generates a policy-as-code configuration that sorts agent tools into allowed, review-required, and blocked tiers, with gates for overreach, accidental deletion or sending, and runaway loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to draft permission policies that define which tools an agent may use, which require review, and which are blocked. It also produces checks for the policy's gates and resource budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator's checks may miss conflicting permissions, and deployment scope may be too broad.

Mitigation: Generate drafts in a restricted project directory, choose paths carefully, avoid symlinks and unintended overwrites, and independently review permission conflicts and budgets.

Risk: A passing policy check does not establish that the policy is enforced by the target runtime.

Mitigation: Require explicit approval of the target environment and permission changes, verify effective permissions after deployment, and have a tested recovery plan.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/gate-policy-generator)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory repository](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)
- [UIBC protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)

## Skill Output:

**Output Type(s):** [Configuration, JSON, Text]

**Output Format:** [JSON policy configuration and policy-check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Policy files include tool tiers, four gates, and loop and token budgets. Review policy conflicts and verify enforcement in the target runtime before relying on a generated policy.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
