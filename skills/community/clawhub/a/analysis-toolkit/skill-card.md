## Description: <br>
Quality-control and data-analysis toolkit for inspection and testing workflows, covering internal quality control, inter-lab comparison, inter-batch comparison, method validation, and trend monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, quality engineers, and laboratory analysts use this skill to plan and run statistical quality-control workflows, validate methods, compare groups or batches, monitor trends, and generate human-readable analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configuration panel can be exposed as a network-reachable local server and can persist changes to templates. <br>
Mitigation: Run it only on trusted machines and networks, bind it to localhost before use when possible, and review saved template changes before relying on them. <br>
Risk: Generated operators can be written into Python source files. <br>
Mitigation: Require human code review and run the included validation or self-test workflows before executing newly generated operators. <br>
Risk: Some generated HTML reports may depend on CDN-hosted chart assets. <br>
Mitigation: Treat those reports as non-offline artifacts unless CDN access is approved, or use the local/static rendering path when offline operation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/analysis-toolkit) <br>
- [Quickstart](references/quickstart.md) <br>
- [Data interface](references/data-interface.md) <br>
- [Pipeline reference](references/pipeline.md) <br>
- [Report generation](references/report-generation.md) <br>
- [Regression and method validation](references/regression-validation.md) <br>
- [Time series analysis](references/time-series.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown responses with Python snippets, structured numeric results, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files and local template or configuration files when invoked.] <br>

## Skill Version(s): <br>
2.0.4 (source: SKILL.md frontmatter, ClawHub release evidence, changelog released 2026-06-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
