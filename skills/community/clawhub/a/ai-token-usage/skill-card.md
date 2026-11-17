## Description:

AI Token消耗监控 reads local QClaw session logs to summarize token usage, detect abnormal consumption, and provide cost-optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to review AI token consumption from local session logs, identify unusual usage patterns, and produce concise optimization guidance before costs become excessive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local QClaw session logs may contain sensitive conversation history.

Mitigation: Install and run the skill only where reading local session logs is acceptable, and review access expectations with users before deployment.

Risk: Generated token usage summaries persist under workspace memory until deleted.

Mitigation: Apply the same retention and deletion practices to generated usage summaries as to other workspace data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/ai-token-usage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and text reports from the token statistics script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local QClaw session logs and may write derived token usage summaries under workspace memory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
