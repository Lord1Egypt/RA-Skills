## Description: <br>
Personal Git history self-review tool that generates descriptive reports about commit patterns, code style, and quality indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to inspect their own local Git history, summarize commit discipline, rhythm, change patterns, code quality markers, and style indicators, and produce self-reflection reports. It is intended for consensual self-review rather than monitoring, ranking, or HR decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and processes local Git history, which may include personal or sensitive repository activity. <br>
Mitigation: Run it only on repositories you own or have consent to analyze, and avoid publishing generated reports that contain personal data. <br>
Risk: The evidence flags inconsistent privacy and data-flow claims around local/offline operation and possible LLM-provider exposure. <br>
Mitigation: Treat repository-derived content as potentially shared with the active agent or LLM provider unless the publisher clarifies the data flow. <br>
Risk: The evidence flags a trigger scope broader than the stated self-review purpose, creating misuse risk for monitoring or HR decisions. <br>
Mitigation: Limit use to consensual self-review and reject requests to rank, compare, monitor, or make employment decisions about people. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-analysis-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated report formats including Markdown, JSON, HTML, and PDF] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces descriptive Git-history self-review reports; does not produce scores, grades, rankings, or comparative performance tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
