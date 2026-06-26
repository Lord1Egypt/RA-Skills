## Description: <br>
Execute and track paper trades from TA setups with JSONL ledger, open/close workflow, and mark-to-market status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading workflow users use this skill to simulate TA-based order execution, record rationale, update mark-to-market status, and close paper positions without connecting to a live broker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paper-trade symbols, quantities, prices, and rationale notes are stored locally in the default JSONL ledger. <br>
Mitigation: Avoid putting secrets or sensitive strategy notes in trade rationale fields, and pass an explicit ledger path when tighter data separation is needed. <br>
Risk: Users may mistake simulated order tracking for live brokerage execution. <br>
Mitigation: Keep usage limited to paper-trading workflows and confirm that orders are recorded only in the local ledger before relying on any result. <br>


## Reference(s): <br>
- [Execution Policy](references/execution-policy.md) <br>
- [ClawHub skill page](https://clawhub.ai/1477009639zw-blip/beta-ta-paper-executor) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script output can be text or JSON; ledger records are JSONL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends simulated order events to a local ledger by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
