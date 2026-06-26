## Description: <br>
ClawGuard governance layer that must run before any SQL, file-system, or API write. Use evaluate_action(action_type, justification, risk_level) to log/authorize actions and get_audit_report(limit) to review the SQLite-based audit ledger. Blocks risk_level >= 4 automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mithileshgau](https://clawhub.ai/user/mithileshgau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use ClawGuard to log and authorize write-capable SQL, file-system, and API actions before execution, then inspect recent audit ledger entries for governance reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may rely on the skill as a guaranteed enforcement layer even when their environment does not force all write actions through it. <br>
Mitigation: Use it only where write-capable SQL, file-system, and API operations are routed through evaluate_action before execution. <br>
Risk: Redis-based throttling and the Civic verification message may surprise operators because they are not clearly disclosed in the skill documentation. <br>
Mitigation: Clarify Redis configuration and treat the Civic-related message as unimplemented unless a separate identity-verification integration is provided. <br>
Risk: Action justifications can expose secrets or sensitive personal data in the persistent audit ledger. <br>
Mitigation: Keep justifications specific but omit secrets and sensitive personal data, and restrict access to the audit ledger. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mithileshgau/clawguard1) <br>
- [ClawGuard Governance Protocol](artifact/GUIDANCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON tool responses and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns allowed or blocked status messages and recent audit ledger entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
