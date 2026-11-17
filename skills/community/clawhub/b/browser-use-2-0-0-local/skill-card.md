## Description:

Automates browser interactions for web testing, form filling, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wings229](https://clawhub.ai/user/wings229)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, page inspection, form entry, screenshots, data extraction, and browser session management for web testing and operational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using real Chrome profiles can expose logged-in sessions, cookies, and account data to browser automation.

Mitigation: Use a dedicated low-privilege browser profile and avoid personal or sensitive logged-in accounts.

Risk: The skill can execute Python in a persistent browser session.

Mitigation: Run Python only from trusted instructions and review code before execution.

Risk: Cloud browser, profile sync, cookie export, and tunnel commands can transfer browser data or expose local ports.

Mitigation: Enable these features only when explicitly intended, and stop tunnels or cloud sessions after use.

## Reference(s):

- [browser-use skill CLI README](https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and structured command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return browser state, page text, screenshots, cookies, command results, or JSON when the CLI is invoked with JSON output.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact _meta.json reports browser-use version 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
