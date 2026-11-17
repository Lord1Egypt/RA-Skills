## Description:

Give isolated sessions such as cron jobs, sub-agents, and event handlers conversation context from a main session using sessions_history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rgba-research](https://clawhub.ai/user/rgba-research)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure isolated background agents that first retrieve main-session history, then produce reports, summaries, or delegated work with relevant conversation context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated agents may retrieve broad private session history or memory content.

Mitigation: Limit sessions_history to the smallest useful scope and redact sensitive session or memory content before using it in delegated tasks.

Risk: Examples include external delivery patterns that could send private context to unintended recipients.

Mitigation: Use explicit source and destination choices, replace every hard-coded account identifier, and verify all recipients and integrations before enabling scheduled delivery.

Risk: Scheduled background execution can repeat risky context sharing without an interactive review step.

Mitigation: Review cron payloads carefully before installation and avoid scheduled external delivery unless the destination and integration are verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rgba-research/skills/context-aware-delegation)
- [Source Homepage](https://gitlab.com/rgba_research/context-aware-delegation)
- [Publisher Website](https://rgbaresearch.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples depend on sessions_list and sessions_history tool access.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
