## Description: <br>
finstep-mcp provides Finstep financial data lookups for market quotes, sectors, company information, macroeconomic indicators, research reports, news, announcements, and trading calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fa1c0n4826](https://clawhub.ai/user/fa1c0n4826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Finstep shell tools for financial market research, including stock quotes, sector rankings, company fundamentals, macroeconomic data, financial news, reports, and announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial lookup queries and the Finstep API signature are sent to Finstep services. <br>
Mitigation: Install only if Finstep is trusted for those queries, keep FINSTEP_SIGNATURE in a secret store or environment variable, and rotate it if exposed. <br>
Risk: Broad URL parsing and web search helpers could disclose confidential or internal content. <br>
Mitigation: Avoid using those helpers with private URLs, internal documents, credentials, or confidential business data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fa1c0n4826/finstep-mcp) <br>
- [Finstep product site](https://product.finstep.cn/) <br>
- [Finstep API base endpoint](https://fintool-mcp.finstep.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; scripts return JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSTEP_SIGNATURE and local bash, curl, jq, and date binaries.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
