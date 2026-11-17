## Description:

AI驱动金融分析 helps an agent support natural-language financial analysis, quantitative research workflows, sentiment analysis, financial indicator extraction, portfolio optimization, and report-style outputs from user-provided or API-backed financial data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for finance-oriented data analysis, quantitative research support, structured results, and report drafts. It is best treated as decision support that requires human review before trading, compliance, or business action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests powerful agent tools and describes file export behavior without tightly specifying destination paths.

Mitigation: Allow exports only to explicit user-chosen paths and review any Read, Write, Edit, or Bash action before it runs.

Risk: Financial data APIs may require credentials such as FINANCE_API_KEY.

Mitigation: Store credentials in environment variables or a secrets manager, use least-privilege keys, and avoid placing keys in prompts, files, or generated reports.

Risk: The artifact describes scheduled automatic financial screening tasks.

Mitigation: Enable scheduled tasks only with explicit user opt-in, document how to disable them, and avoid unattended trading or irreversible actions.

Risk: Financial analysis outputs can be incomplete, delayed, or misleading when source data is stale, unavailable, or misinterpreted.

Mitigation: Verify important results against authoritative data sources and require human review before investment, compliance, or business decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON examples, shell command snippets, and optional JSON or CSV exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on user-provided financial data, external financial data APIs, environment-provided LLM access, and FINANCE_API_KEY-style credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
