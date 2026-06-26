## Description: <br>
DataMaster Pro automates data fetching, cleaning, visualization, and report generation for data analysts and operations teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdp6539](https://clawhub.ai/user/gdp6539) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, data analysts, operations staff, and business teams use this skill to collect data from web, API, and database sources; clean CSV or JSON datasets; create charts; and generate Markdown, HTML, or PDF analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF report generation can run wkhtmltopdf through a shell command with user-controlled report names. <br>
Mitigation: Avoid PDF output and untrusted report names until the conversion call uses a non-shell argument API; validate report names before execution. <br>
Risk: Data fetching can use arbitrary URLs, API headers, and database connection strings. <br>
Mitigation: Restrict fetch targets to approved sources and use least-privilege, short-lived API tokens and database credentials; avoid cookies or long-lived secrets in command arguments. <br>


## Reference(s): <br>
- [DataMaster Pro ClawHub page](https://clawhub.ai/gdp6539/datamaster-pro) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript command examples and generated CSV, JSON, SVG, PNG, HTML, Markdown, or PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes business, technical, and weekly report templates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
