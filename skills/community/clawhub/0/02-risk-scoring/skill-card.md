## Description: <br>
Scores Cainiao logistics suppliers and Cainiao station franchisees, returning risk levels, core issue diagnosis, and advisory actions from KPI, complaint, violation, and operating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal operations, compliance, and vendor-management users use this skill to assess supplier or station risk, identify the main drivers behind the score, and prepare advisory follow-up actions from supplied KPI, complaint, violation, and operating-history data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce business recommendations about supplier suspension, termination, or clearance based on user-provided records. <br>
Mitigation: Treat outputs as advisory and require a qualified human reviewer before taking consequential action. <br>
Risk: Supplier, station, complaint, and operations records may include personal or sensitive information. <br>
Mitigation: Redact unnecessary identifiers such as names, phone numbers, addresses, and complaint narratives before use. <br>
Risk: Scoring thresholds and rule weights may not match an organization's authorized policy. <br>
Mitigation: Verify that the scoring rules and any weight adjustments are approved for the organization before using real records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/02-risk-scoring) <br>
- [Continuation reference](references/continuation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown risk scoring report with tables and prioritized recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include data-gap notes, trend analysis, peer comparison, risk level, one-vote veto flags, and review-cycle recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter declares model v1.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
