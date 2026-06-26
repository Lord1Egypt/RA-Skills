## Description: <br>
Query land ownership, leases, landlord info, and land payments. Write operations for payment management and lease renewals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianppetty](https://clawhub.ai/user/brianppetty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Farm operations managers and authorized staff use this skill to inspect owned and leased land, lease terms, landlord contacts, payment status, annual land costs, and cash requirements. It also supports authenticated payment updates and lease renewal workflows with preview and confirmation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive lease terms, rent amounts, landlord contact details, and payment records. <br>
Mitigation: Install only in a trusted private FarmOS environment and enforce admin or manager authorization on all read and write endpoints. <br>
Risk: Bulk payment marking, lease renewal, and year-end rollover actions can change financial records at scale. <br>
Mitigation: Require the agent to show affected records and obtain explicit human confirmation before any bulk payment, lease renewal, or rollover execution. <br>
Risk: Using truncated dashboard data could create incomplete or misleading financial summaries. <br>
Mitigation: Use the complete `/all` endpoints for portfolio queries, report returned record counts, and tell the user when complete data cannot be retrieved. <br>
Risk: Authenticated write operations depend on a local helper and short-lived JWTs. <br>
Mitigation: Verify the local auth helper before use and ensure the FarmOS server enforces authorization on both read and write endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianppetty/farmos-land-portfolio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, API paths, and structured summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should report record counts, avoid truncated data, and require explicit confirmation before bulk write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
