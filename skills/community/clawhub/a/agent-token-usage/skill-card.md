## Description: <br>
Summarizes daily per-agent LLM token consumption for OpenClaw multi-agent setups from local session JSONL logs and can optionally add a token-usage button to the OpenClaw Control UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[symbolstar](https://clawhub.ai/user/symbolstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw multi-agent environments use this skill to review daily token usage by agent, including input, output, cache read, cache write, total, and estimated billable-equivalent tokens. It is also useful when they want an optional local Control UI button for the same report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional UI installer modifies the local OpenClaw Control UI bundle and, on macOS, installs a LaunchAgent that refreshes token data every five minutes. <br>
Mitigation: Use the CLI-only path when UI integration is not needed; run apply-ui.sh only after reviewing the change, and use remove-ui.sh to restore the UI bundle and remove the background job. <br>
Risk: Token usage reports are derived from local OpenClaw session logs and may reveal agent activity patterns if exported or shared. <br>
Mitigation: Review generated tables or JSON before sharing and keep the Control UI data file local unless disclosure is intended. <br>


## Reference(s): <br>
- [Agent Token Usage on ClawHub](https://clawhub.ai/symbolstar/skills/agent-token-usage) <br>
- [Control UI header button screenshot](https://raw.githubusercontent.com/SymbolStar/echoCue/main/docs/agent-token-usage/header-button.png) <br>
- [Per-agent token breakdown modal screenshot](https://raw.githubusercontent.com/SymbolStar/echoCue/main/docs/agent-token-usage/modal.png) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, tabular text, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can emit a ranked table or JSON for a selected date and timezone; the optional UI writes same-origin JSON for the local Control UI.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
