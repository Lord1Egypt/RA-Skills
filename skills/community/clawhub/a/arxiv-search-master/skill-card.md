## Description: <br>
arXiv Search Master helps agents search arXiv, download papers, export metadata, run batch searches, and produce paper summaries for academic literature review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PeterKouss](https://clawhub.ai/user/PeterKouss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to retrieve arXiv papers by keyword, author, category, or date, then download PDFs, export citations, merge metadata, and draft literature summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that batch JSONL input can choose output file paths outside the intended folder. <br>
Mitigation: Run only trusted batch JSONL files or inspect each name field first to ensure it contains no absolute paths, slashes, or '..' traversal. <br>
Risk: Downloaded PDFs are external documents and may contain unsafe or unwanted content. <br>
Mitigation: Treat downloaded PDFs as untrusted documents and review them in a hardened viewer or isolated environment. <br>
Risk: Disabling SSL verification weakens transport security for downloads. <br>
Mitigation: Avoid using --no-verify-ssl and keep SSL verification enabled unless there is a reviewed operational exception. <br>
Risk: Dependencies are specified as ranges rather than a lockfile, which can change installed package versions over time. <br>
Mitigation: Install in an isolated virtual environment and prefer pinned dependencies or a lockfile before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PeterKouss/arxiv-search-master) <br>
- [Publisher profile](https://clawhub.ai/user/PeterKouss) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [arXiv](https://arxiv.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated JSON metadata, citation exports, summaries, and downloaded PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses command-line arguments; can emit JSON, BibTeX, CSV, RIS, summary JSON, logs, and PDF files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
