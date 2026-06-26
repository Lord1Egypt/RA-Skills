## Description: <br>
Fetches Fortune China 500 ranking data for supported years and produces an Excel workbook with rank, company name, industry, revenue, source, and retrieval time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyqdq888](https://clawhub.ai/user/hyqdq888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve Fortune China 500 company rankings for a requested year and generate a spreadsheet for review, reporting, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a public Fortune China data website to retrieve ranking data. <br>
Mitigation: Review expected network access before installation or execution, and verify generated data against the cited source when accuracy matters. <br>
Risk: The skill writes a local .xlsx file and may use a default /tmp output path. <br>
Mitigation: Choose and review the output path when file location or overwrite behavior matters. <br>
Risk: The skill depends on Python packages for HTTP requests, HTML parsing, and Excel generation. <br>
Mitigation: Install dependencies from trusted package sources and scan the environment according to local policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hyqdq888/fortune-china500-skill) <br>
- [Fortune China 500 data source](https://www.caifuzhongwen.com/fortune500/paiming/china500/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Guidance] <br>
**Output Format:** [Excel workbook (.xlsx) plus concise status or availability messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local .xlsx output, defaulting to /tmp unless an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
