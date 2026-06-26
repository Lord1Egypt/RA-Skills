## Description: <br>
Delegate work from an OpenClaw Discord controller bot to a Claude Code worker bot through a private Discord worker lane, then relay the final result back to the original DM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jini92](https://clawhub.ai/user/jini92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up, operate, test, and debug a Discord-based controller-to-worker flow where a Claude Code worker bot completes delegated work and relays the final answer back to the original DM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord DM requests and worker results may expose sensitive content to worker bot operators or Discord retention behavior. <br>
Mitigation: Use a dedicated private worker lane, restrict membership to intended bots and operators, and avoid sending sensitive DM content unless that exposure is acceptable. <br>
Risk: Overbroad worker-side bot exceptions could allow unintended bot-authored messages into the worker flow. <br>
Mitigation: Allowlist exact controller bot and channel IDs, require a canonical task prefix such as [WORKER_TASK], and keep the default bot guard in place for all other messages. <br>
Risk: A lane response without relay-back to the original DM is only partial success. <br>
Mitigation: Verify the full closed loop from controller DM to worker lane to Claude Code worker and back to the original controller DM. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/jini92/discord-claude-code-delegation) <br>
- [Current contract](references/current-contract.md) <br>
- [Operations](references/operations.md) <br>
- [Debug map](references/debug-map.md) <br>
- [Architecture](references/architecture.md) <br>
- [Example envelopes](examples/envelopes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown] <br>
**Output Format:** [Markdown with structured text envelopes and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on Discord worker-lane setup, operational checks, debugging paths, and relay-back guardrails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
