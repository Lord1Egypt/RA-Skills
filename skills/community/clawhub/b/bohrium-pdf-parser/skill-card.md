## Description: <br>
Parse PDF documents via open.bohrium.com to extract text, tables, charts, formulas, and molecules from PDF URLs or uploaded PDF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit PDF URLs or uploaded PDF files to Bohrium's parsing API and retrieve structured extraction results. It is suited for document parsing tasks involving text, tables, charts, formulas, equations, and molecular structures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF URLs, uploaded PDF files, task tokens, and parsed results are sent through Bohrium's external service using a Bohrium access key. <br>
Mitigation: Use only with documents approved for Bohrium processing; avoid confidential, proprietary, client, secret, or regulated documents unless Bohrium is approved for that data and its retention and privacy terms are understood. <br>


## Reference(s): <br>
- [Bohrium PDF parsing API endpoint](https://open.bohrium.com/openapi/v1/parse) <br>
- [ClawHub skill page](https://clawhub.ai/sorrymaker0624/bohrium-pdf-parser) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides HTTP API submission, polling, result retrieval, and handling of task tokens and extracted PDF content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
