## Description: <br>
客户脉搏 / Customer Pulse is a lightweight CRM assistant for managing customer records, logging follow-ups, tracking sales funnels, and identifying churn risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams and individual account managers use this skill to maintain a local CRM ledger, record follow-up activity, monitor pending customer actions, and review pipeline or churn-risk signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer and sales records are stored locally and CSV exports can contain sensitive business data. <br>
Mitigation: Use an access-controlled data directory, protect exported files and backups, and avoid sharing exports through untrusted channels. <br>
Risk: Delete, import, and export operations can change or expose CRM records. <br>
Mitigation: Review destructive or bulk file commands before execution and keep a current backup before imports or deletes. <br>


## Reference(s): <br>
- [CRM Practice Guide](references/crm-guide.md) <br>
- [Customer Pulse Skill Page](https://clawhub.ai/hanjing5024064/customer-pulse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command outputs and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can generate local JSON records, CSV imports or exports, tabular summaries, reminders, pipeline statistics, and Mermaid charts for paid-tier reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
