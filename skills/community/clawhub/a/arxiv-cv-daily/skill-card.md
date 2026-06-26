## Description: <br>
Fetch arXiv papers for a target date in cs.CV, screen them against a user topic, save logs under a user-chosen output directory, download matched PDFs, and summarize the matched papers from full text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrytea](https://clawhub.ai/user/harrytea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and research assistants use this skill to fetch a dated arXiv cs.CV catalog, screen papers against a topic, and produce saved shortlists plus optional full-text paper summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow contacts arXiv and writes paper metadata, PDFs, extracted text, logs, and summaries to local storage. <br>
Mitigation: Use a non-sensitive output directory, review the saved run directory, and delete local artifacts when they are no longer needed. <br>
Risk: Detailed summaries depend on downloaded PDFs and extracted full text, which may be incomplete if retrieval or text extraction fails. <br>
Mitigation: Check the saved logs and extracted text before relying on detailed paper analysis. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/harrytea/arxiv-cv-daily) <br>
- [arXiv API endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [Markdown responses with saved JSON logs, PDF files, extracted text files, and summary files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Run artifacts are saved under the user-selected output root.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
