## Description:

Agent Phone Call gives an agent a phone number for outbound calls, incoming call answering, call summaries, balance checks, and inbound prompt updates through PollyReach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsz](https://clawhub.ai/user/mrsz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to make task-oriented outbound phone calls, answer incoming calls, retrieve call summaries and transcripts, and manage a PollyReach phone number.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone numbers, call transcripts, recordings, summaries, and caller details may be shared with PollyReach and surfaced in agent chat.

Mitigation: Use the skill only with explicit user awareness, avoid sensitive personal, financial, medical, legal, or confidential business calls, and confirm consent, notice, retention, and recording obligations before use.

Risk: The skill encourages publicizing the assigned phone number and scheduled polling, which can increase collection and reporting of incoming call data.

Mitigation: Enable scheduled polling and share the assigned number only when the user has clear control over what is recorded, summarized, and reported.

Risk: Call outcomes may be incomplete, delayed, or constrained by PollyReach balance and one-call-at-a-time behavior.

Mitigation: Check call results, balance, and failure details before treating a task as complete, and escalate decisions beyond the user's authorization back to the user.

## Reference(s):

- [Agent Phone Call on ClawHub](https://clawhub.ai/mrsz/skills/agent-phone-call)
- [Publisher profile](https://clawhub.ai/user/mrsz)
- [PollyReach homepage](https://pollyreach.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command usage and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local credential configuration and PollyReach API responses for activation, calls, inbound messages, prompt updates, and balance checks.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
