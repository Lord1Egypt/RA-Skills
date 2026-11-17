## Description:

Automates browser interactions for web testing, form filling, screenshots, and data extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tang2606](https://clawhub.ai/user/tang2606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to drive browser-based workflows such as navigation, web testing, form filling, screenshots, authenticated browsing, and page data extraction through the browser-use CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access authenticated browser profiles, cookies, and real browsing sessions.

Mitigation: Use an isolated browser profile for skill activity and avoid personal default profiles unless the task explicitly requires them.

Risk: Cookie export, cookie import, and profile sync commands can expose sensitive session data.

Mitigation: Export or sync cookies and profiles only when necessary, store resulting files carefully, and delete them after use.

Risk: Tunnel commands can expose local development services to the public internet.

Mitigation: Start tunnels only for intended services, verify what is listening on the port, and stop tunnels when the task is complete.

Risk: Cloud browser and API commands can involve account credentials or API keys.

Mitigation: Prefer environment variables or secure secret handling for API keys and avoid placing credentials directly in prompts or command histories.

Risk: The browser-use Python command can execute arbitrary Python in a persistent session.

Mitigation: Review Python snippets before execution and limit them to the minimum code needed for the browser task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tang2606/skills/browser-use-conflict)
- [browser-use CLI README](https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct creation of screenshots, cookie JSON exports, tunnel URLs, and browser session state through the browser-use CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact/_meta.json reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
