## Description:

Scrapes weekly Amazon Brand Analytics hot keyword rankings from AMZ123 and returns keyword trend data as CSV or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncai519](https://clawhub.ai/user/simoncai519)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and ecommerce analysts use this skill to collect Amazon keyword ranking and trend data from AMZ123 for a seed keyword.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser launch configuration disables the Chrome sandbox by default.

Mitigation: Run the skill in an isolated virtual environment or container, avoid privileged browser execution, and remove --no-sandbox unless the container requires it.

Risk: CSV reports may carry spreadsheet-handling risk when opened directly in office tools.

Mitigation: Prefer JSON output for downstream processing or sanitize CSV cells before opening reports in spreadsheet software.

## Reference(s):

- [Workflow Guide](references/workflow.md)
- [Output Format Specification](references/output.md)
- [AMZ123 Hot Keywords](https://www.amz123.com/usatopkeywords)
- [ClawHub Skill Page](https://clawhub.ai/simoncai519/skills/amz-hot-keywords)

## Skill Output:

**Output Type(s):** [text, files, JSON]

**Output Format:** [CSV or JSON file, with the created file path printed as plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output records include search_term, current_rank, last_rank, and trend; collection is capped at 200 results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
