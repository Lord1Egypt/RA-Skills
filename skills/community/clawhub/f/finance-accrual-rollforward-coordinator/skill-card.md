## Description: <br>
Coordinate accrual rollforward work using memory-first retrieval and structured reconciliation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operations users use this skill to coordinate accrual rollforward reconciliation, preserve tracker and memo conventions, and manage related issue follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remembered tracker paths, labels, owners, or escalation conventions may be stale or mismatched. <br>
Mitigation: Confirm remembered values from memory before relying on them and review proposed rollforward changes before accepting them. <br>
Risk: Local tracker or memo edits could introduce incorrect accrual movement labels or unsupported reconciliation details. <br>
Mitigation: Review file edits for consistent movement labels and leave unmatched movements explicit instead of fabricating support. <br>
Risk: Scheduled follow-ups could be created with the wrong timing model. <br>
Mitigation: Use heartbeat only for periodic awareness and cron only for exact-time follow-ups, matching the user's requested scheduling mode. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with possible local file updates and scheduling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses remembered workspace paths and conventions when available; confirms unmatched movements instead of inventing support.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
