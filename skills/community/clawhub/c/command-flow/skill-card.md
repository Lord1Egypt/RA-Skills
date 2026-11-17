## Description:

Command Flow helps agents present OpenClaw slash commands with Chinese explanations, source grouping, searchable command listings, safety labels, and confirmation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[largetool](https://clawhub.ai/user/largetool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OpenClaw users can use this skill to browse, search, explain, export, and launch slash-command workflows without memorizing command names. It is most useful when an agent needs to expose a command catalog in conversational, dashboard-style, or Telegram inline formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Safety labels may mark sensitive OpenClaw command areas as safe.

Mitigation: Treat the dashboard as a command catalog and review sensitive reset, plugin, token/device, memory, message, scheduler, service, hook, and configuration commands before execution.

Risk: The command-generation helper shells out to the local openclaw binary and writes generated JavaScript.

Mitigation: Run the helper only when the openclaw binary on PATH is trusted, then manually review generated JavaScript before using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/largetool/skills/command-flow)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Chinese-language text dashboards, Markdown command exports, command strings, and Telegram inline keyboard JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq according to skill metadata; helper scripts may read local OpenClaw CLI help output to generate command catalog JavaScript.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
