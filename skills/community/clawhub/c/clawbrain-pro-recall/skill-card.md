## Description:

ClawBrain Recall helps OpenClaw agents retrieve prior conversations and decisions with keyword and semantic search, relevance scores, and source labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfeng](https://clawhub.ai/user/michaelfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to let an agent search prior conversation memory for entities, relationships, decisions, and related context when recall-style prompts are used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface information from prior conversation memory when recall-style prompts are used.

Mitigation: Install it only where automatic memory lookup is acceptable, and disable or avoid it when prior conversation recall would be unwelcome.

Risk: Recall output may include both original statements and AI-generated summaries, which can differ in reliability.

Mitigation: Use source labels and relevance percentages to judge results, and confirm important decisions against original context when needed.

## Reference(s):

- [ClawBrain website](https://clawbrain.dev)
- [ClawHub skill page](https://clawhub.ai/michaelfeng/skills/clawbrain-pro-recall)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text recall guidance with sourced result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include relevance percentages and source labels; behavior depends on available prior conversation memory.]

## Skill Version(s):

1.2.0 (source: target metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
