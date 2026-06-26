## Description: <br>
Spending controls for AI agents that pay online via x402. Set limits, require human approval, audit every payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmrtn](https://clawhub.ai/user/nmrtn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use blacktea to let agents access paid x402 endpoints while enforcing spending limits, human approval, and audit logging. It is intended for agents that may pay for APIs, premium data feeds, or other online services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent make real x402 payments using a wallet private key. <br>
Mitigation: Use a dedicated low-balance wallet, set conservative auto-approval limits and a hard cap, and require human approval for larger payments. <br>
Risk: Installing the MCP server means trusting an external package with limited spending authority. <br>
Mitigation: Review the @nmrtn/blacktea-mcp package before using a funded key and test first with BLACKTEA_RAIL=mock. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nmrtn/blacktea) <br>
- [blacktea Repository](https://github.com/nmrtn/blacktea) <br>
- [blacktea MCP npm Package](https://www.npmjs.com/package/@nmrtn/blacktea-mcp) <br>
- [Policy Cookbook](https://github.com/nmrtn/blacktea/blob/main/docs/policy-cookbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP server setup, payment approval flow, spending-policy examples, and audit-query guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
