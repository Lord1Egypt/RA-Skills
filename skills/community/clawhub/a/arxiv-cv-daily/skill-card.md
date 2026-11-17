## Description:

Fetch arXiv papers for a target date in cs.CV, screen them against a user topic, save logs under a user-chosen output directory, download matched PDFs, and summarize the matched papers from full text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrytea](https://clawhub.ai/user/harrytea)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, engineers, and agents use this skill to collect daily arXiv cs.CV papers for a chosen topic, screen titles and abstracts, download relevant PDFs when needed, and produce evidence-based paper shortlists and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts arXiv and downloads research artifacts from the internet.

Mitigation: Run it only where arXiv network access is expected, and review saved logs when downloads or API calls fail.

Risk: The skill creates logs, cache files, PDFs, extracted text, topic specs, and summaries under the selected output directory.

Mitigation: Choose a dedicated output directory that is appropriate for storing paper artifacts, then review generated files before sharing or retaining them.

Risk: PDF text extraction depends on the local pdftotext utility and may produce incomplete or poor-quality text.

Mitigation: Confirm pdftotext is installed and treat summaries as incomplete when extraction fails or the saved text is low quality.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrytea/skills/arxiv-cv-daily)
- [Publisher profile](https://clawhub.ai/user/harrytea)
- [arXiv API query endpoint](https://export.arxiv.org/api/query)
- [arXiv](https://arxiv.org)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files]

**Output Format:** [Markdown summaries and JSON manifests, with saved PDFs, extracted text, logs, and topic specification files under a user-chosen output directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-supplied topic, date, arXiv category, timezone, day count, and output root; requires network access to arXiv and pdftotext for PDF extraction.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
