## Description: <br>
A public fund allocation advisor agent skill that provides fund data queries, portfolio allocation, risk assessment, market monitoring, investment education, report generation, and Feishu notification workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xikal](https://clawhub.ai/user/xikal) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to operate a fund-advisor agent for fund research, portfolio planning, risk review, alerts, investment diary entries, and report generation. It is intended to support investment education and analysis workflows, not to replace professional financial judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store or transmit user-provided investment preferences, diary entries, alerts, and generated reports through configured services. <br>
Mitigation: Avoid brokerage credentials, bank credentials, account numbers, and highly sensitive personal details; verify S3, Feishu, knowledge-base, retention, deletion, and access-control settings before real use. <br>
Risk: Fund data, portfolio suggestions, and generated reports may be incomplete, delayed, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as informational support, verify market and fund data against official sources, and review decisions with qualified financial professionals where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xikal/fund-advisor-agent) <br>
- [Fund Advisor Agent README](artifact/README.md) <br>
- [Usage examples](artifact/examples/usage-examples.md) <br>
- [Tool development guidelines](artifact/references/tool-development.md) <br>
- [Skill integration guide](artifact/references/skill-integration.md) <br>
- [Agent best practices](artifact/references/agent-best-practices.md) <br>
- [Data storage plan](artifact/references/data-storage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Files, Configuration] <br>
**Output Format:** [Natural-language responses, Markdown investment reports, generated PDF/DOCX/Excel files, alert messages, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use fund data search, document generation, knowledge search, local temporary storage, S3 report links, and Feishu notifications when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
