## Description:

Turn a pile of household donation items into sorted bundles, labels, packing steps, and a drop-off checklist without giving tax valuation or tax advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to sort household donation items by condition, destination type, packing needs, and drop-off logistics. It produces practical labels, checklists, and verification reminders while excluding tax valuation and tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could treat destination-type suggestions as confirmation that a specific organization accepts an item.

Mitigation: Tell users to verify current acceptance rules, hours, pickup limits, and item restrictions before loading items.

Risk: Users may ask for tax values, deductibility guidance, or appraisal methods outside the skill's logistics scope.

Mitigation: Do not estimate values or provide tax advice; offer a non-valued inventory and direct tax questions to official guidance, a qualified tax professional, or the donation organization's receipt policy.

Risk: Donated or recycled electronics may retain personal data.

Mitigation: Remind users to remove personal data from devices before donation or recycling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/donation-dropoff-planner)
- [Acceptance Tests](artifact/ACCEPTANCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Checklist]

**Output Format:** [Markdown structured donation plan with sorted item groups, bag or box labels, packing checklist, drop-off plan, verify-first list, and tax-boundary note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, network access, APIs, credentials, or file automation required.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
