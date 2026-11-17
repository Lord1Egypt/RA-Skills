## Description:

Survey arXiv papers from a given year to present on a specific theme. Automatically categorizes papers, translates abstracts to Chinese, and generates a structured markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[6eanut](https://clawhub.ai/user/6eanut)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to ask an agent to search arXiv by year and theme, then produce a structured Markdown survey report with paper metadata and Chinese abstract summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a shell script that makes arXiv API requests and writes Markdown files.

Mitigation: Review the command arguments and output directory before execution, and run it only in a workspace where writing report files is expected.

Risk: Documentation describes automatic categorization and Chinese translation, but security evidence says the script may only create a basic report stub without additional agent work.

Mitigation: Treat generated surveys as drafts and have the agent or a reviewer refine categories, translations, and paper summaries before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/6eanut/skills/arxiv-survey)
- [arXiv API query endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an arxiv-survey-<year>-<theme-slug>.md file; the included script creates a basic report stub and may rely on the agent for categorization, translation, and refinement.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
