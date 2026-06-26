## Description: <br>
Agent Passport adds consent-gated mandates, audit trails, and security checks for sensitive agent actions such as shell commands, communications, data changes, external API calls, financial actions, and identity actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markneville](https://clawhub.ai/user/markneville) <br>

### License/Terms of Use: <br>
MIT with Commons Clause <br>


## Use Case: <br>
Developers and agent operators use Agent Passport to require explicit, scoped mandates before agents perform sensitive actions and to maintain local audit trails with optional threat-definition updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Pro mode can make periodic HTTPS requests to api.agentpassportai.com for license checks and threat-definition updates. <br>
Mitigation: Keep the skill in free/offline mode unless vendor network calls are acceptable, and set AGENT_PASSPORT_LICENSE_KEY only when Pro updates are needed. <br>
Risk: Broad templates such as full-auto can authorize large action scopes for an agent. <br>
Mitigation: Prefer narrow templates, short TTLs, spending caps, rate limits, and allowlists before granting broad mandates. <br>


## Reference(s): <br>
- [Agent Passport ClawHub Page](https://clawhub.ai/markneville/agent-passport) <br>
- [Agent Passport Mandate Reference](references/mandates.md) <br>
- [Agent Passport Pro](https://agentpassportai.com/pro/) <br>
- [Agent Bridge](https://agentbridge.dev) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON ledger/check outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local shell tools jq, bc, xxd, head, date, and mkdir; uses AGENT_PASSPORT_LEDGER_DIR for ledger storage.] <br>

## Skill Version(s): <br>
2.4.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
