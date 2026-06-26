## Description: <br>
Survey arXiv papers from a given year to present on a specific theme, categorize papers, translate abstracts to Chinese, and generate a structured Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[6eanut](https://clawhub.ai/user/6eanut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to collect recent arXiv paper metadata for a topic and produce a structured survey report for review and refinement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public arXiv API requests and writes Markdown files to the chosen output directory. <br>
Mitigation: Review the command arguments and output directory before running, and inspect the generated report before relying on it. <br>
Risk: The bundled script creates a report skeleton and does not fully implement the advertised categorization or Chinese translation by itself. <br>
Mitigation: Use the agent to refine categories, summaries, and translations after the script generates the initial report. <br>


## Reference(s): <br>
- [arXiv API](https://export.arxiv.org/api/query) <br>
- [arXiv paper page](https://arxiv.org/abs/xxxx.xxxxx) <br>
- [ClawHub skill page](https://clawhub.ai/6eanut/arxiv-survey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local report file named arxiv-survey-<year>-<theme-slug>.md in the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
