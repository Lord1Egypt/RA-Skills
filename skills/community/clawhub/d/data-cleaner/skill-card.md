## Description:

Clean and standardize multi-format data with AI-powered field detection, deduplication, missing-value fill, format normalization, multi-source merge, and Feishu-native output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffersplind92](https://clawhub.ai/user/jeffersplind92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to clean, normalize, deduplicate, classify, merge, and export messy spreadsheet, CSV, JSON, or pasted business data. Typical uses include CRM cleanup, order reconciliation, roster cleanup, and multi-system data merge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataset samples may be sent to external AI providers or Feishu outputs when those features are enabled.

Mitigation: Use only non-sensitive or approved datasets unless AI and Feishu uploads are disabled or explicitly governed.

Risk: The shared DATA_CLEANER_API_KEY can be used for MiniMax or DeepSeek features and may also be sent to YK Global for tier verification.

Mitigation: Do not set DATA_CLEANER_API_KEY unless the credential-sharing behavior is acceptable; use isolated credentials and review provider governance before enabling AI features.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffersplind92/skills/data-cleaner)
- [Publisher profile](https://clawhub.ai/user/jeffersplind92)
- [YK-Global paid plans](https://yk-global.com)
- [MiniMax API platform](https://platform.minimax.chat/)
- [DeepSeek API platform](https://platform.deepseek.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI and Python examples; cleaned data files may be exported as CSV or XLSX, and reports may be generated as Markdown or Feishu documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local output files, create Feishu Bitable records and documents, and return structured run metadata such as cleaned row counts, report data, tier, and usage summary.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
