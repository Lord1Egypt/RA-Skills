## Description: <br>
成交加速器 is a Chinese-language CRM assistant for deal management, email signal extraction, pipeline analysis, AI follow-up drafting, self-learning sales intelligence, CRM knowledge graphs, and native IMAP/SMTP email workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams and CRM operators use this skill to manage opportunities, track meetings, analyze sales funnels, draft follow-up emails, extract mailbox signals, and maintain relationship context for active deals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read mailbox content and uses mailbox credentials when email integrations are enabled. <br>
Mitigation: Install only with an appropriate mailbox scope, prefer a dedicated mailbox or app password, protect credential environment variables, and avoid retaining unnecessary email snippets. <br>
Risk: The skill can send email and change CRM data, including import, export, delete, and update actions. <br>
Mitigation: Require manual review before outbound email, delete, import, export, or bulk CRM operations. <br>
Risk: Local CRM, meeting, email, learning, and graph data may contain sensitive sales records. <br>
Mitigation: Protect the configured local data directory and apply normal access controls for customer, opportunity, and mailbox-derived records. <br>


## Reference(s): <br>
- [Deal Closer Skill Page](https://clawhub.ai/hanjing5024064/deal-closer) <br>
- [邮件服务配置指南](references/email-setup-guide.md) <br>
- [销售管道报告模板](references/pipeline-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese-language Markdown with command examples, tables, reports, email drafts, and local JSON-backed workflow guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate Mermaid chart snippets and outbound email drafts; users should review CRM changes, imports, exports, deletes, and emails before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and release changelog state 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
