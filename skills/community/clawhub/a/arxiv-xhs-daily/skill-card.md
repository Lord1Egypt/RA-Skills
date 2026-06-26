## Description: <br>
Read newly announced arXiv papers from cs.AI and cs.CL, filter them by user-defined research topics such as diffusion llm, summarize matching papers into reading notes, and optionally publish a Xiaohongshu post. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhrli324](https://clawhub.ai/user/zhrli324) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and research-content operators use this skill to run a configurable daily arXiv survey, generate concise reading notes, prepare a Xiaohongshu-style post draft, and publish it when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish generated content to Xiaohongshu using local account configuration when run with publishing enabled. <br>
Mitigation: Run with --dry-run first and review the generated title, body, image, destination account, and MCPORTER_CONFIG_PATH before any publish run. <br>
Risk: External arXiv paper metadata is used as input to generated notes and post drafts. <br>
Mitigation: Treat paper metadata as untrusted input and review generated notes and post drafts before scheduling or publishing. <br>


## Reference(s): <br>
- [Operations Guide](artifact/references/operations.md) <br>
- [arXiv API endpoint](http://export.arxiv.org/api/query) <br>
- [ClawHub release page](https://clawhub.ai/zhrli324/arxiv-xhs-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, image files, shell commands, configuration guidance] <br>
**Output Format:** [Markdown notes, JSON post drafts, PNG cover images, command-line status text, and optional publish result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes run artifacts under data/<topic>/<date>/raw/ and data/<topic>/<date>/processed/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
