## Description: <br>
Extracts mathematical formulas and equations from PDF documents using MinerU, including conversion of detected formula content into LaTeX-style Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, academic professionals, developers, and agents use this skill to extract formulas from PDF papers, textbooks, and technical documents and reuse them as LaTeX-style Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs or URLs may be processed by an external MinerU service. <br>
Mitigation: Use only documents that your organization permits for MinerU service processing, and review applicable data-handling terms before use. <br>
Risk: The workflow requires a MinerU token and the mineru-open-api CLI. <br>
Mitigation: Install the CLI only from trusted package sources and manage MINERU_TOKEN as a secret. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mzlzyca/extract-formulas-from-pdf) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and LaTeX-style formula output from MinerU] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mineru-open-api, requires MINERU_TOKEN or mineru-open-api auth, and can write extraction results to an output directory.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
