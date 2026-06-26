## Description: <br>
Risk-aware support response governance for customer-facing automation that uses persona-weighted consensus, detects legal, sensitive-data, and confidentiality issues, applies hard-block policy checks, and writes auditable decision artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and support automation teams use this skill to review human- or agent-authored customer support replies before sending, especially for billing, escalation, regulated, or enterprise support workflows. It returns allow, block, or rewrite decisions and records auditable decision artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: In external_agent mode, caller-supplied votes may drive decisions without local rechecking of risky draft text. <br>
Mitigation: Require local hard-block checks on every draft and validate any external votes before using the decision in automated support workflows. <br>
Risk: Decision artifacts may contain customer support content in the configured consensus state path. <br>
Mitigation: Protect CONSENSUS_STATE_FILE or CONSENSUS_STATE_ROOT with appropriate filesystem permissions, retention controls, and review before production use. <br>


## Reference(s): <br>
- [Consensus Guard Core npm package](https://www.npmjs.com/package/consensus-guard-core) <br>
- [Consensus Guard Core repository](https://github.com/kaicianflone/consensus-guard-core) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Guidance] <br>
**Output Format:** [JSON decision response with optional rewrite patch and filesystem audit artifact JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node >=18, tsx, and a configured consensus state path through CONSENSUS_STATE_FILE or CONSENSUS_STATE_ROOT.] <br>

## Skill Version(s): <br>
1.1.15 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
