## Description: <br>
Search engine for AI agents to discover free and paid tools, APIs, and MCP servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmmel](https://clawhub.ai/user/simmmel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use add.tools to search for free or paid tools, APIs, MCP servers, and x402 endpoints, then review metadata such as capabilities, pricing, and reliability before selecting a tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and optional feedback are sent to add.tools and could reveal sensitive project details if users include them. <br>
Mitigation: Do not include secrets, private project names, credentials, confidential prompts, or sensitive operational details in searches or feedback. <br>
Risk: Returned tools or paid x402 endpoints may have their own security, pricing, reliability, or permission requirements. <br>
Mitigation: Review each returned tool or paid endpoint before allowing an agent to use it, including its permissions, pricing model, and trust posture. <br>


## Reference(s): <br>
- [add.tools website](https://add.tools) <br>
- [add.tools search API example](https://add.tools/search?q=send+email) <br>
- [add.tools feedback endpoint](https://add.tools/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Text] <br>
**Output Format:** [Markdown with inline bash examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches return ranked tool metadata; optional feedback can be submitted to improve result quality.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
