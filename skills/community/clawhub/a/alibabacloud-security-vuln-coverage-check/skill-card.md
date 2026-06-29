## Description: <br>
Checks whether Alibaba Cloud Security Center, WAF, Cloud Firewall, or RASP coverage is recorded for a CVE or AVD ID using a bundled offline AVD snapshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, support teams, and presales solution architects use this skill to answer customer questions about whether specific high-risk CVE or AVD vulnerabilities are covered by supported Alibaba Cloud security products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coverage answers may be stale because the skill uses a bundled offline snapshot rather than live Alibaba Cloud data. <br>
Mitigation: Verify very recent vulnerabilities or high-impact customer claims against official Alibaba Cloud AVD or product channels before relying on the result. <br>
Risk: The skill only covers Security Center, WAF, Cloud Firewall, and RASP. <br>
Mitigation: For other Alibaba Cloud products, route the question to that product's official support or documentation channel instead of extrapolating from this skill. <br>
Risk: A coverage lookup is not proof that a deployed control blocks a real attack payload in a specific customer environment. <br>
Mitigation: Use an appropriate product verification workflow when the user needs live enforcement validation rather than coverage status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-security-vuln-coverage-check) <br>
- [Alibaba Cloud AVD vulnerability database](https://avd.aliyun.com/) <br>
- [Coverage data snapshot](references/coverage-data.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Chinese plain text or Markdown answers with AVD links; Markdown tables for bulk CVE checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a bundled offline snapshot and does not require credentials or network access.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
