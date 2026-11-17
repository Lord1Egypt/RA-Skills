## Description:

Helps users summarize daily work and generate structured Markdown daily reports when prompted for a daily report, work summary, or end-of-day update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yying01](https://clawhub.ai/user/yying01)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual contributors use this skill to turn daily work notes into a structured report organized by project, status, next-day plan, and remarks. It can optionally save the generated report as a dated Markdown file in a configured reports directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional save flow can write or overwrite local report files in the configured reports directory.

Mitigation: Set REPORTS_DIR deliberately, review the destination path before saving, and confirm overwrite behavior before relying on the saved file.

Risk: Passing report content as a shell command argument can expose sensitive report text or mishandle special characters.

Mitigation: Avoid placing sensitive content in reports unless intended, and prefer a safer save path that accepts content through stdin or another shell-free API.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown daily report with optional shell command output from saving the report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a dated Markdown file to REPORTS_DIR or ~/reports when the save script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
