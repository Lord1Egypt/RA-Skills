## Description:

Coordinates authorized handoffs between phone and desktop tasks, turning selected screenshots, voice notes, and channel exports into reviewable results and status records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

People coordinating tasks across devices and messaging channels use this skill to prepare handoff packages, to-do lists, consolidated inboxes, and stop-or-recovery plans. External actions require suitable tools and explicit authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task materials or external tools may expose private information or credentials.

Mitigation: Confirm the official service domain and permitted upload scope; minimize or redact data and never include passwords, tokens, codes, cookies, or full identity documents.

Risk: Handoffs may trigger unauthorized sending, payments, deletion, or other external changes.

Mitigation: Require action-specific permission and the relevant device or app access before execution; otherwise provide a draft or manual handoff.

Risk: External model use may incur unexpected charges or be unavailable.

Mitigation: Check the actual tools, current price, currency, and spending limit; start with a small sample and do not claim completion without a verified result.

## Reference(s):

- [Product identity and source boundaries](artifact/references/scope-and-sources.md)
- [Screenshot and voice to-do workflow](artifact/references/workflow-13.md)
- [Phone-to-desktop handoff workflow](artifact/references/workflow-20.md)
- [Cross-channel inbox workflow](artifact/references/workflow-21.md)
- [Pause and recovery workflow](artifact/references/workflow-42.md)
- [Result and evidence contract](artifact/references/output-contract.md)
- [AI-HIVE connection and authorization](artifact/references/ai-hive-connection.md)

## Skill Output:

**Output Type(s):** [Text, JSON files, CSV files, Guidance]

**Output Format:** [Reviewable task records, handoff packages, lists, and written guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [External completion requires an actual tool result and reviewable evidence; otherwise the output remains a draft or handoff plan.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
