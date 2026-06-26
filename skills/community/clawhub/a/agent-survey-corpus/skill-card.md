## Description: <br>
Download a small corpus of open-access arXiv survey and review PDFs about LLM agents, then extract text for style learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to build a local reference corpus of arXiv agent survey papers and inspect extracted text, section structure, and style patterns for survey-writing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes broad research-writing pipeline files and workflow tooling beyond the advertised arXiv corpus downloader. <br>
Mitigation: Review before installing, keep it sandboxed in sensitive repositories, and invoke artifact/scripts/run.py directly for the advertised ref/agent-surveys workflow. <br>
Risk: The skill downloads remote PDFs and writes local PDF, text, JSONL, and Markdown files into the selected workspace. <br>
Mitigation: Review the arXiv ID input list, run in a dedicated workspace, and keep generated ref/agent-surveys PDF and text directories out of git. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/WILLOSCAR/agent-survey-corpus) <br>
- [arXiv abstract pages](https://arxiv.org/abs/) <br>
- [arXiv PDF downloads](https://arxiv.org/pdf/) <br>
- [arXiv API query endpoint](https://export.arxiv.org/api/query?id_list={arxiv_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown instructions plus generated PDFs, text extracts, JSONL index records, and a Markdown style report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and network access; downloads only arXiv PDFs and writes outputs under ref/agent-surveys by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
