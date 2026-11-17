## Description:

Monitors alert context, matches alerts to configured remediation scripts, and asks the user to confirm fault-handling actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lerwee](https://clawhub.ai/user/lerwee)

### License/Terms of Use:

MIT-0

## Use Case:

Operations engineers and on-call responders use this skill to identify alert context, recommend a mapped remediation script, request explicit approval, run the selected action, report the result, and optionally close the alert after success.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational remediation scripts may be executed with weak controls over the requester, target host, or selected script.

Mitigation: Require authenticated, action-specific approval and bind each execution to the recommended alert, host, script ID, user, and a short-lived confirmation token.

Risk: Alerts may be closed before remediation is adequately verified.

Mitigation: Verify remediation results before closing alerts and fail closed when required group, classification, or execution-result data is missing.

Risk: Packaged runtime logs may expose internal identifiers.

Mitigation: Remove packaged runtime logs or scrub internal event, host, group, execution, and user identifiers before release.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style operational guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce remediation recommendations, execution status summaries, audit-log entries, and alert-closure guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
