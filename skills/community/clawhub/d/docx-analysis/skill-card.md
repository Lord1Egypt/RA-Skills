## Description: <br>
Analyzes Word .docx files with MinerU and returns structured Markdown that preserves headings, tables, lists, and layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, reviewers, and agents use this skill to inspect Word document structure, understand layout, and convert selected .docx content into Markdown for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected Word documents, and possibly URLs, may be processed by the external MinerU service. <br>
Mitigation: Use the skill only for documents appropriate for external processing, review MinerU data handling terms before confidential or regulated use, and avoid sending sensitive files unless approved. <br>
Risk: The MINERU_TOKEN credential is required for full extraction mode. <br>
Mitigation: Store the token in the environment or approved secret storage, avoid committing it to files, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mzlzyca/docx-analysis) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit Markdown to stdout or save output to a directory through the MinerU CLI.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
