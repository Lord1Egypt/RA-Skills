## Description: <br>
Context-Aware Doc Generator: Automatically syncs Python docstrings (Google style), Go comments, and README.md based on code changes. Also logs change summaries to a local KB/ChromaDB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shangter666](https://clawhub.ai/user/shangter666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use doc-sync to keep Python docstrings, Go comments, README sections, and a local change-history knowledge base aligned with code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested docstring or README updates may be incorrect or misleading if code behavior is misunderstood. <br>
Mitigation: Review proposed documentation edits before committing them. <br>
Risk: Knowledge-base summaries may retain secrets, proprietary rationale, or sensitive paths in local project storage. <br>
Mitigation: Avoid including sensitive information in KB summaries and review local .gemini data before sharing the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shangter666/doc-sync) <br>
- [Doc Styles](references/doc_styles.md) <br>
- [Google Python Style Guide: Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) <br>
- [Effective Go: Commentary](https://golang.org/doc/effective_go.html#commentary) <br>
- [Go Doc Comments](https://go.dev/doc/comment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with proposed documentation edits and optional shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local knowledge-base summaries to ChromaDB or JSONL when the user requests KB sync.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
