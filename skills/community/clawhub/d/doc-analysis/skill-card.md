## Description: <br>
Doc Analysis helps agents analyze Word .doc and .docx files with MinerU and return structured Markdown that preserves headings, paragraphs, tables, lists, and layout cues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, editors, quality assurance teams, and agent developers use this skill to inspect Word document structure, extract content, and preserve layout before processing, editing, or conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents or URLs processed by the skill may be sent to MinerU or the configured extraction backend. <br>
Mitigation: Review the extraction service's data-handling terms and avoid confidential, regulated, or private documents until the processing path is approved. <br>
Risk: The skill relies on a MinerU authentication token for full extraction. <br>
Mitigation: Provide the token through the documented auth flow or environment variable and avoid committing, logging, or sharing token values. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mzlzyca/doc-analysis) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU API Token Management](https://mineru.net/apiManage/token) <br>
- [OpenDataLab MinerU Repository](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with CLI command examples and structured document extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mineru-open-api and MINERU_TOKEN for full extraction; supports local Word files and URLs; document content is written to stdout or an output directory while progress messages go to stderr.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
