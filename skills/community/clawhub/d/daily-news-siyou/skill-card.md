## Description:

Daily News Skill fetches recent news for configured categories and prepares scheduled text or voice news broadcasts through Feishu and NoizAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anightmare2](https://clawhub.ai/user/anightmare2)

### License/Terms of Use:

MIT

## Use Case:

Individuals or teams use this skill to create category-based daily news briefings and send text or voice updates to a Feishu chat on a schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script is reported as unsafe because a configurable news limit can become local command execution.

Mitigation: Review before installing and avoid running it until the news limit is validated and passed to Python as data rather than source code.

Risk: Scheduled runs can automatically send messages to a Feishu chat using stored credentials.

Mitigation: Run only under a low-privilege account, do not run cron as root, narrowly scope the Feishu app, protect configuration files, and confirm the destination chat.

Risk: The skill depends on Feishu, NoizAI, and Tavily credentials.

Mitigation: Store credentials in protected secret storage and restrict access to users and automation that need to run the broadcaster.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anightmare2/skills/daily-news-siyou)
- [Tavily search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash examples; runtime output is terminal text and optional Feishu voice broadcast.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu, NoizAI, and optionally Tavily credentials; scheduled operation can be configured with cron.]

## Skill Version(s):

1.1.0 (source: server release evidence and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
