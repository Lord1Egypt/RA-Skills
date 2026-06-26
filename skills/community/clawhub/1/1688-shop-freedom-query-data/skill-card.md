## Description: <br>
This skill helps an agent answer natural-language questions about 1688 merchant operations by matching the question to relevant data APIs and returning real shop metrics with interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External merchants and their agents use this skill to query 1688 shop traffic, transaction metrics, product rankings, search keywords, peer comparisons, and real-time shop data. It supports natural-language questions, asks for clarification when API or time-range choices are ambiguous, and returns data-backed business interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 1688 access key and may store it in the OpenClaw config file. <br>
Mitigation: Install only in trusted workspaces, protect the config file, and rotate the access key if the config is exposed. <br>
Risk: Queried merchant metrics or generated exports may contain sensitive business data. <br>
Mitigation: Avoid shared workspaces for generated output and review exported files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-shop-freedom-query-data) <br>
- [Interaction component specifications](references/interaction-specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with tables and JSON-backed command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt for API, time range, or export selection; optional HTML or Excel export can be produced after user selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
