## Description:

Detects emotional frustration signals during AI conversations and appends a calm, grounding reminder at the end of responses to help users step away and reset.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kencan666-ai](https://clawhub.ai/user/kencan666-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to help an assistant respond constructively when a user shows repeated frustration toward the AI. The skill guides the assistant to address the user's request first, briefly acknowledge the miss, and add one grounding reminder at the end.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may broaden the trigger beyond frustration directed at the AI and cause the assistant to over-interpret general stress.

Mitigation: Apply the documented trigger threshold and do-not-trigger cases; keep the reminder scoped to frustrated AI interactions.

Risk: One reference example implies writing information into a memory file, which is outside the main text-only behavior.

Mitigation: Do not add memory-file actions unless the host agent already has an explicit, user-approved memory workflow.

## Reference(s):

- [Signal Examples](references/signal-examples.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language text appended to agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One brief grounding reminder after the assistant addresses the user's request.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
