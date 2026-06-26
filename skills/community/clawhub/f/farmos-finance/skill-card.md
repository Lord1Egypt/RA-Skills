## Description: <br>
Query farm financial data including cash flow projections, cost tracking, and breakeven analysis with admin-only access controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianppetty](https://clawhub.ai/user/brianppetty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Farm owners and authorized administrators use this skill to retrieve cost summaries, cash flow projections, breakeven analysis, and detailed cost line items while keeping financial data restricted to admin users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents access to sensitive farm financial data. <br>
Mitigation: Use only with admin authorization and do not return financial details to non-admin users. <br>
Risk: The security summary notes plain HTTP and unauthenticated integration endpoints. <br>
Mitigation: Install only on a trusted private network, prefer HTTPS and authenticated endpoints, and enable AI access only intentionally. <br>
Risk: Partial endpoint failures can lead to misleading financial reporting. <br>
Mitigation: State endpoint failures clearly and do not present costs without revenue as a complete cash flow picture. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/brianppetty/farmos-finance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with API request guidance and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial reports should state totals, disclose endpoint failures, and avoid presenting partial cash flow data as complete.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
