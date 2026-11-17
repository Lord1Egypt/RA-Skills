## Description:

c刊期刊分析 helps agents collect recent CNKI metadata for CSSCI journals and generate a structured Word report covering publication trends, topics, keywords, methods, authors, columns, research gaps, and submission advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yipng05-max](https://clawhub.ai/user/yipng05-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and academic writers use this skill to analyze a named Chinese CSSCI journal's recent publication patterns and produce a Word report for topic selection, literature positioning, and submission planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted journal title can cause generated report or chart paths to escape the intended output folder.

Mitigation: Run the skill in a dedicated project folder or virtual environment, use trusted journal-title inputs, and sanitize output filenames before processing untrusted JSON.

Risk: The skill browses CNKI and creates local JSON, chart, and DOCX files.

Mitigation: Install and run it only in an environment where CNKI browsing, browser tooling, Python dependency installation, and local file creation are acceptable.

## Reference(s):

- [CNKI journal code quick reference](references/journal_codes.md)
- [CNKI journal navigation](https://navi.cnki.net/knavi/)
- [ClawHub skill page](https://clawhub.ai/yipng05-max/skills/cjournal-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with browser steps, Python commands, JSON input data, PNG charts, and a DOCX report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSON-derived analysis artifacts and a Word report; may require user-assisted CNKI verification and Python dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
