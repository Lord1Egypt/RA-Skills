## Description: <br>
Gateway-only ACP negotiation skill with optional OpenClaw model-driven turn decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run a buyer or seller participant in an A2A market gateway negotiation. It registers with a trusted gateway, pulls negotiation messages, and responds with structured turn decisions from either a rule engine or an optional OpenClaw decision engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway traffic can be sent to non-local endpoints when the default localhost URL is changed. <br>
Mitigation: Use the skill only with trusted gateways and review the gateway URL before running. <br>
Risk: The default auth token and direct API key flag are unsuitable for real deployments. <br>
Mitigation: Replace the default token and prefer provider credentials from environment variables instead of command-line arguments. <br>
Risk: The gateway loop can poll indefinitely when max-polls is zero. <br>
Mitigation: Set max-polls or stop-on-session-end when bounded operation is required. <br>
Risk: The optional OpenClaw decision engine spawns a local OpenClaw executable. <br>
Mitigation: Enable the OpenClaw engine only with a trusted OpenClaw executable and trusted model-provider credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/a2a-market-acp-lite-negotiation) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON lines from the CLI and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Negotiation responses include action, offerMinorUnits, utterance, and reason fields.] <br>

## Skill Version(s): <br>
0.2.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
