## Description: <br>
Pre-publish security scan for ClawHub skills - Scans code for patterns that might get flagged as suspicious and gives fixing suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyiyuleyuli-cloud](https://clawhub.ai/user/yuyiyuleyuli-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill before releasing ClawHub skills to scan a skill folder for suspicious code patterns, run a pre-publish checklist, and review remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running scan.py or precheck.py can charge 0.001 USDT through SkillPay and sends billing metadata to SkillPay. <br>
Mitigation: Run paid commands only when billing is intended, and provide SKILLPAY_API_KEY or --api-key only for authorized use. <br>
Risk: A broad scan path may inspect more files than the user intended. <br>
Mitigation: Scope --path to the specific skill folder being prepared for publication. <br>


## Reference(s): <br>
- [ClawHub Security Scan release page](https://clawhub.ai/yuyiyuleyuli-cloud/clawhub-security-scan) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with optional JSON scan report and inline command or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a non-zero exit status when high-risk findings are detected.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
