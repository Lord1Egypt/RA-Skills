## Description:

Analyze and diagnose common programming error messages and stack traces with root causes and fix suggestions for Python, Node.js, Go, Bash, and system errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to interpret error messages, stack traces, and logs, then get concise root-cause explanations and practical fix suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted log or error text could include terminal control characters that make output misleading in some terminals.

Mitigation: Review pasted or piped input from untrusted sources and avoid relying on terminal-rendered formatting alone.

Risk: Suggested commands may include privileged or system-changing operations such as sudo, service inspection, firewall checks, ownership changes, or permission changes.

Mitigation: Review every suggested command before running it and adapt placeholders to the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/debug-assistant)
- [MDN HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal text with diagnostic sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ANSI color formatting and command suggestions for manual review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
