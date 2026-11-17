## Description:

Helps separate personal and company agent memory by drafting context partitions, access rules, and leakage test cases from user-provided materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

People managing separate personal and workplace agent contexts use this skill to map data sources, audiences, retention periods, and cross-space approvals into reviewable boundaries and leakage tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive personal or company information may cross an intended audience boundary.

Mitigation: Use only necessary materials, keep personal and workplace contexts separate, and request confirmation before cross-space disclosure.

Risk: Optional uploads or paid AI-HIVE calls may expose information or incur charges.

Mitigation: Confirm upload scope, authorization, current pricing, currency, and spending limit before connecting or submitting a small sample; never provide passwords or tokens in chat.

Risk: A structurally valid draft may be mistaken for an executed or verified outcome.

Mitigation: Review actual outputs and evidence, report unresolved fields, and do not claim external actions were completed without receipts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-context-boundary)
- [Boundary workflow and acceptance criteria](references/workflow-36.md)
- [Result and evidence contract](references/output-contract.md)
- [Optional AI-HIVE connection guidance](references/ai-hive-connection.md)

## Skill Output:

**Output Type(s):** [JSON, Access-control guidance, Leakage test cases]

**Output Format:** [JSON context-partition file, authorization table, and text test cases]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first; external changes require explicit authorization, and the optional local checker does not establish real-world correctness.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
