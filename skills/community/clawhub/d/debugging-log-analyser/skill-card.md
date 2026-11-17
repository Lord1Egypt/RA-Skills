## Description:

Parses error logs, stack traces, and crash reports into a structured root cause diagnosis with classification, stack trace analysis, confidence, affected path, code-level fix suggestions, and ordered debugging steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn application errors, stack traces, and crash reports into a structured debugging report with likely root cause, affected code path, concrete fixes, and next diagnostic steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logs and crash reports can contain API keys, tokens, passwords, customer data, internal hostnames, or other sensitive production details.

Mitigation: Provide minimized excerpts and redact sensitive values before sharing logs with the skill.

Risk: Suggested fixes and debugging commands may be incorrect or incomplete when the input log lacks full context.

Mitigation: Review proposed changes, commands, and root cause confidence before applying them to production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/debugging-log-analyser)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/debugging-log-analyser.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown debugging report with optional code snippets and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes error classification, stack trace walkthrough, root cause confidence, suggested fix, next debugging steps, and prevention guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
