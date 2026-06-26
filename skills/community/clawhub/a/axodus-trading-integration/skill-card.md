## Description: <br>
Integrate trading infrastructure (hummingbot/MCP) with paper-first mode and audit logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate hummingbot or MCP Axodus Trading infrastructure with paper-first execution, audit logging, risk limits, and validation before any live trading mode is enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Malformed trigger metadata may prevent reliable automatic activation. <br>
Mitigation: Review and fix trigger metadata before relying on automatic invocation. <br>
Risk: Live trading can create financial loss if real accounts are connected before validation. <br>
Mitigation: Keep paper mode as the default and require paper-mode tests, explicit live-mode confirmation, passing preflight checks, and configured risk limits before connecting real accounts. <br>
Risk: Exchange API keys or other secrets could be exposed if handled insecurely. <br>
Mitigation: Use secure secret storage and do not print, commit, or store exchange API keys in plaintext. <br>
Risk: Trading outputs could be misread as profit guarantees. <br>
Mitigation: Avoid guaranteed-profit claims and present trading systems as controlled-risk, experimental workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mzfshark/axodus-trading-integration) <br>
- [trading-integration.md](artifact/trading-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with configuration contracts and validation runbooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve paper-mode defaults, explicit live-mode confirmation, risk controls, audit logging, and secret-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, skill.yml, and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
