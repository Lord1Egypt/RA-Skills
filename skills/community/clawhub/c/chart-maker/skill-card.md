## Description: <br>
Chart Generator helps agents create bar, line, pie, scatter, radar, area, and stacked charts from common data sources for reports, presentations, and documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and document authors use this skill to generate local charts from manual data, CSV, Excel, JSON, or extracted text and embed the results into reports or presentation materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python can read local input files and write chart or document outputs. <br>
Mitigation: Install in a virtual environment when possible, review generated Python before running it, and choose input and output paths deliberately. <br>
Risk: Generated Word, HTML, and Markdown files may contain embedded chart data or untrusted titles and captions. <br>
Mitigation: Treat generated documents as shareable artifacts that may expose embedded data, and escape or review untrusted titles and captions before publishing HTML or Markdown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/chart-maker) <br>
- [Publisher profile](https://clawhub.ai/user/tobewin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command code blocks; generated artifacts may include PNG, SVG, PDF, Word, Excel, Markdown, or HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python dependencies and writes chart/report files to deliberate output paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
