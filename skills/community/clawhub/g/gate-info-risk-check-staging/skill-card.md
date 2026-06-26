## Description: <br>
Token and address risk assessment for security-only queries about token contracts, honeypots, rugs, and address safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request security-focused token or contract risk reports, including honeypot, tax, holder concentration, open-source, and name-risk checks. Address safety requests are supported only as basic on-chain information until address compliance risk detection is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address safety output can be mistaken for a blacklist, compliance label, or definitive safety verdict even though address compliance risk detection is unavailable. <br>
Mitigation: State that address compliance risk detection is under development and provide only basic on-chain address information unless a supported compliance signal is available. <br>
Risk: Automated token checks can miss risks outside the retrieved on-chain security data. <br>
Mitigation: Avoid absolute safety guarantees, preserve high-severity warnings such as honeypot, high tax, or concentrated holdings, and recommend further due diligence when risk signals or missing data warrant it. <br>


## Reference(s): <br>
- [Gate Info RiskCheck MCP Specification](references/mcp.md) <br>
- [RiskCheck Scenarios and Prompt Examples](references/scenarios.md) <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-info-risk-check-staging) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown risk report or concise degradation notice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token mode produces a structured contract security report; address mode discloses that compliance risk labels are unavailable and reports only basic on-chain information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
