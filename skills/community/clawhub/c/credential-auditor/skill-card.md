## Description: <br>
Automates authorized credential security auditing with default device credential lookup, password dictionary generation, and multi-protocol password testing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeanphorn](https://clawhub.ai/user/jeanphorn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, penetration testers, and auditors use this skill to support credential assessments on systems they are authorized to test. It helps find default credentials, build target-specific password lists, run controlled password checks, and summarize remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated password testing can be misused against systems without authorization. <br>
Mitigation: Require written authorization and an explicit target scope before enabling any login attempts. <br>
Risk: Password guessing can trigger account lockouts, service disruption, or detection controls. <br>
Mitigation: Use low request rates, lockout-aware attempt limits, and manual confirmation before active testing. <br>
Risk: Generated wordlists and credential reports may contain sensitive information. <br>
Mitigation: Store outputs privately, restrict access, and delete or archive them according to the assessment data-handling plan. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeanphorn/credential-auditor) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Python](https://www.python.org/) <br>
- [device_passwords.json](references/device_passwords.json) <br>
- [password_rules.json](references/password_rules.json) <br>
- [protocol_configs.json](references/protocol_configs.json) <br>
- [usernames.txt](references/usernames.txt) <br>
- [passlist.txt](references/passlist.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with shell command examples, generated wordlists, JSON reports, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local files containing wordlists or credential audit results; these should be handled as sensitive data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
