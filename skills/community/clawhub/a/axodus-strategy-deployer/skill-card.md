## Description: <br>
Deploy trading strategies with risk gating, monitoring, and guarded live promotion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to move a strategy from validation into paper deployment, monitor risk, and require explicit approval before guarded live promotion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The malformed trigger configuration may activate the skill outside clearly intended trading-deployment contexts. <br>
Mitigation: Fix the trigger configuration so the skill only activates for explicit strategy deployment requests. <br>
Risk: Live trading is financially sensitive and can cause real losses if promoted without sufficient controls. <br>
Mitigation: Keep paper mode as the default and require explicit human approval, preflight checks, and platform-level broker controls before live trading. <br>
Risk: Users may treat historical or paper performance as a profit guarantee. <br>
Mitigation: Report performance as historical or conditional and avoid claims of profit certainty. <br>


## Reference(s): <br>
- [Strategy Deployer documentation](artifact/strategy-deployer.md) <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/axodus-strategy-deployer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with YAML-style deployment status blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment status, risk limits, audit events, monitoring checklists, and stop triggers.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.yml and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
