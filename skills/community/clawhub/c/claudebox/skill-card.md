## Description:

Install, configure, or run Claude Code through the claudebox wrapper, or connect to its HTTP, MCP, Telegram, or cron surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Claudebox to run Claude Code interactively or from scripts, and to connect it to HTTP, OpenAI-compatible, MCP, Telegram, or scheduled-job workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious because setup guidance pipes a remote installer into Bash and the default wrapper grants host Docker access.

Mitigation: Inspect and pin the installer to a reviewed version before running it; isolate the container and avoid using the default wrapper for untrusted prompts.

Risk: API and MCP endpoints have no authentication when their respective tokens are unset.

Mitigation: Set separate API and MCP tokens, and bind to loopback or use an authenticating proxy before exposing either endpoint beyond localhost.

## Reference(s):

- [Setup guide](references/setup.md)
- [Claudebox project](https://github.com/psyb0t/docker-claudebox)
- [API mode documentation](https://github.com/psyb0t/docker-claudebox/blob/master/docs/modes/api.md)
- [MCP mode documentation](https://github.com/psyb0t/docker-claudebox/blob/master/docs/modes/mcp.md)
- [Telegram mode documentation](https://github.com/psyb0t/docker-claudebox/blob/master/docs/modes/telegram.md)
- [Cron mode documentation](https://github.com/psyb0t/docker-claudebox/blob/master/docs/modes/cron.md)
- [ClawHub release page](https://clawhub.ai/psyb0t/skills/claudebox)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with shell commands and JSON/YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.8.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
