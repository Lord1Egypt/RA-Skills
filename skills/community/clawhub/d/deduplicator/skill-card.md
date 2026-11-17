## Description:

Deduplicator filters duplicate content and links within a conversation session, skipping repeated list items such as search results or profile entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiiang0529](https://clawhub.ai/user/xiiang0529)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Deduplicator to keep session-scoped lists, search results, profile entries, and links unique by skipping items that were already seen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically omit an item it identifies as duplicate during list-processing tasks.

Mitigation: Use the documented reset command before starting a new list or when duplicate tracking should no longer apply.

Risk: Default duplicate and reset messages are in Chinese, which may be unclear in an English-only workflow.

Mitigation: Confirm the expected user-facing language before deployment and adapt duplicate notices where the runtime allows.

## Reference(s):

- [Deduplicator ClawHub skill page](https://clawhub.ai/xiiang0529/skills/deduplicator)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown or plain text duplicate-filtering responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session-scoped duplicate tracking with duplicate content and duplicate link notices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
