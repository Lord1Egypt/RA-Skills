## Description: <br>
Helps an agent analyze uploaded data files up to 100MB by reading local files, running pandas-based analysis code, and returning structured findings and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users, operators, developers, students, and researchers use this skill to delegate single-file data-analysis tasks such as sales reviews, campaign evaluation, log analysis, and survey summaries. It is intended for natural-language requests that need local file reading, statistical analysis, optional visualization, and a concise result narrative. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated analysis code or conclusions may be incorrect or misleading. <br>
Mitigation: Review generated code before execution and validate reported findings against the source dataset and domain expectations. <br>
Risk: Processing untrusted datasets in the agent workspace can expose local files or produce unsafe file operations. <br>
Mitigation: Use the skill only with data files you are comfortable processing, keep outputs in the working directory, and avoid absolute paths or parent-directory references. <br>
Risk: External integrations added by the user may mishandle credentials. <br>
Mitigation: Provide external API credentials only through environment variables and do not hardcode secrets in prompts, scripts, or generated files. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/data-analyst-expert-free) <br>
- [SkillHub homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, code blocks, and structured JSON-style results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focused on single-file analysis up to 100MB; outputs commonly include data overview, key findings, business recommendations, execution logs, and optional charts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
