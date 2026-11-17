## Description:

Fetches WeChat public-account article links from the Dajiala API and saves them to an Excel file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mabao-laodie](https://clawhub.ai/user/mabao-laodie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect recent WeChat public-account article metadata from Dajiala and generate a local Excel report for review or downstream reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated spreadsheets contain remote article data and links that may be interpreted by spreadsheet software.

Mitigation: Review generated .xlsx files before sharing or opening them in environments that evaluate formulas, links, or external content.

Risk: The skill requires a Dajiala API key and writes reports to a configured local path.

Mitigation: Provide DAJIALA_KEY only in trusted environments and confirm the input and output paths before execution.

## Reference(s):

- [Dajiala API endpoint used by the skill](https://www.dajiala.com/fbmain/monitor/v3/post_condition)
- [ClawHub skill page](https://clawhub.ai/mabao-laodie/skills/dajiala-article-fetcher)
- [Publisher profile](https://clawhub.ai/user/mabao-laodie)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python execution and Excel file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DAJIALA_KEY and writes generated .xlsx reports under the configured local output path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
