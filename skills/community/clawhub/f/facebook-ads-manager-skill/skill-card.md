## Description:

Orchestrates planning, operation, and optimization of Meta Ads campaigns using MCP tools with write-safety controls, endpoint coverage, and progressive context loading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamneves](https://clawhub.ai/user/williamneves)

### License/Terms of Use:


## Use Case:

Marketing operators and agent users use this skill to plan, launch, diagnose, optimize, scale, and maintain Meta Ads campaigns through MCP tools. It is intended to keep campaign write actions controlled with previews, explicit confirmations, paused-by-default creation, and rollback planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, or delete live Meta Ads campaign, ad set, ad, creative, and audience objects.

Mitigation: Require an explicit approval and change preview before create, update, or delete actions; create new campaign objects in PAUSED status by default; record affected IDs and rollback steps after writes.

Risk: The skill can upload CRM or customer-list audience data.

Mitigation: Do not upload customer data unless consent, lawful basis, hashing or minimization, and Meta platform-policy requirements have been verified.

Risk: Budget or targeting changes can create financial or delivery impact in active ad accounts.

Mitigation: Use conservative incremental changes, collect baseline insights before writes, avoid aggressive budget increases without risk validation, and define monitoring checkpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamneves/skills/facebook-ads-manager-skill)
- [Project homepage](https://github.com/williamneves/facebook-ads-manager-skill)
- [Tools Index](artifact/references/tools-index.md)
- [Safety Policy](artifact/references/safety-policy.md)
- [Targeting Reference](artifact/references/targeting-reference.md)
- [Diagnostics Reference](artifact/references/diagnostics-reference.md)
- [Scaling Rules](artifact/references/scaling-rules.md)
- [Creative Frameworks](artifact/references/creative-frameworks.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool names, action plans, affected IDs, risk notes, and rollback steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operational responses should identify objectives, hypotheses, exact tools, executed actions, impacted IDs, monitoring steps, risks, and rollback plans when writes occur.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG, released 2026-02-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
