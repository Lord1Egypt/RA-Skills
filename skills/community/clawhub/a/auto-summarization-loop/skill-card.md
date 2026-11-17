## Description:

Auto Summarization Loop helps agents manage long conversations by keeping core memory, recent working memory, and compressed long-term summaries with soft and hard token-watermark triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoujj8009](https://clawhub.ai/user/zhoujj8009)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add automatic context management to long-running AI conversations. It is especially relevant when an application needs to reduce context cost, avoid context overflow, and preserve user facts or pending tasks across turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses conversation summaries and user profile facts, which can include personal or sensitive data.

Mitigation: Require opt-in memory, clear retention and deletion controls, and redaction for sensitive data before production use.

Risk: Generated summaries or profile fields may be inaccurate or unsafe if reused directly in privileged prompts.

Mitigation: Validate summarizer output and avoid placing untrusted summaries or profile fields in system-role prompts without review.

## Reference(s):

- [Summary prompt templates](artifact/references/summary_prompts.md)
- [ClawHub skill page](https://clawhub.ai/zhoujj8009/skills/auto-summarization-loop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON-oriented summary templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompt-building guidance, memory configuration examples, and structured summary formats for long-conversation agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
