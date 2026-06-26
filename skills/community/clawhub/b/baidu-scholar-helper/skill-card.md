## Description: <br>
Searches Baidu Scholar and arXiv for academic papers, sorts results, summarizes core contributions and innovations, and downloads PDFs for research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiliuah](https://clawhub.ai/user/weiliuah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and agent operators use this skill to find papers on Baidu Scholar or arXiv, review citation-oriented search results, summarize paper contributions, and save PDFs into organized local folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes academic-site network requests and downloads remote PDFs. <br>
Mitigation: Use it only in environments where outbound academic search and PDF downloads are permitted. <br>
Risk: The skill runs Poppler PDF utilities such as pdftotext and pdfimages. <br>
Mitigation: Install patched system packages and process PDFs in a contained workspace when handling untrusted documents. <br>
Risk: The skill automatically saves downloaded PDFs under Desktop paper folders. <br>
Mitigation: Run searches from an expected user account and review the output folder to avoid unwanted files on the main Desktop. <br>


## Reference(s): <br>
- [Baidu Scholar](https://xueshu.baidu.com) <br>
- [arXiv API](https://export.arxiv.org/api/query) <br>
- [arXiv](https://arxiv.org) <br>
- [Semantic Scholar](https://www.semanticscholar.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/weiliuah/baidu-scholar-helper) <br>
- [Publisher Profile](https://clawhub.ai/user/weiliuah) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown-style research report with search results, summaries, links, download status, and local PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create folders and save downloaded PDFs under ~/Desktop/papers/<query>/.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
