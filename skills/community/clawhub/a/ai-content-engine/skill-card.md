## Description: <br>
AI Content Engine lets agents generate video scripts, images, and short-form or long-form videos through an MCP server with public quote tools, API-key brand access, and paid USDC or prepaid-token operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimitd-ai](https://clawhub.ai/user/jimitd-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and agent operators use this skill to quote, generate, retrieve, and publish AI-assisted scripts, images, and videos. It supports anonymous pricing checks, brand-scoped content lookup with an API key, and paid creation or publishing flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid tools and token purchases can spend USDC or prepaid content tokens. <br>
Mitigation: Use sandbox mode first, call pricing or quote tools before paid operations, and require explicit approval before signing payments or purchasing tokens. <br>
Risk: The skill can use sensitive credentials, including an API key and wallet private key. <br>
Mitigation: Keep credentials out of prompts and logs, use a dedicated low-balance Base wallet for payment signing, and scope API keys to the intended brand. <br>
Risk: Publishing tools can post generated content to connected social platforms. <br>
Mitigation: Manually review generated content and publishing targets before approving social publishing requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimitd-ai/ai-content-engine) <br>
- [Content Engine Homepage](https://content-engine-app.fly.dev) <br>
- [MCP Endpoint](https://content-engine-x402.fly.dev/mcp) <br>
- [MCP Server Discovery](https://content-engine-x402.fly.dev/.well-known/mcp.json) <br>
- [x402 Payment Protocol](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [MCP tool responses, Markdown guidance, JSON-like content metadata, and generated media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid operations may require explicit USDC payment approval or prepaid-token authorization; brand-scoped reads require an API key.] <br>

## Skill Version(s): <br>
1.0.9 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
