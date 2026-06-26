## Description: <br>
Gate partner affiliate data and application skill for partner commissions, referral volume, and affiliate program application questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate Exchange partners and their supporting agents use this skill to review affiliate eligibility, recent application status, commissions, referred-user activity, and team performance through the configured Gate MCP session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Affiliate reports can be misleading if list fields are summed blindly or if assets, deduplication, and period boundaries are ignored. <br>
Mitigation: Use the documented aggregation rules and disclose empty, truncated, or paginated results instead of fabricating totals. <br>
Risk: Partner API credentials and user identifiers expose account-specific affiliate data. <br>
Mitigation: Use only the configured local Gate MCP session, never ask users to paste secrets, and query only the authenticated partner's data. <br>
Risk: Gate partner history endpoints have time-window limits and reject future query bounds. <br>
Mitigation: Normalize ranges in UTC+8, split requests longer than 30 days up to the documented 180-day limit, and reject future-dated requests. <br>
Risk: Security guidance indicates generated campaign material may require human review before use. <br>
Mitigation: Review generated user-facing guidance before sending or acting on it, especially where regulatory, identity, consent, or unsubscribe details are involved. <br>


## Reference(s): <br>
- [Gate Skills Homepage](https://github.com/gate/gate-skills) <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-exchange-affiliate) <br>
- [Gate Affiliate Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate Affiliate MCP Specification](references/mcp.md) <br>
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage) <br>
- [Gate Affiliate Dashboard](https://www.gate.com/referral/affiliate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown reports, concise setup guidance, and read-only partner data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Gate MCP session with GATE_API_KEY and GATE_API_SECRET; normal operation is read-only.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
