## Description:

Collect fresh cross-source recommendation candidates for cspr using profile memory, feeds, search, Agent-Reach, and optional subagents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happywalkers](https://clawhub.ai/user/happywalkers)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run daily, weekly, or monthly source-discovery passes that turn profile memory, feeds, search, Agent-Reach routes, and optional subagent outputs into fresh recommendation candidates for cspr.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile- and history-derived interests may be sent to many external discovery services without clear per-provider approval.

Mitigation: Review before installing, disable routes or authenticated tools that should not be associated with user accounts, and run only when the user is comfortable with inferred interests being searched across third-party platforms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happywalkers/skills/cspr-source-scout)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSONL candidate files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces run artifacts such as source reports, route-attempt logs, candidate JSONL, blocker notes, and validation results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
