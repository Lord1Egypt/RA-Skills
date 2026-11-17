## Description:

Helps agents configure, generate, debug, clean, and optimize web data processing workflows, including code generation from URLs and field descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to plan and debug web data processing workflows, generate starter Python code, clean extracted data, and improve processing strategies from run history. It is intended for authorized, compliant data handling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated networked data collection code can violate site rules, terms, or rate limits if used without review.

Mitigation: Review generated code before execution, honor robots.txt and site terms, prefer official APIs, and apply conservative rate limits.

Risk: Automation workarounds and evasion-oriented guidance can be misused against sites that restrict automated access.

Mitigation: Use automation only where authorized and remove or reject recommendations intended to bypass access restrictions.

Risk: The included contact-ranking behavior can process identifiable contact records without sufficient disclosure or consent.

Mitigation: Process contact data only with a clear lawful basis, minimize retained fields, and avoid profiling without appropriate review.

## Reference(s):

- [Data Handling Guide](artifact/references/data_handling_guide.md)
- [Data Quality Checklist](artifact/references/data_quality_checklist.md)
- [Process Best Practices](artifact/references/process_best_practices.md)
- [Crawl Best Practices](artifact/references/crawl_best_practices.md)
- [Publisher Homepage](https://xiaping.coze.site)
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/datacrawl-debug)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, generated Python code, and formatted data outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate runnable networked Python code and JSON, CSV, or JSONL formatted data outputs.]

## Skill Version(s):

1.2.0 (source: server release metadata, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
