## Description: <br>
Doorstep helps agents arrange real-world pickups, deliveries, errands, and gifts through a human tasker in San Francisco. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjmaxwell4](https://clawhub.ai/user/jjmaxwell4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use Doorstep to request San Francisco-only physical-world errands, review quotes, approve payment, and track tasker progress. <br>

### Deployment Geography for Use: <br>
San Francisco, CA <br>

## Known Risks and Mitigations: <br>
Risk: Doorstep handles sensitive account, location, task, and payment-related details. <br>
Mitigation: Share only the minimum necessary address, timing, item, phone, and message details, and protect the Doorstep API key. <br>
Risk: Physical errands can involve charges, dispatch, and no-refund cancellation after a tasker has actively started. <br>
Mitigation: Review the final task, quote, address, timing, and any auto-approval limits before approving payment or dispatch. <br>
Risk: Requests outside San Francisco are unsupported. <br>
Mitigation: Decline or caveat tasks outside San Francisco before creating a Doorstep task. <br>


## Reference(s): <br>
- [Doorstep homepage](https://trydoorstep.app) <br>
- [Doorstep API key dashboard](https://trydoorstep.app/dashboard/api-keys) <br>
- [Doorstep MCP endpoint](https://trydoorstep.app/mcp) <br>
- [Doorstep auth MCP endpoint](https://trydoorstep.app/mcp/auth) <br>
- [ClawHub Doorstep release page](https://clawhub.ai/jjmaxwell4/doorstep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task status, quote, receipt, account, and message details returned by the Doorstep MCP service.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
