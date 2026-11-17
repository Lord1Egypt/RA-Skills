## Description:

Agent Token Usage summarizes per-agent LLM token consumption for OpenClaw by reading canonical assistant message usage records from session JSONL logs and optionally installing a Control UI button for daily summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolstar](https://clawhub.ai/user/symbolstar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect daily OpenClaw agent token usage, rank agents by input, output, cache read, cache write, total, and billable-equivalent tokens, and optionally expose the same summary in the local Control UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional UI installer patches discovered OpenClaw Control UI bundles and can add a macOS LaunchAgent that refreshes local data every five minutes.

Mitigation: Use the CLI-only path when a token summary is sufficient; review apply-ui.sh before running it and use remove-ui.sh to restore patched UI assets and remove the scheduled job.

Risk: The UI path publishes local agent token data into the Control UI data directory and renders agent-provided fields in a browser modal.

Mitigation: Avoid the UI patch in shared or untrusted local environments until the rendered fields are escaped or rebuilt with DOM text APIs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/symbolstar/skills/agent-token-usage)
- [Header button screenshot](https://raw.githubusercontent.com/SymbolStar/echoCue/main/docs/agent-token-usage/header-button.png)
- [Modal screenshot](https://raw.githubusercontent.com/SymbolStar/echoCue/main/docs/agent-token-usage/modal.png)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands plus optional CLI text or JSON token-usage summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can return ranked text tables or JSON records for a selected date and timezone.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
