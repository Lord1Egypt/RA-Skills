## Description:

Generates Chinese Markdown and PDF financial news briefs from important global market news from the past 24 hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jihefanlan-art](https://clawhub.ai/user/jihefanlan-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-news readers use this skill to gather recent macro, equity, foreign exchange, and commodity news into a structured Chinese daily brief with cited sources and PDF output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs web research for time-sensitive financial reporting, which can produce incomplete, stale, or misleading summaries if sources are weak or market conditions change quickly.

Mitigation: Review the cited source links and treat the report as informational rather than investment advice.

Risk: The PDF generation script may install Python packages automatically.

Mitigation: Preinstall reviewed, pinned dependencies in an isolated environment before running the skill.

Risk: The skill writes report files and uses headless Chrome with reduced sandboxing for PDF generation.

Mitigation: Review the script first, confirm output paths, and run it only in a controlled workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jihefanlan-art/skills/finance-news-brief)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands]

**Output Format:** [Markdown report and PDF file, with final file paths reported in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes finance_brief_YYYYMMDD.md and finance_brief_YYYYMMDD.pdf to the current or user-specified directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
