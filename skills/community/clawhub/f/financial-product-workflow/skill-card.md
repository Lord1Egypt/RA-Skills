## Description: <br>
Helps financial product teams use an AI-assisted workflow for strategy, requirement analysis, product design, technical review, development follow-up, testing, launch operations, compliance checks, and tool-connected delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial product managers and delivery teams use this skill to structure financial product work from early strategy through launch operations, including PRDs, requirements, self-operation design, compliance checklists, and fallback documentation when integrations are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow encourages connected business-tool writes such as creating issues, pages, notifications, branches, or other external records. <br>
Mitigation: Use sandbox projects first and require manual approval before every external create, update, or send action. <br>
Risk: Broad API tokens or workspace credentials could allow excessive access to Jira, Confluence, code hosting, analytics, or messaging systems. <br>
Mitigation: Use least-privilege credentials scoped to the minimum project, space, repository, or channel required for the task. <br>
Risk: Financial product work may involve regulated, customer, or confidential data. <br>
Mitigation: Do not provide regulated, customer, or confidential financial data to integrations unless the organization has approved that data flow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lj22503/financial-product-workflow) <br>
- [Financial Product Workflow README](README.md) <br>
- [Quickstart Guide](QUICKSTART.md) <br>
- [Tool Support Guide](TOOLS_SUPPORT.md) <br>
- [Compliance Checklist](references/compliance-checklist.md) <br>
- [STAR Framework](references/star-framework.md) <br>
- [Self-Operation Design](references/self-operation-design.md) <br>
- [Tool Integration](references/tool-integration.md) <br>
- [MBTI Mapping](references/mbti-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with structured checklists, templates, Mermaid diagrams, code snippets, shell commands, and integration fallback steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose external business-tool actions when configured; users should approve create, update, or send actions before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
