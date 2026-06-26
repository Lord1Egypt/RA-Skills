## Description: <br>
Data Analyzer helps agents analyze, summarize, compare, aggregate, and report on local Excel, CSV, Word, PDF, TXT, and Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other users can use this skill through an agent to inspect selected local files or folders, compare datasets, summarize document contents, calculate basic statistics, and produce reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local files and folders selected by the user, which may include sensitive documents. <br>
Mitigation: Point the agent only at narrow, intended folders and avoid sensitive directories unless the analysis requires them. <br>
Risk: Generated summaries or reports may expose sensitive local data if shared externally. <br>
Mitigation: Review reports and summaries before sharing or publishing them. <br>
Risk: The skill depends on Python packages for parsing and reporting. <br>
Mitigation: Install suggested Python packages from trusted package sources and keep the environment scoped to this task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tobewin/data-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [Markdown reports, structured summaries, generated documents, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Markdown, Excel, Word, or PDF reports from local files selected by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter: 1.0.9) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
