## Description:

Fxbaogao Deep Research helps agents conduct structured research on industries, companies, or topics by decomposing questions, searching fxbaogao reports, reading selected reports, and producing traceable conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quickzhang](https://clawhub.ai/user/quickzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, researchers, and agents use this skill to plan and execute fxbaogao report research, including single-report close reading and multi-report deep research with traceable evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, organization filters, and report IDs may be sent to the fxbaogao API using the configured API key.

Mitigation: Use the skill only for intended fxbaogao research workflows and avoid submitting sensitive queries unless permitted by local policy.

Risk: Downloaded PDFs and generated Markdown outputs are research material, not verified ground truth.

Mitigation: Review source PDFs, report IDs, and generated conclusions before relying on them for decisions.

Risk: Paragraph summaries can be insufficient for formal citation or key-data verification.

Mitigation: Download and inspect the original PDF before quoting text, relying on page-specific data, or treating a finding as final.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quickzhang/skills/fxbaogao-deep-research)
- [Fxbaogao API Usage](artifact/references/api-usage.md)
- [Research Playbook](artifact/references/research-playbook.md)
- [Report Reader Playbook](artifact/references/report-reader-playbook.md)
- [Fxbaogao Report Viewer](https://www.fxbaogao.com/view?id=<reportId>)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and workspace files with report links, fact cards, comparison tables, and API command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FXBAOGAO_API_KEY and external access to api.fxbaogao.com; key data should be checked against downloaded PDFs for formal research.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
