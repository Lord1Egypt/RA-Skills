## Description: <br>
DiDi Ride SKILL helps agents handle China urban mobility requests, including ride hailing, fare estimates, route planning, nearby search, order status, driver location, and cancellations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[didi](https://clawhub.ai/user/didi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to plan routes, estimate fares, create or manage DiDi ride orders, and query driver or order status through the DiDi MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive DIDI_MCP_KEY credential and may encourage users to share or persist it in chat. <br>
Mitigation: Use a secure configuration method for DIDI_MCP_KEY, avoid pasting the key into normal chat, and confirm what account permissions the key grants before installation. <br>
Risk: The skill can place real or scheduled ride orders, store addresses and phone numbers, and send delayed status notifications. <br>
Mitigation: Review order details before use, preserve the documented confirmation steps for ride creation and cancellation, and monitor stored preferences for sensitive personal data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/didi/didi-ride-skill-official) <br>
- [DiDi MCP Platform](https://mcp.didichuxing.com) <br>
- [DiDi MCP Key Setup](https://mcp.didichuxing.com/claw) <br>
- [Setup Reference](references/setup.md) <br>
- [Workflow Reference](references/workflow.md) <br>
- [API Reference](references/api_references.md) <br>
- [Error Handling Reference](references/error_handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and structured ride status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw, mcporter, and a configured DIDI_MCP_KEY.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
