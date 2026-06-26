## Description: <br>
Scan websites, GitHub repositories, and Claw Hub skills for practical security issues using a local quick website scan and CyberLens cloud analysis when connected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadoprizm](https://clawhub.ai/user/shadoprizm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and teams use this skill to scan websites, GitHub repositories, and Claw Hub skills for security findings before shipping, installing, or trusting them. It also helps turn scan results into readable remediation guidance and shareable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning may contact websites, repositories, Claw Hub packages, and CyberLens cloud services for targets the user asks it to scan. <br>
Mitigation: Scan only authorized targets, use local scanning for sensitive websites where possible, and connect to cloud scanning only when the user accepts that target data may be sent to CyberLens services. <br>
Risk: A connected account stores or uses a CyberLens API key on the local machine. <br>
Mitigation: Protect the local configuration file, prefer the CYBERLENS_API_KEY environment variable on shared systems, and rotate the key if it may have been exposed. <br>
Risk: Generated reports can contain security findings, target details, and remediation context that may be sensitive. <br>
Mitigation: Review markdown and PDF reports before sharing them outside the intended audience. <br>


## Reference(s): <br>
- [CyberLens homepage](https://cyberlensai.com) <br>
- [Claw Hub skill page](https://clawhub.ai/shadoprizm/cyberlens) <br>
- [Publisher profile](https://clawhub.ai/user/shadoprizm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Structured scan results, plain-text guidance, markdown reports, and optional PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include security scores, letter grades, findings, remediation advice, report paths, and account or quota status.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
