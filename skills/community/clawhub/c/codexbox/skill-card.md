## Description:

Install, configure, or run Codex through the codexbox wrapper, or connect to its HTTP, MCP, Telegram, or cron surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use codexbox to run Codex from a chosen workspace or connect it to scripts, MCP clients, Telegram, or scheduled jobs. The skill provides setup and configuration guidance for those workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial, and setup examples use mutable Docker image tags that can change after review.

Mitigation: Pin a reviewed image version or digest and review image changes before installing or updating.

Risk: When enabled without their own bearer tokens, reachable API or MCP surfaces can run prompts and access workspace files.

Mitigation: Set distinct API and MCP tokens for each enabled surface, and bind services to loopback or place them behind an authenticating proxy.

## Reference(s):

- [Project homepage](https://github.com/psyb0t/docker-codexbox)
- [ClawHub release page](https://clawhub.ai/psyb0t/skills/codexbox)
- [Setup guide](references/setup.md)
- [Codex CLI](https://github.com/openai/codex)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup guidance for wrapper, HTTP, MCP, Telegram, and cron workflows.]

## Skill Version(s):

0.7.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
