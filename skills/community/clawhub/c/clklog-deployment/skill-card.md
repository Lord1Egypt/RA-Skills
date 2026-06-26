## Description: <br>
Helps users choose Docker quick deployment or source deployment for ClkLog and follow official documentation to set up the user behavior analytics system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaingush](https://clawhub.ai/user/gaingush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to evaluate a Linux deployment environment, choose between Docker Compose and source deployment paths, and follow official ClkLog setup and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployed ClkLog product handles user behavior analytics and may collect identifiers or behavioral data. <br>
Mitigation: Confirm lawful basis or user consent, minimize collected identifiers, configure retention and deletion processes, and document the analytics collection scope before using it with real users. <br>
Risk: Analytics dashboards and backing databases may expose sensitive behavior data if access is too broad. <br>
Mitigation: Restrict dashboard and database access to authorized operators and review access controls before starting services. <br>
Risk: Incorrect Docker or source configuration can start services with unsuitable defaults for the operator's environment. <br>
Mitigation: Review the official ClkLog Docker or source deployment configuration and verify environment prerequisites before launching services. <br>
Risk: ClkLog itself is described in the artifact as AGPL-3.0 software with commercial licensing considerations. <br>
Mitigation: Review AGPL-3.0 obligations and any required commercial license terms before modifying, redistributing, or integrating ClkLog into closed-source commercial products. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaingush/clklog-deployment) <br>
- [ClkLog official site](https://clklog.com) <br>
- [ClkLog documentation center](https://clklog.com/resource/docscenter.html) <br>
- [ClkLog Docker installation guide](https://clklog.com/install/docker/intro.html) <br>
- [ClkLog Docker FAQ](https://clklog.com/install/docker/fqa.html) <br>
- [ClkLog source deployment guide](https://clklog.com/install/source/deployment.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and official documentation links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment checks, deployment path selection, troubleshooting guidance, and license reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
