## Description:

Monitors and stages Douyin creator comments, then helps classify, review, and reply to them through a two-phase fetch and process workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators or account operators use this skill to collect recent Douyin comments, stage them as JSON, generate moderation and reply decisions, apply status updates, and prepare concise public replies through a logged-in creator account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act through a logged-in Douyin creator account and prepare public replies.

Mitigation: Use a dedicated creator account, require manual approval before posting replies, and audit generated reply text before execution.

Risk: The skill stores comment data in a fixed personal vault path and writes local state and logs.

Mitigation: Run with constrained filesystem access and update storage paths to an approved, isolated workspace before use.

Risk: Model-produced moderation and reply decisions have weak validation.

Mitigation: Validate the LLM JSON action schema, route uncertain comments to manual review, and test moderation rules with representative comments before unattended operation.

Risk: State-validation and retry logic are incomplete or unsafe according to the security evidence.

Mitigation: Correct and test state transitions, retry counters, and failure handling before enabling automatic reply workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/skills/douyin-comment-reply)
- [Douyin Creator Center](https://creator.douyin.com/)
- [Douyin creator content management](https://creator.douyin.com/creator-micro/content/manage)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and Python command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged comment JSON, status summaries, LLM prompt text, moderation actions, reply text, and local Markdown comment logs.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
