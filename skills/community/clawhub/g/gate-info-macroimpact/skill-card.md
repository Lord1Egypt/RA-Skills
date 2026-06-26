## Description: <br>
Macro-driven crypto via Gate-Info and Gate-News MCP for analyzing how macro events and indicators relate to crypto markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to connect macroeconomic events such as CPI, NFP, Fed decisions, rates, and payrolls with crypto market context. The skill coordinates read-only Gate Info and Gate News MCP queries, then produces a structured macro-to-crypto impact report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Gate Info and Gate News MCP servers; missing or untrusted MCP servers could lead to incomplete or unreliable analysis. <br>
Mitigation: Confirm the required MCP servers come from a trusted source before use, and degrade gracefully when a required tool is unavailable. <br>
Risk: Macro and crypto correlations can be uncertain and should not be treated as trading instructions. <br>
Mitigation: Keep outputs neutral and data-driven, label uncertainty clearly, and avoid explicit buy or sell advice. <br>


## Reference(s): <br>
- [Gate Info Macro Impact Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-info-macroimpact) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown report with tables and concise narrative analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Gate Info and Gate News MCP results; does not place trades, request secrets, or write files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
