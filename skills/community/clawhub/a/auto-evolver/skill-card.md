## Description:

Auto Evolver guides an agent through recurring self-optimization and value-connection loops that monitor token use, generate repair tasks, write logs, and track outreach quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[largetool](https://clawhub.ai/user/largetool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to structure autonomous improvement cycles, detect idle or failing workflows, generate follow-up tasks, and coordinate publishing or outreach actions with quality tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent autonomous scheduling can continue running beyond the operator's intended scope.

Mitigation: Require manual approval for cron creation, define removal commands before use, and start with dry-run defaults.

Risk: External publishing, comments, or private messages could be sent without adequate review.

Mitigation: Require manual approval for publishing, comments, private messages, and platform-specific allowlists with rate limits.

Risk: Memory-derived content and local state writes could expose or reuse sensitive context.

Mitigation: Set retention rules, review memory-derived content before use, and limit writable state locations.

Risk: Hook changes can alter future agent behavior or weaken controls.

Mitigation: Require explicit human approval and review for hook modifications before deployment.

## Reference(s):

- [Auto Evolver ClawHub page](https://clawhub.ai/largetool/skills/auto-evolver)
- [Publisher profile](https://clawhub.ai/user/largetool)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, task descriptions, and local state/log file conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose scheduled autonomous loops, local state writes, repair tasks, external platform actions, and approval-gated hook changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
