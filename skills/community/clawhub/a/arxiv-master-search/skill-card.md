## Description: <br>
arXiv Master Search helps agents search arXiv papers, download PDFs, export metadata, run batch queries, and generate lightweight summaries for literature review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PeterKouss](https://clawhub.ai/user/PeterKouss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to automate arXiv discovery workflows, including query-based search, paper retrieval, citation export, batch processing, and summary generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes remote PDFs and arXiv metadata, which can expose the runtime to malformed or unexpected external content. <br>
Mitigation: Install and run it in an environment where remote PDF processing is acceptable, and review downloaded files before reusing them in downstream workflows. <br>
Risk: Dependency hygiene needs attention for packages such as requests, urllib3, PyYAML, PyPDF2, and pdfminer.six. <br>
Mitigation: Prefer pinned, regularly updated dependency versions and refresh the environment when security fixes are released. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PeterKouss/arxiv-master-search) <br>
- [Publisher profile](https://clawhub.ai/user/PeterKouss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with command examples plus generated JSON, BibTeX, CSV, RIS, PDF, and summary files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized into search metadata, downloaded PDFs, exported citation data, and generated summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
