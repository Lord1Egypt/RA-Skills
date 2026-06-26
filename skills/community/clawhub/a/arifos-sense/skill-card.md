## Description: <br>
Constitutional governance layer for arifOS that evaluates irreversible, high-stakes, externally consequential, identity-shaping, or constitutional-boundary actions and returns SEAL, CAUTION, HOLD, or VOID guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariffazil](https://clawhub.ai/user/ariffazil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to apply arifOS governance checks before consequential actions, pause for human review when required, and format verdicts with concise reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The governance layer may interrupt normal workflows by pausing high-stakes or uncertain actions. <br>
Mitigation: Review the trigger list and HOLD/VOID behavior before installation, and require explicit human approval before resuming paused actions. <br>
Risk: The audit ledger may retain local decision context for consequential actions. <br>
Mitigation: Review the VAULT999 ledger path and retention expectations before use in sensitive environments. <br>


## Reference(s): <br>
- [The 13 Constitutional Floors](references/floors.md) <br>
- [VAULT999 Immutable Audit Ledger Format](references/vault999-format.md) <br>
- [ClawHub skill page](https://clawhub.ai/ariffazil/arifos-sense) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files] <br>
**Output Format:** [Markdown verdict blocks and audit ledger entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause high-stakes actions with HOLD or VOID guidance and append local VAULT999 audit entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
