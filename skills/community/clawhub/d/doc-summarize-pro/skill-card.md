## Description: <br>
Enhanced document summarizer. Smart summary, bullet extraction, executive summary, chapter breakdown, multi-doc comparison, translate+summarize. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and document-heavy teams use this skill to summarize local text documents, extract keywords and outlines, compare documents, and export summaries in reusable formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local processing history can record processed file paths and commands under $HOME/.doc-summarize-pro/history.log. <br>
Mitigation: Avoid processing sensitive paths when history retention is a concern, and review or clear the local history file according to the user's retention policy. <br>
Risk: Generated summaries, keyword lists, and comparisons can omit nuance or produce misleading reductions of source documents. <br>
Mitigation: Verify summaries against the source material before relying on them for important decisions. <br>
Risk: The translate-summary behavior summarizes text but does not provide full translation. <br>
Mitigation: Use a dedicated translation tool when translation accuracy is required. <br>


## Reference(s): <br>
- [Doc Summarize Pro on ClawHub](https://clawhub.ai/xueyetianya/doc-summarize-pro) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text summaries, Markdown or JSON exports, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local configuration and processing history under $HOME/.doc-summarize-pro.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
