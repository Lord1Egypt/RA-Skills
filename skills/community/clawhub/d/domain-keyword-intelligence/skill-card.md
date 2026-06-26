## Description: <br>
Discover domain investment opportunities from emerging keyword spikes. Filters junk signals from real multi-party market activity using registration profiling, catalyst research, and NRDS position analysis. Powered by DomainKits MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abtdomain](https://clawhub.ai/user/abtdomain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, domain investors, and domain research teams use this skill to identify emerging registration trends, separate multi-party demand from low-quality spikes, and investigate catalysts before pursuing domain opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional DomainKits API key is an account credential. <br>
Mitigation: Store the key in the agent or MCP environment as DOMAINKITS_API_KEY and avoid pasting it into prompts, logs, or shared outputs. <br>
Risk: Domain research prompts may disclose confidential acquisition plans or client strategy to DomainKits or web search services. <br>
Mitigation: Avoid entering confidential plans, client names, or private strategy unless those disclosures are approved for the connected services. <br>
Risk: Connecting to an unintended MCP endpoint could expose requests or credentials. <br>
Mitigation: Verify the DomainKits MCP endpoint before connecting it and use the documented service URL from the skill references. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/abtdomain/domain-keyword-intelligence) <br>
- [DomainKits MCP documentation](https://domainkits.com/mcp) <br>
- [DomainKits MCP GitHub repository](https://github.com/ABTdomain/domainkits-mcp) <br>
- [ABTdomain](https://abtdomain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown analysis with tables, concise profile summaries, cited catalyst links, and optional MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DomainKits MCP and web search access; optional DOMAINKITS_API_KEY can raise service limits.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
