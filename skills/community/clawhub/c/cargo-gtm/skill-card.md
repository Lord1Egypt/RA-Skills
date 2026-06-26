## Description: <br>
Cargo Gtm routes GTM prospecting, enrichment, email and phone lookup, verification, scoring, sequencing, CRM sync, and signal-monitoring tasks through Cargo guides, recipes, and provider playbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and GTM operators use this skill to plan and execute Cargo workflows for building prospect lists, enriching accounts and contacts, verifying outreach data, monitoring buying signals, and preparing records for CRM or sequencer activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enrich personal data and send prospect, account, or deal data to Cargo and named third-party providers. <br>
Mitigation: Use it only in authorized workspaces, minimize fields, confirm vendor and privacy requirements, and require explicit approval before enrichment, reverse lookup, visitor identification, or LLM analysis of internal data. <br>
Risk: The skill can mutate CRM or sequencer records and send Slack or webhook notifications. <br>
Mitigation: Require explicit user approval before writes or sends, verify mappings and suppression lists, and review generated records before activation. <br>
Risk: Recurring monitoring can keep processing prospect or account data after the initial request. <br>
Mitigation: Require approval for scheduled monitoring, document scope and cadence, and provide a clear stop or review path. <br>


## Reference(s): <br>
- [Cargo Gtm on ClawHub](https://clawhub.ai/cargo-ai/cargo-gtm) <br>
- [Cargo Skills Homepage](https://github.com/getcargohq/cargo-skills) <br>
- [Stage Action Map](references/stage-action-map.md) <br>
- [Credits Cost Table](references/credits-cost-table.md) <br>
- [Waterfall Strategy](references/waterfall-strategy.md) <br>
- [Output Retrieval](references/output-retrieval.md) <br>
- [Alternative Provider Chains](references/alternatives.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workflow plans, provider/action selections, credit estimates, enrichment steps, output retrieval commands, and CRM or sequencer activation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
