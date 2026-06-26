## Description: <br>
Tool-only paper processing skill with a manual language parameter: supports batch artifact download for many papers or single-paper download, then the model manually reads source/PDF and writes summary.md in the selected language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xukp20](https://clawhub.ai/user/xukp20) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and research workflow operators use this skill to download arXiv source or PDF artifacts for one or many paper directories, then have the agent read the paper and write a grounded summary.md in the selected language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded arXiv source archives may be malformed and could write outside the intended extraction folder. <br>
Mitigation: Run the skill in a non-sensitive workspace, review downloaded contents as untrusted files, and prefer a version with hardened archive extraction before processing arbitrary paper IDs. <br>
Risk: The skill runs local Python scripts that download and extract remote paper artifacts. <br>
Mitigation: Inspect the scripts before use, keep paper runs isolated from sensitive files, and review generated logs and summaries before relying on them. <br>


## Reference(s): <br>
- [Summary Format Reference](references/summary-format.md) <br>
- [English Summary Example](references/summary-example-en.md) <br>
- [Chinese Summary Example](references/summary-example-zh.md) <br>
- [ClawHub Release Page](https://clawhub.ai/xukp20/arxiv-paper-processor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown summary files with optional shell commands and JSON download logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one summary.md per paper directory and may create source artifacts, PDFs, and download log JSON files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
