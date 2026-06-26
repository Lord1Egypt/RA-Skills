## Description: <br>
Creates publication-ready charts from CSV, JSON, FRED, or inline data, with support for line, bar, scatter, area-fill, indexed series, annotations, and multi-series overlays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent workflows use this skill to generate chart configuration, shell commands, and Python-based chart outputs for economic data, time-series comparison, trend analysis, and custom plotting tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local data files and fetch CSV or FRED data from URLs supplied in configuration. <br>
Mitigation: Review configurations before execution and treat URLs or configs from other people as untrusted. <br>
Risk: The skill writes chart image files to configured output paths. <br>
Mitigation: Use explicit output paths in trusted directories and check paths before running generated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pratyushchauhan/data-chart-builder) <br>
- [Publisher profile](https://clawhub.ai/user/pratyushchauhan) <br>
- [FRED data service](https://fred.stlouisfed.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, Python code, and generated chart image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads configured local or remote data sources and writes chart image files to user-specified output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
