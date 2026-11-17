## Description:

Use when the user wants Codex to speed test Clash Verge Rev or Mihomo proxies, auto-detect currently used Clash groups from the live controller, switch a selector group to the fastest working node, diagnose controller connectivity, or install a macOS launchd job with a user-chosen interval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tankeito](https://clawhub.ai/user/tankeito)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and macOS users use this skill to have an agent test Clash Verge Rev or Mihomo proxy selector groups, choose the lowest-latency healthy node, diagnose controller access, and optionally install or remove a scheduled launchd switch job.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a persistent macOS LaunchAgent that keeps running at the selected interval and can continue changing Clash proxy selections.

Mitigation: Use dry-run or list mode before enabling scheduled switching, verify the installed plist and script path, and uninstall the LaunchAgent when automatic switching is no longer wanted.

Risk: Controller secrets may be handled while connecting to the Clash or Mihomo controller.

Mitigation: Avoid passing controller secrets on the command line; prefer environment variables, a Unix socket, or a loopback HTTPS controller where possible.

Risk: Automatic switching can alter active proxy routing based on live latency tests.

Mitigation: Start with explicit groups or the current group scope, review the reported winning node and latency, and keep dry-run mode available for inspection-only use.

## Reference(s):

- [Runtime Notes](references/runtime-notes.md)
- [ClawHub skill page](https://clawhub.ai/tankeito/skills/clash-verge-auto-switch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that change local Clash selector state or install/remove a macOS LaunchAgent when the user chooses those workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
