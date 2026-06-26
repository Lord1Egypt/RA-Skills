## Description: <br>
Automates local CSV data analysis and cleaning, producing Markdown reports or cleaned CSV/JSON outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arthasking123](https://clawhub.ai/user/arthasking123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to run basic local CSV summaries, clean duplicated or missing data, and generate shareable analysis artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated output files can contain copies or summaries of sensitive datasets. <br>
Mitigation: Treat generated reports and cleaned files as sensitive data, restrict access, and delete them when they are no longer needed. <br>
Risk: The implementation requires pandas and supports a narrower feature set than some artifact text advertises. <br>
Mitigation: Install pandas before use and validate that required Excel, charting, PDF/HTML, trend, or anomaly workflows are implemented before relying on them. <br>


## Reference(s): <br>
- [AI Data Analysis on ClawHub](https://clawhub.ai/arthasking123/ai-data-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Markdown reports, CSV/JSON data files, and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated reports and cleaned data to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
