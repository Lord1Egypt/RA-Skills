## Description: <br>
Douyin Local Food is a restaurant-operations Agent for Douyin Local Life that provides store diagnosis, dish promotion, group-buying design, content strategy, data analysis, and customer-service script guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronnee520](https://clawhub.ai/user/aaronnee520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant operators and marketing teams use this skill to plan Douyin Local Life restaurant operations, including store diagnosis, dish promotion, group-buying packages, content calendars, metric reviews, and customer-service scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised data-analysis command may return fixed sample metrics rather than analyzing the provided file. <br>
Mitigation: Treat analysis output as sample guidance and verify business metrics against real Douyin reports before making operational decisions. <br>
Risk: Configuration can contain account, POI, shop, and restaurant business details. <br>
Mitigation: Avoid storing passwords or API tokens in config files and keep local configuration files out of shared repositories. <br>
Risk: The skill installs Python dependencies and runs a local script. <br>
Mitigation: Install dependencies in a virtual environment and review the script before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/aaronnee520/douyin-local-food) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI writes local JSON outputs for diagnosis, dish plans, group-buying plans, content calendars, analytics reports, and customer-service scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
