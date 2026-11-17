## Description:

Helps users pause agent activity, assess completed actions, and prepare an evidence-backed handoff and recovery plan without promising reversals that tools cannot perform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

People supervising an agent use this skill to document its last known state, stop pending actions where tools allow, identify impacts, and prepare a narrowly scoped recovery or human handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pausing or reversing an agent may require tools that are unavailable, and a sent action may not be reversible.

Mitigation: Check available pause, log, and reversal tools and actual receipts; otherwise deliver a draft handoff and state what could not be executed.

Risk: Connecting tools or uploading materials could expose sensitive data or incur unexpected charges.

Mitigation: Confirm discovered tools, upload scope, current pricing, and a budget cap; redact sensitive inputs and start with a small sample.

Risk: Sending, paying, deleting, posting, refunding, or modifying business systems without authorization could cause harm.

Mitigation: Require separate explicit approval for each external action; a recovery plan alone does not authorize execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-agent-stop-recovery)
- [Agent stop and recovery workflow](references/workflow-42.md)
- [Result and evidence contract](references/output-contract.md)
- [AI-HIVE connection guidance](references/ai-hive-connection.md)
- [AI-HIVE user portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON]

**Output Format:** [Reviewable stop record, impact list, and recovery recommendations; optional structured JSON or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records can include action, last_state, reversible, pause_receipt, recovery_option, and evidence references; unknown outcomes remain marked for review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
