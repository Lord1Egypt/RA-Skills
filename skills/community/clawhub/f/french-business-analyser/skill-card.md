## Description: <br>
Provides verified French business data for autonomous B2B agents by querying real-time signals from official registries through pay-per-call MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vannelier](https://clawhub.ai/user/vannelier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business and procurement agents use this skill to check French suppliers, invoices, VAT details, liens, certifications, director risk, and due diligence signals before payment or onboarding decisions. <br>

### Deployment Geography for Use: <br>
France <br>

## Known Risks and Mitigations: <br>
Risk: Paid checks can spend funds when invoked. <br>
Mitigation: Keep approval gates enabled and show the exact cost before each paid tool call. <br>
Risk: Hosted checks send French business identifiers, optional IBAN details, and invoice text to the remote service. <br>
Mitigation: Use the hosted service only for acceptable data, and self-host when invoices or identifiers require stricter data control. <br>
Risk: Returned business signals do not guarantee solvency and may miss confidential or delayed public registry events. <br>
Mitigation: Treat pay, hold, and block verdicts as decision support and escalate hold, block, incomplete, or high-value cases to a human reviewer. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/vannelier/french-business-analyser) <br>
- [Publisher profile](https://clawhub.ai/user/vannelier) <br>
- [Source code](https://github.com/Vannelier/MCP-business-checker) <br>
- [Hosted MCP endpoint](https://mcp-business-checker-production.up.railway.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some tools require explicit user approval and per-call payment before execution.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
