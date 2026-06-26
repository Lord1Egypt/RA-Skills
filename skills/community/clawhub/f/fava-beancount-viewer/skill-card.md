## Description: <br>
Fava Beancount Viewer helps agents analyze Beancount/Fava portfolios for tax-loss harvesting, asset allocation, related security grouping, and tax-efficient selling workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to ask an agent for Beancount/Fava portfolio analysis, including allocation breakdowns, cash drag checks, related-security grouping, tax-loss harvesting, and gain-minimizing sell-order guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as a Fava/Beancount viewer, but the security evidence says its artifacts also steer agents toward quant-trading, broker, setup, and persistence workflows. <br>
Mitigation: Use the skill in an isolated environment, review proposed commands before running them, and require explicit user confirmation before any trading or account-impacting workflow. <br>
Risk: The skill may ask for broker, wallet, or paid-provider access when broader finance workflows are used. <br>
Mitigation: Avoid supplying broker, wallet, or paid-provider credentials unless they are intentionally required for the task and can be scoped to a test or least-privilege account. <br>
Risk: Generated portfolio, tax, and trading guidance can affect financial decisions if treated as authoritative. <br>
Mitigation: Treat outputs as decision support, verify calculations against source ledgers and market data, and route material tax or trading decisions through qualified review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/fava-beancount-viewer) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include financial analysis steps and executable local setup or data commands; review before execution.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
