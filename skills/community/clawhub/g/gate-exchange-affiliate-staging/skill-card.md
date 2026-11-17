## Description:

Gate partner affiliate data and application skill for partner commissions, referral volume, application eligibility, and application status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate partners and developers use this skill to query read-only affiliate metrics, check partner application eligibility or recent status, and produce concise partner reports from configured Gate MCP credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad commission or application-status triggers may cause account-linked Gate affiliate data to be queried from ambiguous user prompts.

Mitigation: Use explicit Gate affiliate wording for intended requests and treat commission, eligibility, and application-status prompts as sensitive.

Risk: The skill can access Gate affiliate data through configured MCP credentials.

Mitigation: Install only when credentialed Gate affiliate reporting is intended, keep secrets in the configured MCP session, and require Rebate:Read permission.

Risk: Incorrect time windows, trader filters, or aggregation can misstate commission, volume, or fee metrics.

Mitigation: Respect the 30-day API request limit, split longer supported windows, avoid future timestamps, use user_id only for explicit trader queries, and aggregate by the documented business rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gaixianggeng/skills/gate-exchange-affiliate-staging)
- [Gate Skills Homepage](https://github.com/gate/gate-skills)
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage)
- [Gate Affiliate Portal](https://www.gate.com/referral/affiliate)
- [Gate Exchange Affiliate Runtime Rules](artifact/references/gate-runtime-rules.md)
- [Gate Affiliate MCP Specification](artifact/references/mcp.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown reports and concise text responses with metric summaries, eligibility guidance, application status, and error handling notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only Gate MCP rebate tools, UTC+8 date windows, pagination when needed, and 30-day request segments for longer reporting periods.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version 2026.4.8-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
