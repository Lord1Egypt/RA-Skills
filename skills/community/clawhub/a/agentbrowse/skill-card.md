## Description: <br>
Browser automation workflows through the agentbrowse CLI for launch, attach, observe, act, extract, navigation, and screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xor777](https://clawhub.ai/user/xor777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use AgentBrowse to control browser sessions for web tasks, including launching or attaching to a browser, inspecting visible page state, interacting with returned targets, navigating, extracting structured data, and capturing screenshots for evidence or recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-assisted observe goals and extract commands may send page content through the configured LLM gateway, including sensitive content if used on the wrong page. <br>
Mitigation: Use a dedicated API key, protect the local config file, and avoid AI-assisted observe or extract on pages containing credentials, payment details, or sensitive personal data unless that sharing is approved. <br>
Risk: Browser automation can reach login, identity, or payment steps where protected values or explicit approval are required. <br>
Mitigation: Stop at protected boundaries and switch to the appropriate protected-flow tool instead of entering secrets, personal data, or payment details through AgentBrowse. <br>
Risk: Browser sessions and target refs can become stale after redirects, reloads, dynamic updates, or reconnects. <br>
Mitigation: Re-run observe after meaningful page changes, use browser-status for diagnostics, and reconnect before acting when the current session is unreachable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xor777/agentbrowse) <br>
- [Publisher profile](https://clawhub.ai/user/xor777) <br>
- [AgentBrowse browser library and docs](https://github.com/MercuryoAI/agentbrowse) <br>
- [AgentBrowse marketplace documentation](https://github.com/MercuryoAI/skills/blob/main/docs/agentbrowse/openclaw/marketplace/README.md) <br>
- [Operating guide](references/workflow.md) <br>
- [Command guide](references/commands.md) <br>
- [Failure recovery](references/statuses.md) <br>
- [Boundaries and escalation](references/guardrails.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Conversational guidance with inline shell commands and optional JSON extraction schemas or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agentbrowse CLI on PATH; AI-assisted observe goals and extract commands require a configured API key.] <br>

## Skill Version(s): <br>
0.1.22 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
