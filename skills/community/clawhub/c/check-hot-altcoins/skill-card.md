## Description:

Generates a Chinese-language daily cryptocurrency briefing PDF with industry updates, FDV rankings, hot sectors, project watch items, and risk notes using CoinGecko market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nihaovand](https://clawhub.ai/user/nihaovand)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to compile a daily Chinese cryptocurrency morning report that ranks selected altcoins by FDV, summarizes sector movements, and prepares an HTML report for PDF export and optional sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary report and data files may be written to shared paths.

Mitigation: Use a private temporary directory with restrictive permissions and clean up generated files after the report is reviewed.

Risk: Generated HTML report fields may include unescaped content.

Mitigation: Escape all dynamic report fields before rendering HTML or exporting the PDF.

Risk: A generated report may be sent to Feishu without clear confirmation, including knowledge-base content.

Mitigation: Require explicit user confirmation before sending the report and review any sensitive or knowledge-base-derived content first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nihaovand/skills/check-hot-altcoins)
- [CoinGecko coins markets API](https://api.coingecko.com/api/v3/coins/markets)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Chinese-language HTML report intended for PDF export, with supporting shell and Python command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CoinGecko market data, writes temporary JSON and HTML report files, and may share the generated report through Feishu after review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
