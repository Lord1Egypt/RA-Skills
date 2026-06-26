## Description: <br>
Provides agent guidance for CSAM detection, blocking, evidence preservation, and reporting workflows using hash matching, content analysis, and behavior analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Platform safety, trust and legal operators use this skill to configure agent workflows for detecting possible CSAM, blocking user-generated content, preserving evidence, and preparing required reports. It is intended for authorized operators with legal review and scoped operational credentials. <br>

### Deployment Geography for Use: <br>
Global, subject to jurisdiction-specific CSAM reporting and privacy requirements. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents broad automatic reporting, enforcement, monitoring, and evidence-retention authority. <br>
Mitigation: Install only for authorized platform safety or legal operators, require jurisdiction-specific legal approval, and add human-review gates where legally appropriate. <br>
Risk: Reporting credentials and preserved evidence are highly sensitive. <br>
Mitigation: Independently review the npm package and dependencies, pin verified versions, scope reporting credentials, minimize evidence retention, and restrict access to evidence stores. <br>
Risk: Mistaken enforcement can affect users and create appeal or rollback obligations. <br>
Mitigation: Document review, appeal, and rollback handling before enabling automatic account or content actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/raghulpasupathi/csam-shield) <br>
- [Publisher profile](https://clawhub.ai/user/raghulpasupathi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes high-risk operational guidance for reporting, enforcement, evidence retention, and access control.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
