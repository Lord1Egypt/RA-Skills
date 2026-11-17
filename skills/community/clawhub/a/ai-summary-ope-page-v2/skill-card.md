## Description:

Creates Russian, board-oriented summaries of PDF and DOCX reports with source-checked facts and discussion questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dariaakimov](https://clawhub.ai/user/dariaakimov)

### License/Terms of Use:

MIT-0

## Use Case:

Board members and analysts use it to turn PDF and DOCX reports into Russian A4 summaries with key findings and open questions for discussion. It supports Russian or foreign-language source reports and recommends human review before circulation.

### Deployment Geography for Use:

Global (Russian-language, Sber-focused use)

## Known Risks and Mitigations:

Risk: Automated checks may not catch inaccurate quotations, chart values, source pages, or unsupported meaning.

Mitigation: Human-check quotations, chart values, and cited source pages before circulating the summary.

Risk: Web search or runtime network access may be unsuitable for confidential reports.

Mitigation: Decline web search for confidential material, preload OCR models, or block runtime network access.

Risk: Working copies of report content may remain after processing.

Mitigation: Purge retained working copies when finished.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dariaakimov/skills/ai-summary-ope-page-v2)
- [Summary canon](artifact/references/summary_canon.md)
- [Fact-check guide](artifact/references/factcheck_guide.md)
- [Translation guide](artifact/references/translation_guide.md)
- [Humanization guide](artifact/references/humanize_guide.md)

## Skill Output:

**Output Type(s):** [PDF, Text]

**Output Format:** [Russian-language A4 PDF summary with key findings, discussion questions, and source-page references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for one page but may exceed one page; an HTML copy is available only on request.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
